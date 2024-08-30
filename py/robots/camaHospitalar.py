import asyncio
import websockets
import struct
from   vpython import *
import random
import time

# --- Configuração da Janela e Canvas ---
scene = canvas(width=1280, height=600, background=color.white) 
scene.title = "Simulador de Cama Hospitalar"  # Define o título da janela

# --- Barra de Navegação ---
navbar_height = 50
navbar = box(pos=vector(0, scene.height/2 + navbar_height/2, 0), 
              size=vector(scene.width, navbar_height, 0), 
              color=color.gray(0.8))

"""
Simulates a hospital bed by generating random data for bed inclination, head elevation, patient weight, and alarm status.

The function runs indefinitely, generating new data every second. The data is then printed to the console.

Parameters:
None

Returns:
None
"""

# --- Botões ---
button_width = 100
button_height = 30
button_color = color.blue

# Função auxiliar para criar botões
def create_button(text, pos):
    button = box(pos=pos, size=vector(button_width, button_height, 0), color=button_color)
    label(pos=pos, text=text, color=color.white, height=16, box=False)
    return button

# Criando os botões da navbar
button_start = create_button("INICIAR", pos=vector(-3*button_width, scene.height/2 + navbar_height/2, 0))
button_stop = create_button("PARAR", pos=vector(-1*button_width, scene.height/2 + navbar_height/2, 0))
button_capture = create_button("CAPTURAR", pos=vector(button_width, scene.height/2 + navbar_height/2, 0))
button_transmit = create_button("TRANSMITIR", pos=vector(3*button_width, scene.height/2 + navbar_height/2, 0))
button_exit = create_button("SAIR", pos=vector(5*button_width, scene.height/2 + navbar_height/2, 0))

# --- Funções para lidar com os eventos dos botões (ainda a serem implementadas) ---
def handle_start():
    # Implemente a lógica para iniciar a simulação
    pass  

def handle_stop():
    # Implemente a lógica para parar a simulação
    pass

def handle_capture():
    # Implemente a lógica para capturar dados
    pass

def handle_transmit():
    # Implemente a lógica para transmitir dados
    pass

def handle_exit():
    # Implemente a lógica para sair da aplicação
    exit()

async def simulate_hospital_bed():
    # Criando a cama
    base = box(pos=vector(0, -1, 0), size=vector(5, 1, 3), color=color.gray(0.7))
    # Criando o colchão
    colchao = box(pos=vector(0, -0.5, 0), size=vector(4.8, 0.8, 2.8), color=color.blue)

    # Labels para as dimensões
    comprimento_label = label(pos=colchao.pos + vector(2.4, 0, 0), text="Comprimento: 4.8",  xoffset=10, yoffset=50, space=10, height=16, border=4, font='sans')
    altura_label = label(pos=colchao.pos + vector(0, 0.4, 0), text="Altura: 0.8", xoffset=10, yoffset=70, space=10, height=16, border=4, font='sans')
    largura_label = label(pos=colchao.pos + vector(0, 0, 1.4), text="Largura: 2.8", xoffset=10, yoffset=90, space=10, height=16, border=4, font='sans')


    # Posição inicial da cabeceira (acima da largura do colchão)
    #cabec_pos_inicial = vector(4.4, 0.4, 1.4)  # Ajustada para o topo do colchão
    #cabec = box(pos=colchao.pos + cabec_pos_inicial , size=vector(2.4, 1, 0.2), color=color.orange)

    #cabec = box(pos=vector(0, 0.5, -1.3), size=vector(4.8, 1, 0.2), color=color.orange)

    while True:
        # ... (Atualizações da simulação) ...

        # Verificação de eventos dos botões (ainda a ser implementada)
        # ...
        while True:
            # Simulando a posição da cama
            bed_inclination = random.uniform(0, 45)  # Inclinação da cama em graus (0 a 45)
            head_elevation = 28 #random.uniform(0, 30)  # Elevação da cabeça em graus (0 a 30)
            patient_weight = random.uniform(50, 150)  # Peso do paciente em kg

            # Simulando alarmes (0 = sem alarme, 1 = saída não autorizada)
            alarm = 0
            if random.random() < 0.05:  # 5% de chance de alarme de saída
                alarm = 1

            # Convertendo dados para formato binário
            dataBin = struct.pack('fffI', bed_inclination, head_elevation, patient_weight, alarm)

            data = {
                'bed_inclination': bed_inclination,
                'head_elevation': head_elevation,
                'patient_weight': patient_weight,
                'alarm': alarm
            }

            # Calcular o ângulo de rotação em relação à posição inicial
            #angulo_rotacao = radians(data['head_elevation']) 

            # Rotacionar a cabeceira em relação à sua posição inicial
            #cabec.rotate(angle=angulo_rotacao, axis=vector(1, 0, 0), origin=cabec_pos_inicial)

            print(dataBin.hex())
            print(data)
            
            #time.sleep(0.1)  # Pequena pausa para visualização
            
            # Enviando dados de telemetria para o servidor
            #print(f"Enviado: Inclinação = {bed_inclination:.2f}°, Elevação Cabeça = {head_elevation:.2f}°, Peso Paciente = {patient_weight:.2f} kg, Alarme = {alarm}")

            # Aguardar 1 segundo antes de enviar novos dados
            await asyncio.sleep(1)

# Executando o simulador de Camas Hospitalares
asyncio.run(simulate_hospital_bed())
