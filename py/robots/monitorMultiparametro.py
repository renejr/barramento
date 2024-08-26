import asyncio
import websockets
import struct
import random

async def simulate_multi_parameter_monitor():
    while True:
        # Simulando sinais vitais:
        heart_rate = random.uniform(60, 100)  # Frequência cardíaca em bpm
        systolic_bp = random.uniform(100, 140)  # Pressão arterial sistólica em mmHg
        diastolic_bp = random.uniform(60, 90)  # Pressão arterial diastólica em mmHg
        oxygen_saturation = random.uniform(95, 100)  # Saturação de oxigênio em %
        body_temperature = random.uniform(36.5, 37.5)  # Temperatura corporal em Celsius
        respiratory_rate = random.uniform(12, 20)  # Frequência respiratória em rpm

        data = {
            "heart_rate": heart_rate,
            "systolic_bp": systolic_bp,
            "diastolic_bp": diastolic_bp,
            "oxygen_saturation": oxygen_saturation,
            "body_temperature": body_temperature,
            "respiratory_rate": respiratory_rate
        }

        print(data)

        # print(f"Enviado: FC = {heart_rate:.2f} bpm, PA Sistólica = {systolic_bp:.2f} mmHg, PA Diastólica = {diastolic_bp:.2f} mmHg, Sat. O2 = {oxygen_saturation:.2f}%, Temp. = {body_temperature:.2f}°C, FR = {respiratory_rate:.2f} rpm")

        # Aguardar 1 segundo antes de enviar novos dados
        await asyncio.sleep(1)

# Executando o simulador de Monitor Multiparâmetro
asyncio.run(simulate_multi_parameter_monitor())
