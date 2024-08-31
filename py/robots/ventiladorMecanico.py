import random
import time
import asyncio
import websockets
import struct
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer

class VentiladorSimulator(QObject):
    data_updated = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.timer = None  # Inicialmente, o timer é None
        self.is_running = False

    def setup_timer(self):
        self.timer = QTimer(self)  # Crie o timer aqui
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.generate_data)

    def start(self):
        if self.timer is None:
            self.setup_timer()  # Configura o timer somente quando necessário
        self.is_running = True
        self.timer.start()  # Inicie o timer aqui

    def stop(self):
        self.is_running = False
        if self.timer is not None:
            self.timer.stop()

    async def send_data_websocket(self, data):
        device = 'VM'  # Define o nome do dispositivo
        uri = "ws://localhost:8080"
        async with websockets.connect(uri) as websocket:
            # Calcula o tamanho da string do device CORRIGIDO
            device_size = len(device)  
            # Define o formato incluindo o tamanho do device
            data_format = f'{device_size}sffff{len(data[5])}s{len(data[6])}sQ'  
            data_bin = struct.pack(data_format, *data)
            await websocket.send(data_bin)

    def generate_data(self):
        if not self.is_running:
            return
        
        respiratory_rate = random.uniform(10, 30)
        tidal_volume = random.uniform(300, 600)
        inspiratory_pressure = random.uniform(10, 40)
        fio2 = random.uniform(0.21, 1.0)
        ventilation_mode = random.choice(["VCV", "PCV", "PSV"])
        device = 'VM'  # Define o nome do dispositivo

        alarms = []
        if respiratory_rate > 25:
            alarms.append("FR Alta")
        if respiratory_rate < 8:
            alarms.append("FR Baixa")
        if tidal_volume > 700:
            alarms.append("VC Alto")
        if inspiratory_pressure > 35:
            alarms.append("PIns Alta")
        if inspiratory_pressure < 5:
            alarms.append("PIns Baixa")

        alarm_string = ', '.join(alarms) if alarms else "Sem Alarmes"

        microtimestamp = int(time.time() * 1000)

        asyncio.run(self.send_data_websocket((
                                            device.encode('utf-8'), # Inclui o device no envio
                                            respiratory_rate,
                                            tidal_volume,
                                            inspiratory_pressure,
                                            fio2,
                                            ventilation_mode.encode('utf-8'),
                                            alarm_string.encode('utf-8'),
                                            microtimestamp)))

        self.data_updated.emit((respiratory_rate,
                                tidal_volume,
                                inspiratory_pressure,
                                fio2,
                                ventilation_mode,
                                alarm_string,
                                microtimestamp))
