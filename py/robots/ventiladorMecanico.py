import random
import time
import asyncio
import websockets
import struct
import pymysql
from datetime import datetime
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

        # Convert microtimestamp to seconds
        timestamp_seconds = microtimestamp / 1000

        # Convert to datetime object
        datetime_object = datetime.fromtimestamp(timestamp_seconds)

        # Format datetime object for MySQL
        formatted_timestamp = datetime_object.strftime('%Y-%m-%d %H:%M:%S')

        # Dados de exemplo
        data_batch = [
            {'device': device, 'data': {'rr': respiratory_rate, 'vc': tidal_volume, 'pi': inspiratory_pressure, 'fio2': fio2, 'mode': ventilation_mode, 'alarms': alarm_string, 'timestamp': microtimestamp}},
        ]        

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
        sql = "SELECT id FROM equipamentos WHERE sigla = '" + device + "' LIMIT 1"
        cursor.execute(sql)
        device_id = cursor.fetchone()[0]

        # print('sql: ' + sql)

        # Query de inserção em lote
        sql = "INSERT INTO telemetria (equipamentoID, timestamp, device, DATA) VALUES (%s, %s, %s, JSON_OBJECT('rr', %s, 'vc', %s, 'pi', %s, 'fio2', %s, 'mode', %s, 'alarms', %s, 'timestamp', %s))"
        cursor.executemany(sql, [(device_id, formatted_timestamp, data['device'], data['data']['rr'], data['data']['vc'], data['data']['pi'], data['data']['fio2'], data['data']['mode'], data['data']['alarms'], data['data']['timestamp']) for data in data_batch])

        mydb.commit()
        cursor.close()
        mydb.close()

        print("Dados inseridos com sucesso!")

        # print(sql)

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
