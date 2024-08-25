import curses
import asyncio
import websockets
import struct
import threading

# Inicializa as variáveis globais para armazenar os dados de cada equipamento
equipment_data = {
    "Monitores Multiparâmetros": "",
    "Bombas Infusoras": "",
    "Camas Hospitalares": "",
    "Estação de Triagem": "",
    "Equipamentos Médicos Diversos": "",
}
alerts = []

async def receive_data_from_equipment():
    #uri = "ws://localhost:8080"  # Endereço do servidor WebSocket em PHP
    #async with websockets.connect(uri) as websocket:
        while True:
            #data = await websocket.recv()
            # Exemplo de decodificação de dados - ajuste conforme o formato binário real
            equipment_type, temperature, systolic_bp, diastolic_bp, heart_rate, alarm = struct.unpack('IffffI', data)
            
            # Atualiza os dados de acordo com o tipo de equipamento
            if equipment_type == 1:
                equipment_data["Monitores Multiparâmetros"] = f"Temp: {temperature:.1f}°C, PA Sistólica: {systolic_bp:.0f}, PA Diastólica: {diastolic_bp:.0f}, FC: {heart_rate:.0f} bpm"
                if alarm > 0:
                    alerts.append(f"Alarme do Monitor Multiparâmetro: Código {alarm}")
            elif equipment_type == 2:
                equipment_data["Bombas Infusoras"] = f"Taxa de Infusão: {temperature:.1f} mL/h, Volume Total: {systolic_bp:.1f} mL, Status: {'Ok' if alarm == 0 else 'Falha'}"
                if alarm > 0:
                    alerts.append(f"Alarme da Bomba Infusora: Código {alarm}")
            elif equipment_type == 3:
                equipment_data["Camas Hospitalares"] = f"Posição da Cabeça: {temperature:.0f}°, Peso do Paciente: {systolic_bp:.1f} kg"
                if alarm > 0:
                    alerts.append(f"Alarme da Cama Hospitalar: Código {alarm}")
            elif equipment_type == 4:
                equipment_data["Estação de Triagem"] = f"Temp: {temperature:.1f}°C, PA: {systolic_bp:.0f}/{diastolic_bp:.0f}, FC: {heart_rate:.0f} bpm, Prioridade: {alarm}"
                if alarm > 0:
                    alerts.append(f"Alarme da Estação de Triagem: Código {alarm}")
            elif equipment_type == 5:
                equipment_data["Equipamentos Médicos Diversos"] = f"Status: {'Ativo' if temperature > 0 else 'Inativo'}, Código de Alarme: {alarm}"
                if alarm > 0:
                    alerts.append(f"Alarme do Equipamento Diverso: Código {alarm}")

            await asyncio.sleep(1)

def start_asyncio_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(receive_data_from_equipment())

def draw_interface(stdscr):
    curses.curs_set(0)  # Desativa o cursor

    current_tab = 0
    tabs = list(equipment_data.keys())

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Desenha o cabeçalho
        stdscr.addstr(0, 0, "Monitoramento de Equipamentos Médicos", curses.A_BOLD)
        stdscr.addstr(1, 0, "Pressione 'q' para sair, 'a' e 'd' para mudar de aba", curses.A_DIM)

        # Desenha as abas
        tab_str = " | ".join(tabs)
        stdscr.addstr(2, 0, tab_str)

        # Desenha os dados da aba atual
        stdscr.addstr(4, 0, f"Dados de {tabs[current_tab]}:", curses.A_UNDERLINE)
        stdscr.addstr(5, 0, equipment_data[tabs[current_tab]])

        # Desenha a área de alerta
        stdscr.addstr(7, 0, "Alertas Atuais:", curses.A_BOLD)
        for i, alert in enumerate(alerts[-5:]):  # Mostra apenas os 5 últimos alertas
            stdscr.addstr(8 + i, 0, f"- {alert}")

        stdscr.refresh()

        # Processa entrada do usuário para mudar de aba ou sair
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('a'):
            current_tab = (current_tab - 1) % len(tabs)
        elif key == ord('d'):
            current_tab = (current_tab + 1) % len(tabs)

def main():
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=start_asyncio_loop, args=(loop,))
    t.start()

    curses.wrapper(draw_interface)

if __name__ == '__main__':
    main()
