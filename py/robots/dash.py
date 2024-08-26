from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import asyncio
import websockets
import struct

app = Flask(__name__)
socketio = SocketIO(app)

# Simulação de Dados Recebidos de Equipamentos Médicos
async def receive_data_from_equipment():
    uri = "ws://localhost:8080"  # Endereço do servidor WebSocket em PHP
    async with websockets.connect(uri) as websocket:
        while True:
            data = await websocket.recv()
            # Decodifica os dados recebidos
            temperature, systolic_bp, diastolic_bp, heart_rate, priority = struct.unpack('ffffI', data)
            
            # Envia os dados para o cliente conectado via SocketIO
            socketio.emit('update_data', {
                'temperature': temperature,
                'systolic_bp': systolic_bp,
                'diastolic_bp': diastolic_bp,
                'heart_rate': heart_rate,
                'priority': priority
            })

            await asyncio.sleep(1)

# Inicializa a tarefa assíncrona para receber dados
def start_asyncio_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(receive_data_from_equipment())

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=start_asyncio_loop, args=(loop,))
    t.start()
    socketio.run(app, debug=True)
