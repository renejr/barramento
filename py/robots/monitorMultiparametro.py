import asyncio
import random
import websockets
import struct
import pymysql  # Importe o pymysql
from datetime import datetime  # Importe datetime
import time
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

class MonitorSimulator(QObject):
    data_updated = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.is_running = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.simulate_data)
        self.timer.start(1000)  # Inicia o timer aqui

    def connect_to_db(self):
        # Conexão com o banco de dados
        self.mydb = pymysql.connect(
            host="localhost",
            port=3307,
            user="root",
            password="",
            database="barramento"
        )
        self.cursor = self.mydb.cursor()

    def get_device_id(self):
        # Busco o ID do dispositivo
        sql = "SELECT id FROM equipamentos WHERE sigla = 'MM' LIMIT 1"
        self.cursor.execute(sql)
        device_id = self.cursor.fetchone()[0]
        return device_id

    def insert_data(self, device_id, data, formatted_timestamp):
        # Query de inserção
        sql = "INSERT INTO telemetria (equipamentoID, timestamp, device, DATA) VALUES (%s, %s, %s, JSON_OBJECT('hr', %s, 'sys', %s, 'dia', %s, 'spo2', %s, 'temp', %s, 'rr', %s, 'timestamp', %s))"
        self.cursor.execute(sql, (device_id, formatted_timestamp, data['device'], data['heart_rate'], data['systolic_bp'], data['diastolic_bp'], data['oxygen_saturation'], data['body_temperature'], data['respiratory_rate'], data['timestamp']))
        self.mydb.commit()

    # def start(self):
    #     self.is_running = True

    def stop(self):
        self.timer.stop()
        self.is_running = False        

    def simulate_data(self):
        if not self.is_running:
            return

        # Simulação de dados
        heart_rate = random.uniform(45, 150)
        systolic_bp = random.uniform(50, 200)
        diastolic_bp = random.uniform(40, 150)
        oxygen_saturation = random.uniform(50, 150)
        body_temperature = random.uniform(34.0, 39.0)
        respiratory_rate = random.uniform(8, 28)
        device = 'MM'  # Nome do dispositivo

        microtimestamp = int(time.time() * 1000)

        # Convert microtimestamp to seconds
        timestamp_seconds = microtimestamp / 1000

        # Convert to datetime object
        datetime_object = datetime.fromtimestamp(timestamp_seconds)

        # Format datetime object for MySQL
        formatted_timestamp = datetime_object.strftime('%Y-%m-%d %H:%M:%S')

        # Dados simulados
        data = {
            'device': device,
            'timestamp': time.time(),
            'heart_rate': heart_rate,
            'systolic_bp': systolic_bp,
            'diastolic_bp': diastolic_bp,
            'oxygen_saturation': oxygen_saturation,
            'body_temperature': body_temperature,
            'respiratory_rate': respiratory_rate
        }

        # Chamando o método format_data_binary
        data_bin = self.format_data_binary(data)
        # print(f"Hexadecimal: {data_bin.hex()}")

        # Conecte-se ao banco de dados
        self.connect_to_db()

        # Obtenha o ID do dispositivo
        device_id = self.get_device_id()

        # Insira os dados no banco de dados
        self.insert_data(device_id, data, formatted_timestamp)

        # Feche a conexão com o banco de dados (opcional, mas recomendado)
        self.cursor.close()
        self.mydb.close()

        # Emitindo os dados simulados para quem estiver conectado ao sinal
        self.data_updated.emit(data)

    def format_data_binary(self, data):
        # print(data)

        # Simulação de dados
        device_name = data['device'].encode('utf-8')[:2]  # Truncating to ensure 2 bytes

        data_format = f'2s d 6f'  # Device name (2 bytes), timestamp (double), and 6 floats

        # print(data_format)
        # print(device_name)
        # print(data['timestamp'])
        timestamp = data['timestamp'] / 1000
        # print(timestamp)
        # print(float(timestamp))
        heart_rate = data['heart_rate'] / 100
        # print(heart_rate)
        systolic_bp = data['systolic_bp'] / 100
        # print(systolic_bp)
        diastolic_bp = data['diastolic_bp'] / 100
        # print(diastolic_bp)
        oxygen_saturation = data['oxygen_saturation'] / 100
        # print(oxygen_saturation)
        body_temperature = data['body_temperature'] / 100
        # print(body_temperature)
        respiratory_rate = data['respiratory_rate'] / 100
        # print(respiratory_rate)

        data_bin = struct.pack(data_format,
                                device_name,  # device_name  # 2 bytes for device name
                                timestamp,  # float(timestamp),  # Timestamp converted to float
                                heart_rate,
                                systolic_bp,
                                diastolic_bp,
                                oxygen_saturation,
                                body_temperature,
                                respiratory_rate
                                )

        # print(data_bin)
        # print(data_bin.hex())

        return data_bin

        def get_device_id(self):
            # Busco o ID do dispositivo
            sql = "SELECT id FROM equipamentos WHERE sigla = 'MM' LIMIT 1"
            self.cursor.execute(sql)
            device_id = self.cursor.fetchone()[0]
            return device_id

        def insert_data(self, device_id, data, formatted_timestamp):
            # Query de inserção
            sql = "INSERT INTO telemetria (equipamentoID, timestamp, device, DATA) VALUES (%s, %s, %s, JSON_OBJECT('hr', %s, 'sys', %s, 'dia', %s, 'spo2', %s, 'temp', %s, 'rr', %s, 'timestamp', %s))"
            self.cursor.execute(sql, (device_id, formatted_timestamp, data['device'], data['heart_rate'], data['systolic_bp'], data['diastolic_bp'], data['oxygen_saturation'], data['body_temperature'], data['respiratory_rate'], data['timestamp']))
            self.mydb.commit()


        def start(self):
            self.is_running = True

        def stop(self):
            self.is_running = False

