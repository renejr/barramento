import asyncio
import random
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

class MonitorSimulator(QObject):
    data_updated = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.is_running = False
        self.timer = None

    def simulate_data(self):
        if not self.is_running:
            return

        # Simulando sinais vitais:
        heart_rate = random.uniform(45, 150)
        systolic_bp = random.uniform(50, 200)
        diastolic_bp = random.uniform(40, 150)
        oxygen_saturation = random.uniform(50, 150)
        body_temperature = random.uniform(34.0, 39.0)
        respiratory_rate = random.uniform(8, 28)

        data = {
            "heart_rate": heart_rate,
            "systolic_bp": systolic_bp,
            "diastolic_bp": diastolic_bp,
            "oxygen_saturation": oxygen_saturation,
            "body_temperature": body_temperature,
            "respiratory_rate": respiratory_rate
        }

        self.data_updated.emit(data)

        # Use a timer to call this method again after 1 second
        self.timer = QTimer()
        self.timer.timeout.connect(self.simulate_data)
        self.timer.setSingleShot(True)  # Ensure it runs only once
        self.timer.start(1000)  # 1000 milliseconds = 1 second

    def start(self):
        self.is_running = True
        self.simulate_data()

    def stop(self):
        self.is_running = False
        if self.timer:
            self.timer.stop()
