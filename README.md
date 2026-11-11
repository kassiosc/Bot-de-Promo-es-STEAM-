# 🎮 Bot Monitor de Promoções da Steam

Um bot automatizado desenvolvido em Python que realiza varreduras periódicas na loja da Steam (Brasil) em busca das melhores promoções de jogos populares e envia notificações nativas diretamente na área de trabalho do Windows.

---

## ✨ Funcionalidades

- **Varredura Automática:** Executa buscas na loja em intervalos de tempo configuráveis (padrão: a cada 6 horas).
- **Filtro de Popularidade:** Ordena pelos mais vendidos (`topsellers`) e exige um número mínimo de avaliações na Steam para evitar alertas de jogos desconhecidos.
- **Foco em Jogos Base:** Ignora automaticamente DLCs, expansões e trilhas sonoras.
- **Filtro de Desconto:** Notifica apenas ofertas que atingem a porcentagem mínima definida pelo usuário.
- **Controle de Histórico:** Salva os IDs dos jogos já notificados em um arquivo `promocoes_enviadas.json` para não enviar alertas repetidos.
- **Notificações Interativas no Windows:** Exibe alertas nativos com preço atual, porcentagem de desconto e um botão clicável para abrir a página do jogo diretamente na Steam.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- `requests` — Para consumo dos endpoints públicos da Steam.
- `schedule` — Para agendamento das varreduras periódicas.
- `winotify` — Para exibição de notificações nativas com botões de ação no Windows.
- `pyinstaller` — Para empacotar o projeto em um executável `.exe` independente.

---

## 📂 Estrutura do Projeto

```text
├── bot.py                     # Lógica de varredura, filtros, histórico e notificações
├── main.py                    # Ponto de entrada e agendamento das execuções
├── promocoes_enviadas.json    # Gerado automaticamente para evitar notificações duplicadas
└── README.md                  # Documentação do projeto
```

---

## 🚀 Como Instalar e Executar (Modo Desenvolvimento)

### 1. Pré-requisitos
Certifique-se de ter o **Python 3** instalado em sua máquina (Windows 10 ou 11).

### 2. Clone o repositório
```bash
git clone https://github.com
cd nome-do-repositorio
```

### 3. Instale as dependências
```bash
pip install requests schedule winotify
```

### 4. Inicie o bot
```bash
python main.py
```

---

## 📦 Como Criar o Executável (`.exe`) e Iniciar com o Windows

Para não precisar abrir o terminal manualmente toda vez, você pode transformar o bot em um executável que roda oculto em segundo plano ao ligar o computador.

### Passo 1: Instalar o PyInstaller
No terminal, dentro da pasta do projeto, instale a biblioteca de empacotamento:
```bash
pip install pyinstaller
```

### Passo 2: Gerar o arquivo `.exe` oculto
Execute o comando abaixo para criar um arquivo único que não abre a janela preta do prompt:
```bash
pyinstaller --onefile --noconsole --name "BotPromocoesSteam" main.py
```
- `--onefile`: Junta tudo em um único arquivo executável.
- `--noconsole`: Faz o bot rodar silenciosamente em segundo plano.
- `--name`: Define o nome do arquivo final.

Após concluir, o arquivo **`BotPromocoesSteam.exe`** estará dentro da pasta **`dist/`**.

### Passo 3: Configurar para iniciar com o Windows
1. Pressione as teclas **`Win + R`** no teclado para abrir a janela **Executar**.
2. Digite **`shell:startup`** e pressione **Enter** (isso abrirá a pasta de inicialização automática do Windows).
3. Vá até a pasta **`dist/`** do seu projeto, clique com o botão direito no **`BotPromocoesSteam.exe`** e selecione **Criar atalho**.
4. Mova esse **atalho** criado para dentro da pasta que você abriu no passo 2.

*(Nota: Sempre que o Windows iniciar, o bot começará a rodar automaticamente em segundo plano. O arquivo `promocoes_enviadas.json` será salvo na mesma pasta onde o `.exe` original estiver).*

---

## ⚙️ Personalização

Você pode ajustar os critérios de busca editando as constantes no topo dos arquivos (lembre-se de gerar o `.exe` novamente caso altere o código):

**No arquivo `bot.py`:**
```python
DESCONTO_MINIMO = 70  # Porcentagem mínima de desconto (ex: 70%)
MINIMO_AVALIACOES = 1000  # Quantidade mínima de avaliações na Steam
```

**No arquivo `main.py`:**
```python
INTERVALO_HORAS = 6  # Intervalo em horas entre cada varredura
```

---

## 📝 Licença

Este projeto é de uso livre para fins de estudo e automação pessoal.
