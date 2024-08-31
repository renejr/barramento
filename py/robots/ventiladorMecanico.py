import random
import time
import struct
from PyQt5.QtCore import QObject, pyqtSignal, QTimer  # Importe QTimer aqui

class VentiladorSimulator(QObject):
    data_updated = pyqtSignal(tuple)  # Sinal para enviar dados para a GUI

    def __init__(self):
        super().__init__()
        self.timer = QTimer()  # Agora você pode usar QTimer
        self.timer.setInterval(1000)  # Atualiza a cada 1 segundo
        self.timer.timeout.connect(self.generate_data)
        self.is_running = False

    def start(self):
        self.is_running = True
        self.timer.start()

    def stop(self):
        self.is_running = False
        self.timer.stop()

    def generate_data(self):
        if not self.is_running:
            return

        # -- Dados do Ventilador --
        respiratory_rate = random.uniform(10, 30)
        tidal_volume = random.uniform(300, 600)
        inspiratory_pressure = random.uniform(10, 40)
        fio2 = random.uniform(0.21, 1.0)
        ventilation_mode = random.choice(["VCV", "PCV", "PSV"])

        # -- Lógica de Alarmes --
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

        alarm_string = ', '.join(alarms) if alarms else "Sem Alarmes" # Mova esta linha para cá!

        # -- Microtimestamp --
        microtimestamp = int(time.time() * 1000)

        # -- Empacotamento de Dados (opcional) --
        # dataBin = struct.pack(f'ffffsI{alarm_size}sQ', 
        #                      respiratory_rate, 
        #                      tidal_volume, 
        #                      inspiratory_pressure, 
        #                      fio2, 
        #                      ventilation_mode.encode('utf-8'),
        #                      alarm_size,
        #                      alarm_bytes,
        #                      microtimestamp)

        # Envie os dados para a interface gráfica
        self.data_updated.emit((respiratory_rate, tidal_volume, inspiratory_pressure, fio2, ventilation_mode, alarm_string, microtimestamp))
