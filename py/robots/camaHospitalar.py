import asyncio
import websockets
import struct
import random

async def simulate_hospital_bed():
        while True:
            # Simulando a posição da cama
            bed_inclination = random.uniform(0, 45)  # Inclinação da cama em graus (0 a 45)
            head_elevation = random.uniform(0, 30)  # Elevação da cabeça em graus (0 a 30)
            patient_weight = random.uniform(50, 150)  # Peso do paciente em kg

            # Simulando alarmes (0 = sem alarme, 1 = saída não autorizada)
            alarm = 0
            if random.random() < 0.05:  # 5% de chance de alarme de saída
                alarm = 1

            # Convertendo dados para formato binário
            # data = struct.pack('fffI', bed_inclination, head_elevation, patient_weight, alarm)

            data = {
                'bed_inclination': bed_inclination,
                'head_elevation': head_elevation,
                'patient_weight': patient_weight,
                'alarm': alarm
            }

            # Enviando dados de telemetria para o servidor
            print(f"Enviado: Inclinação = {bed_inclination:.2f}°, Elevação Cabeça = {head_elevation:.2f}°, Peso Paciente = {patient_weight:.2f} kg, Alarme = {alarm}")

            # Aguardar 1 segundo antes de enviar novos dados
            await asyncio.sleep(1)

# Executando o simulador de Camas Hospitalares
asyncio.run(simulate_hospital_bed())
