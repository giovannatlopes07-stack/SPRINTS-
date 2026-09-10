import time
from machine import Pin

# Configuração dos Pinos de Saída (LEDs)
led_verde = Pin(15, Pin.OUT)
led_amarelo = Pin(14, Pin.OUT)
led_vermelho = Pin(13, Pin.OUT)


def apagar_leds():
    led_verde.value(0)
    led_amarelo.value(0)
    led_vermelho.value(0)


def exibir_representacao_dados(valor_w):
    """Demonstra a representação de dados em Decimal, Binário e Hexadecimal (Conceito de Arquitetura de Computadores)"""
    valor_abs = abs(valor_w)
    print("\n--- REPRESENTAÇÃO DE DADOS (MEMÓRIA) ---")
    print(f"Valor analisado (Potência Disponível): {valor_w} W")
    print(f"Decimal:     {valor_w}")
    print(f"Binário:     {bin(valor_abs)}")
    print(f"Hexadecimal: {hex(valor_abs).upper()}")
    print("-----------------------------------------\n")


def processar_sessao_recarga(geracao, consumo):
    apagar_leds()

    # Cálculo da energia disponível
    disponivel = geracao - consumo

    print("=========================================")
    print(f"GERACAO:    {geracao} W")
    print(f"CONSUMO:    {consumo} W")
    print(f"DISPONIVEL: {disponivel} W")
    print(" ")
    print("STATUS:")

    # Lógica de decisão para determinação do estado da recarga
    # Limiares configurados:
    # >= 1000 W -> Recarga Autorizada (Verde)
    # > 0 W e < 1000 W -> Recarga Reduzida (Amarelo)
    # <= 0 W -> Recarga Bloqueada (Vermelho)

    if disponivel >= 1000:
        status = "RECARGA AUTORIZADA"
        led_verde.value(1)
    elif disponivel > 0:
        status = "RECARGA REDUZIDA"
        led_amarelo.value(1)
    else:
        status = "RECARGA BLOQUEADA"
        led_vermelho.value(1)

    print(status)
    exibir_representacao_dados(disponivel)


# Teste contínuo das 3 situações de operação solicitadas
cenarios = [
    {"geracao": 4000, "consumo": 1500},  # Situação 1: Autorizada (2500 W)
    {"geracao": 1800, "consumo": 1500},  # Situação 2: Reduzida (300 W)
    {"geracao": 1000, "consumo": 1800},  # Situação 3: Bloqueada (-800 W)
]

while True:
    for cenario in cenarios:
        processar_sessao_recarga(cenario["geracao"], cenario["consumo"])
        time.sleep(5)  # Intervalo de 5 segundos entre simulações