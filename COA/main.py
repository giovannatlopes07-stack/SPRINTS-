from machine import Pin
import time

# Configuração dos LEDs por veículo [Vermelho, Amarelo, Verde]
leds_car1 = [Pin(2, Pin.OUT), Pin(3, Pin.OUT), Pin(4, Pin.OUT)]
leds_car2 = [Pin(5, Pin.OUT), Pin(6, Pin.OUT), Pin(7, Pin.OUT)]
leds_car3 = [Pin(8, Pin.OUT), Pin(9, Pin.OUT), Pin(10, Pin.OUT)]

# Configuração do Botão (Simula a mudança de disponibilidade de energia)
btn_cenario = Pin(11, Pin.IN, Pin.PULL_DOWN)

# Banco de dados simulado dos veículos
veiculos = [
    {"id": 1, "bateria": 15, "demanda_kw": 7, "leds": leds_car1},
    {"id": 2, "bateria": 50, "demanda_kw": 7, "leds": leds_car2},
    {"id": 3, "bateria": 85, "demanda_kw": 7, "leds": leds_car3}
]

# Cenários de energia disponível em kW (Alta, Limitada, Baixa)
cenarios_energia = [25, 15, 6]
indice_cenario = 0

def atualizar_leds(veiculo, estado):
    """ Desliga todos os LEDs e liga apenas o correspondente ao estado """
    for led in veiculo["leds"]:
        led.value(0)
        
    if estado == "VERDE":
        veiculo["leds"][2].value(1) # Recarga Ativa
    elif estado == "AMARELO":
        veiculo["leds"][1].value(1) # Recarga Reduzida
    elif estado == "VERMELHO":
        veiculo["leds"][0].value(1) # Aguardando/Bloqueado

def gerenciar_recarga(energia_disponivel):
    print("="*40)
    print(f"ENERGIA DISPONÍVEL NO SISTEMA: {energia_disponivel} kW")
    
    demanda_total = sum(v["demanda_kw"] for v in veiculos)
    print(f"DEMANDA TOTAL DOS VEÍCULOS: {demanda_total} kW\n")

    # ALGORITMO DE TOMADA DE DECISÃO
    # Situação 1: Alta Disponibilidade (Energia >= Demanda)
    if energia_disponivel >= demanda_total:
        print("STATUS GERAL: ALTA DISPONIBILIDADE -> RECARGA ATIVA")
        for v in veiculos:
            atualizar_leds(v, "VERDE")
            print(f"Carro {v['id']} | Bat: {v['bateria']}% | Potência: {v['demanda_kw']}kW | LED: VERDE")

    # Situação 2: Disponibilidade Limitada (Distribuição/Redução)
    elif energia_disponivel > 10 and energia_disponivel < demanda_total:
        print("STATUS GERAL: DISPONIBILIDADE LIMITADA -> RECARGA REDUZIDA")
        potencia_reduzida = energia_disponivel / len(veiculos)
        for v in veiculos:
            atualizar_leds(v, "AMARELO")
            print(f"Carro {v['id']} | Bat: {v['bateria']}% | Potência: {potencia_reduzida:.1f}kW | LED: AMARELO")

    # Situação 3: Baixa Disponibilidade (Bloqueio seletivo por bateria)
    else:
        print("STATUS GERAL: BAIXA DISPONIBILIDADE -> RECARGA LIMITADA")
        # Ordena veículos pela bateria (menor bateria ganha prioridade)
        veiculos_ordenados = sorted(veiculos, key=lambda x: x["bateria"])
        energia_restante = energia_disponivel
        
        for v in veiculos_ordenados:
            if energia_restante >= v["demanda_kw"]:
                atualizar_leds(v, "VERDE")
                energia_restante -= v["demanda_kw"]
                print(f"Carro {v['id']} | Bat: {v['bateria']}% | Potência: {v['demanda_kw']}kW | LED: VERDE")
            else:
                atualizar_leds(v, "VERMELHO")
                print(f"Carro {v['id']} | Bat: {v['bateria']}% | Potência: 0kW | LED: VERMELHO (ESPERA)")
    print("="*40)

# Loop Principal
estado_anterior_btn = 0
gerenciar_recarga(cenarios_energia[indice_cenario]) # Chamada inicial

while True:
    estado_btn = btn_cenario.value()
    
    # Detecção de borda de subida (Debounce simples)
    if estado_btn == 1 and estado_anterior_btn == 0:
        indice_cenario = (indice_cenario + 1) % len(cenarios_energia)
        gerenciar_recarga(cenarios_energia[indice_cenario])
        time.sleep(0.3) # Evita saltos duplos
        
    estado_anterior_btn = estado_btn
    time.sleep(0.05)
