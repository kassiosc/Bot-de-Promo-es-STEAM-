import time
from bot import varrer_promocao_steam
import schedule

INTERVALO_HORAS = 6

def main():
    
    varrer_promocao_steam()
    
    schedule.every(INTERVALO_HORAS).hours.do(varrer_promocao_steam)

    print(f"Bot ativo! Próxima varredura em {INTERVALO_HORAS} horas...")
    while True:
        schedule.run_pending()
        time.sleep(60)
    
              


if __name__ == '__main__':
    main()