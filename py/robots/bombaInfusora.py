import asyncio
import websockets
import struct
import random

async def simulate_infusion_pump():
        total_volume_administered = 0  # Volume total administrado em mL
        infusion_active = True  # Status inicial da infusão (ativa ou inativa)
        infusion_rate = random.uniform(1, 10)  # Taxa de infusão inicial em mL/h

        while True:
            if infusion_active:
                # Simulando a administração de medicamento
                infusion_rate = random.uniform(1, 10)  # Taxa de infusão atual em mL/h
                volume_administered = infusion_rate / 60  # Volume administrado por minuto
                total_volume_administered += volume_administered
                
                # Simulando status e alarmes
                status = 0  # 0 = Normal, 1 = Oclusão, 2 = Fim de Infusão, 3 = Falha
                if random.random() < 0.01:
                    status = random.choice([1, 2, 3])  # Simular um alarme ocasionalmente

                    data = {
                        'infusion_rate': infusion_rate,
                        'volume_administered': volume_administered,
                        'total_volume_administered': total_volume_administered,
                        'status': status}
                
                # Enviando dados de telemetria para o servidor
                print(f"Enviado: Taxa de Infusão = {infusion_rate:.2f} mL/h, Volume Total Administrado = {total_volume_administered:.2f} mL, Status = {status}")

            # Aguardando comandos ou alterações (simulação apenas de envio neste momento)
            await asyncio.sleep(1)

# Executando o simulador de Bomba Infusora
asyncio.run(simulate_infusion_pump())
