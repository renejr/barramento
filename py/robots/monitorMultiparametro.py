import asyncio
import random
from PyQt5.QtCore import QObject, pyqtSignal

class MonitorSimulator(QObject):  # Herdando de QObject para usar sinais
    data_updated = pyqtSignal(dict)  # Sinal para enviar os dados

    def __init__(self):
        super().__init__()
        self.is_running = False

    async def simulate(self):
        while self.is_running:
            # Simulando sinais vitais:
            heart_rate = random.uniform(50, 110)
            systolic_bp = random.uniform(80, 150)
            diastolic_bp = random.uniform(50, 100)
            oxygen_saturation = random.uniform(90, 100)
            body_temperature = random.uniform(35.0, 38.0)
            respiratory_rate = random.uniform(10, 25)

            data = {
                "heart_rate": heart_rate,
                "systolic_bp": systolic_bp,
                "diastolic_bp": diastolic_bp,
                "oxygen_saturation": oxygen_saturation,
                "body_temperature": body_temperature,
                "respiratory_rate": respiratory_rate
            }

            # Emitindo o sinal com os dados
            self.data_updated.emit(data) 

            await asyncio.sleep(1)

    def start(self):
        self.is_running = True
        asyncio.run(self.simulate())

    def stop(self):
        self.is_running = False
