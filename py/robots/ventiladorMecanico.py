import asyncio
import websockets
import struct
import random
import time

async def simulate_ventilator():
    while True:
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

        alarm_string = ', '.join(alarms) if alarms else "Sem Alarmes"
        alarm_bytes = alarm_string.encode('utf-8')
        alarm_size = len(alarm_bytes)

        # -- Microtimestamp --
        microtimestamp = int(time.time() * 1000) # Tempo em milissegundos desde 1 de janeiro de 1970

        # -- Empacotamento de Dados --
        dataBin = struct.pack(f'ffffsI{alarm_size}sQ', 
                             respiratory_rate, 
                             tidal_volume, 
                             inspiratory_pressure, 
                             fio2, 
                             ventilation_mode.encode('utf-8'),
                             alarm_size,
                             alarm_bytes,
                             microtimestamp)
        
        data = {
            'respiratory_rate': respiratory_rate,
            'tidal_volume': tidal_volume,
            'inspiratory_pressure': inspiratory_pressure,
            'fio2': fio2,
            'ventilation_mode': ventilation_mode,
            'alarms': alarm_string,
            'timestamp': microtimestamp 
        }

        print(data)
        print(f"Enviado: {dataBin.hex()}")
        
        await asyncio.sleep(1)

asyncio.run(simulate_ventilator())
