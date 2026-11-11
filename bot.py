import json
import os
import time
import requests
from winotify import Notification, audio

# Configurações
DESCONTO_MINIMO = 70
MINIMO_AVALIACOES = 1000
ARQUIVO_HISTORICO = "promocoes_enviadas.json"

# Montagem segura do domínio da Steam para evitar cortes ao copiar/colar o texto
DOMINIO = "store." + "steampowered" + ".com"


def carregar_historioco():
  if os.path.exists(ARQUIVO_HISTORICO):
    with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
      # Converte a lista salva em um 'set' (conjunto), que deixa a busca muito mais rápida
      return set(json.load(f))
  # Se for a primeira vez rodando o bot (arquivo não existe), retorna um conjunto vazio
  return set()


def salvar_historico(historioco):
  with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
    # Transforma o conjunto de volta em lista para poder salvar em JSON
    json.dump(list(historioco), f)


def varrer_promocao_steam():
  # Aviso visual no Windows de que a busca começou
  notificacao = Notification(
      app_id="Varedura de Promoções",
      title="Começando a varedura",
      msg="Buscando ofertas na Steam...",
      duration="short",
  )
  notificacao.set_audio(audio.Default, loop=False)
  notificacao.show()

  historico = carregar_historioco()
  novas_promocoes = []

  # Percorre as 3 primeiras páginas da busca (50 jogos por página = 150 jogos analisados)
  for pagina in range(0, 3):
    start = pagina * 50  # Calcula de qual posição começar (0, 50, 100)

    # Monta a URL de busca filtrando apenas promoções (specials=1) em Reais (cc=BR)
    caminho_busca = "/search/results/?query"
    parametros = (
        f"&start={start}&count=50&specials=1&filter=topsellers"
        "&cc=BR&l=portuguese&json=1"
    )
    url = "https://" + DOMINIO + caminho_busca + parametros

    try:
      # Acessa a página da Steam
      resposta = requests.get(url, timeout=10)
      if resposta.status_code != 200:
        continue

      dados = resposta.json()
      itens = dados.get("items", [])

      for item in itens:
        nome = item.get("name")
        link = item.get("logo", "")
        app_id = link.split("/apps/")[1].split("/")[0] if "/apps/" in link else nome

        if app_id not in historico:
          detalhes = verificar_detalhes_jogo(app_id)
          # Verifica se o jogo tem preço válido e se o desconto atinge a meta mínima
          if (
              detalhes
              and detalhes["desconto"] >= DESCONTO_MINIMO
              and detalhes["avaliacoes"] >= MINIMO_AVALIACOES
          ):
            novas_promocoes.append(detalhes)
            historico.add(app_id)

        time.sleep(0.5)

    except Exception as error:
      notificacao = Notification(
          app_id="Algo esta errado",
          title="Verifique o possivel erro",
          msg=f"Erro na requisição: {error}",
          duration="long",
      )
      notificacao.set_audio(audio.Default, loop=False)
      notificacao.show()

  if novas_promocoes:
    enviar_relatorio(novas_promocoes)
    salvar_historico(historico)
  else:
    notificacao = Notification(
        app_id="Varedura feita",
        title="Varedura muito bem concluida",
        msg="Varredura concluída. Nenhuma nova promoção atingiu o critério",
        duration="short",
    )
    notificacao.set_audio(audio.Default, loop=False)
    notificacao.show()


def verificar_detalhes_jogo(app_id):
  if not str(app_id).isdigit():
    return None

  # Monta o endereço da API de detalhes do jogo específico
  caminho_api = f"/api/appdetails?appids={app_id}&cc=br&l=portuguese"
  url = "https://" + DOMINIO + caminho_api
  url_loja = "https://" + DOMINIO + f"/app/{app_id}"

  try:
    res = requests.get(url, timeout=10).json()
    if res and res[str(app_id)]["success"]:
      data = res[str(app_id)]["data"]
      if data.get("type") != "game":
        return None
      total_avaliacoes = data.get("recommendations", {}).get("total", 0)
      if "price_overview" in data:
        return {
            "nome": data["name"],
            "preco": data["price_overview"]["final"] / 100,
            "desconto": data["price_overview"]["discount_percent"],
            "avaliacoes": total_avaliacoes,
            "url": url_loja,
        }
  except Exception:
    pass
  return None


def enviar_relatorio(lista_jogos):
  for jogo in lista_jogos:
    mensagem = (
        f"-{jogo['desconto']}% | R$ {jogo['preco']:.2f}\n"
        "Clique para abrir na loja."
    )

    notificacao = Notification(
        app_id="Varredura de Promoções",
        title=f"🔥 {jogo['nome']}",
        msg=mensagem,
        duration="long",
    )
    notificacao.add_actions(label="Abrir na Steam", launch=jogo["url"])
    notificacao.set_audio(audio.Default, loop=False)
    notificacao.show()
    time.sleep(5)
