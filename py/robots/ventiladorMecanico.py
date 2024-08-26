import asyncio
import websockets
import struct
import random

async def simulate_ventilator():
    while True:
        # Simulando dados de telemetria (por exemplo, frequência respiratória, volume corrente)
        respiratory_rate = random.uniform(10, 30)  # Simulando uma frequência respiratória
        tidal_volume = random.uniform(300, 600)  # Simulando um volume corrente em mL

        # data = struct.pack('fff', respiratory_rate, 0, tidal_volume)
        # print(f"Enviado: {data.hex()}")

        data = {
            'respiratory_rate': respiratory_rate,
            'tidal_volume': tidal_volume
        }

        print(data)
        
        #print(f"Enviado: Taxa de Respiração = {respiratory_rate:.2f}, Volume Corrente = {tidal_volume:.2f}")

        # Exibindo os dados de telemetria em tempo real
        #print(f"Frequência Respiratória = {respiratory_rate:.2f}, Volume Corrente = {tidal_volume:.2f} mL")

        # Aguardar 1 segundo antes de enviar novos dados
        await asyncio.sleep(1)

# Executando o simulador de ventilador mecânico
asyncio.run(simulate_ventilator())
