import asyncio
import random
import websockets
import struct
import pymysql
from datetime import datetime
import time
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QCoreApplication
import sys

class simulate_triage_station(QObject):
    data_updated = pyqtSignal(tuple)
   
    def __init__(self):
        super().__init__()
        self.timer = None
        self.is_running = False

    def setup_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.generate_data)
        self.timer.setInterval(1000)  # 1 segundo

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
        # Simulação de dados iniciais do paciente coletados na triagem
        device_name = data[0]['device'].encode('utf-8')[:2]  # Truncating to ensure 2 bytes
        data_format = f'2s d 6f'  # Device name (2 bytes), timestamp (double), and 6 floats
        timestamp = data[0]['data']['timestamp'] / 1000
        heart_rate = data[0]['data']['hr'] / 100
        systolic_bp = data[0]['data']['sys'] / 100
        diastolic_bp = data[0]['data']['dia'] / 100
        oxygen_saturation = 98 / 100  # Valor padrão, já que 'spo2' não está presente
        body_temperature = data[0]['data']['temp'] / 100
        respiratory_rate = 16 / 100  # Valor padrão, já que 'rr' não está presente

        data_bin = struct.pack(data_format,
                        device_name,  # 2 bytes for device name
                        timestamp,  # Timestamp converted to float
                        heart_rate,
                        systolic_bp,
                        diastolic_bp,
                        oxygen_saturation,
                        body_temperature,
                        respiratory_rate)
        
        return data_bin               

    def generate_data(self):
        if not self.is_running:
            return
       
        # Simulando dados iniciais do paciente coletados na triagem
        temperature = random.uniform(36.0, 39.0)
        systolic_bp = random.uniform(100, 180)
        diastolic_bp = random.uniform(60, 120)
        heart_rate = random.uniform(60, 100)
        priority = random.randint(1, 5)
        respiratory_rate = random.uniform(12, 20)  # Adicionando taxa respiratória
        device = 'ET'

        # Criar alarmes
        alarms = []
        if temperature > 38:
            alarms.append("Temperatura Alta")
        if temperature < 34:
            alarms.append("Temperatura Baixa")
        if systolic_bp > 120:
            alarms.append("Pressão Alta")
        if systolic_bp < 90:
            alarms.append("Pressão Baixa")
        if diastolic_bp > 80:
            alarms.append("Pressão Alta")
        if diastolic_bp < 60:
            alarms.append("Pressão Baixa")
        if heart_rate > 90:
            alarms.append("Frequência Alta")
        if heart_rate < 60:
            alarms.append("Frequência Baixa")
        if priority > 3:
            alarms.append("Prioridade Alta")
        if priority < 1:
            alarms.append("Prioridade Baixa")

        alarm_string = ', '.join(alarms) if alarms else "Sem Alarmes"
        microtimestamp = int(time.time() * 1000)
        timestamp_seconds = microtimestamp / 1000
        datetime_object = datetime.fromtimestamp(timestamp_seconds)
        formatted_timestamp = datetime_object.strftime('%Y-%m-%d %H:%M:%S')

        data_batch = [
        {'device': 'ET', 'data': {'temp': temperature, 'sys': systolic_bp, 'dia': diastolic_bp, 
                                  'hr': heart_rate, 'priority': priority, 'rr': respiratory_rate, 
                                  'alarms': alarm_string, 'timestamp': microtimestamp}}
        ]

        data_bin = self.format_data_binary(data_batch)
        print(f"Hexadecimal: {data_bin.hex()}")
   
        # Conexão com o banco de dados
        mydb = pymysql.connect(
            host="localhost",
            port=3307,
            user="root",
            password="",
            database="barramento"
        )
        cursor = mydb.cursor()

        # Busco o ID do dispositivo
        sql = "SELECT id FROM equipamentos WHERE sigla = 'ET' LIMIT 1"
        cursor.execute(sql)
        device_id = cursor.fetchone()[0]

        print(f'SQL: {sql}')
        print(f'Device ID: {device_id}')
        print(f'Data Batch: {data_batch}')

        # Query de inserção em lote
        sqlInsert = """
            INSERT INTO telemetria (equipamentoID, timestamp, device, DATA) 
            VALUES (%s, %s, %s, JSON_OBJECT('temp', %s, 'sys', %s, 'dia', %s, 'hr', %s, 'priority', %s, 'alarms', %s, 'timestamp', %s))
        """

        # Executar a inserção
        cursor.executemany(sqlInsert, [
            (str(device_id), formatted_timestamp, 'ET', 
            data['data']['temp'], data['data']['sys'], data['data']['dia'], 
            data['data']['hr'], data['data']['priority'], data['data']['alarms'], 
            data['data']['timestamp']) for data in data_batch
        ])

        print(f'SQL Insert: {sqlInsert}')

        mydb.commit()
        cursor.close()
        mydb.close()

        print("Dados inseridos com sucesso!")

        self.data_updated.emit((device, temperature, systolic_bp, diastolic_bp, heart_rate, priority))
        

    def format_data_binary(self, data):
        # Simulação de dados iniciais do paciente coletados na triagem
        device_name = data[0]['device'].encode('utf-8')[:2]  # Truncating to ensure 2 bytes
        data_format = f'2s d 6f'  # Device name (2 bytes), timestamp (double), and 6 floats
        timestamp = data[0]['data']['timestamp'] / 1000
        heart_rate = data[0]['data']['hr'] / 100
        systolic_bp = data[0]['data']['sys'] / 100
        diastolic_bp = data[0]['data']['dia'] / 100
        oxygen_saturation = 98 / 100  # Valor padrão, já que 'spo2' não está presente
        body_temperature = data[0]['data']['temp'] / 100
        respiratory_rate = 16 / 100  # Valor padrão, já que 'rr' não está presente

        data_bin = struct.pack(data_format,
                        device_name,  # 2 bytes for device name
                        timestamp,  # Timestamp converted to float
                        heart_rate,
                        systolic_bp,
                        diastolic_bp,
                        oxygen_saturation,
                        body_temperature,
                        respiratory_rate)
        
        return data_bin   



if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    
    # Criar uma instância da classe
    station = simulate_triage_station()
    
    # Iniciar a simulação
    station.start()
    
    # Executar o loop de eventos
    sys.exit(app.exec_())
