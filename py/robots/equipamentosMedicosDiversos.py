import asyncio
import websockets
import struct
import random

async def simulate_medical_equipment():
    #uri = "ws://localhost:8080"  # Endereço do servidor WebSocket em PHP
    #async with websockets.connect(uri) as websocket:
        while True:
            # Simulando dados específicos do equipamento (Exemplo: Dispositivo de Raios X)
            operation_status = random.choice([0, 1])  # 0 = Inativo, 1 = Ativo
            exposure_time = random.uniform(0.1, 2.0) if operation_status == 1 else 0.0  # Tempo de exposição em segundos
            image_quality = random.uniform(70, 100) if operation_status == 1 else 0  # Qualidade da imagem de 0 a 100
            alarm_code = random.choice([0, 101, 102])  # 0 = Sem alarme, 101 = Falha técnica, 102 = Manutenção necessária
            
            # Convertendo dados para formato binário
            #data = struct.pack('fIfI', operation_status, exposure_time, int(image_quality), alarm_code)

            data = {
                    'operation_status': operation_status,
                    'exposure_time': exposure_time,
                '   image_quality': image_quality,
                '   alarm_code': alarm_code}
            
            print(data)

            # Enviando dados de telemetria para o servidor
            #await websocket.send(data)
            #print(f"Enviado: Status de Operação = {operation_status}, Tempo de Exposição = {exposure_time:.2f}s, Qualidade da Imagem = {image_quality}, Código de Alarme = {alarm_code}")

            # Aguardar 1 segundo antes de enviar novos dados
            await asyncio.sleep(1)

# Executando o simulador de Equipamentos Médicos Diversos
asyncio.run(simulate_medical_equipment())
