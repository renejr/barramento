import asyncio
import websockets
import struct
import random

async def simulate_triage_station():
    #uri = "ws://localhost:8080"  # Endereço do servidor WebSocket em PHP
    #async with websockets.connect(uri) as websocket:
        while True:
            # Simulando dados iniciais do paciente coletados na triagem
            temperature = random.uniform(36.0, 39.0)  # Temperatura corporal em Celsius
            systolic_bp = random.uniform(100, 180)  # Pressão arterial sistólica em mmHg
            diastolic_bp = random.uniform(60, 120)  # Pressão arterial diastólica em mmHg
            heart_rate = random.uniform(60, 100)  # Frequência cardíaca em bpm
            priority = random.randint(1, 5)  # Classificação de prioridade de atendimento (1 = emergência, 5 = baixa prioridade)

            # Convertendo dados para formato binário
            #data = struct.pack('ffffI', temperature, systolic_bp, diastolic_bp, heart_rate, priority)

            # Enviando dados de triagem para o servidor
            #await websocket.send(data)
            print(f"Enviado: Temp = {temperature:.2f}°C, PA Sistólica = {systolic_bp:.2f} mmHg, PA Diastólica = {diastolic_bp:.2f} mmHg, FC = {heart_rate:.2f} bpm, Prioridade = {priority}")

            # Aguardar 1 segundo antes de enviar novos dados
            await asyncio.sleep(1)

# Executando o simulador de Estação de Triagem
asyncio.run(simulate_triage_station())
