import asyncio
import websockets
import struct
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QCoreApplication
import sys
import time
import random

class simulate_triage_station(QObject):
    data_updated = pyqtSignal(tuple)
   
    def __init__(self):
        super().__init__()
        self.timer = None
        self.is_running = False

    def setup_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.generate_and_send_data)
        self.timer.setInterval(1000)  # 1 second

    def start(self):
        if self.timer is None:
            self.setup_timer()
        self.is_running = True
        self.timer.start()

    def stop(self):
        self.is_running = False
        if self.timer is not None:
            self.timer.stop()

    def format_data_binary(self, data):
        # Simulating patient data collected during triage
        device_name = data['device'].encode('utf-8')[:2]  # Truncate to 2 bytes
        data_format = '2s d 6f'  # 2 bytes device name, double for timestamp, 6 floats
        timestamp = data['timestamp'] / 1000
        heart_rate = data['hr'] / 100
        systolic_bp = data['sys'] / 100
        diastolic_bp = data['dia'] / 100
        oxygen_saturation = 98 / 100  # Default value as 'spo2' is missing
        body_temperature = data['temp'] / 100
        respiratory_rate = 16 / 100  # Default value as 'rr' is missing

        data_bin = struct.pack(data_format,
                               device_name, timestamp, heart_rate,
                               systolic_bp, diastolic_bp, oxygen_saturation,
                               body_temperature, respiratory_rate)
        return data_bin

    async def send_data_to_websocket(self, data):
        async with websockets.connect('ws://localhost:8080') as websocket:
            await websocket.send(data)
            print("Data sent to WebSocket server")

    def generate_and_send_data(self):
        # Example data
        data = {
            'device': 'HRM',  # Heart rate monitor device
            'timestamp': time.time() * 1000,
            'hr': random.uniform(60, 100),
            'sys': random.uniform(120, 140),
            'dia': random.uniform(80, 90),
            'temp': random.uniform(36, 38)
        }
        binary_data = self.format_data_binary(data)

        # Run asyncio task using asyncio.run
        asyncio.run(self.send_data_to_websocket(binary_data))

if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    
    # Create an instance of the simulation class
    station = simulate_triage_station()
    
    # Start the simulation
    station.start()
    
    # Run the event loop
    sys.exit(app.exec_())
