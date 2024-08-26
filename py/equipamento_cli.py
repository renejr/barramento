
import websockets
import struct
import random
import curses
import asyncio
import threading
from robots import (
    simulate_multi_parameter_monitor,
    simulate_infusion_pump,
    simulate_hospital_bed,
    simulate_triage_station,
    simulate_medical_equipment,
    simulate_ventilator,
)

# Inicializa as variáveis globais para armazenar os dados de cada equipamento
equipment_data = {
    "Monitores Multiparâmetros": "",
    "Bombas Infusoras": "",
    "Camas Hospitalares": "",
    "Estação de Triagem": "",
    "Equipamentos Médicos Diversos": "",
    "Ventilador Mecânico": "",
}
alerts = []

# Função para atualizar os dados de telemetria dos robôs
async def update_equipment_data():
    while True:
        # Atualiza os dados de cada robô
        equipment_data["Monitores Multiparâmetros"] = await simulate_multi_parameter_monitor()
        equipment_data["Bombas Infusoras"] = await simulate_infusion_pump()
        equipment_data["Camas Hospitalares"] = await simulate_hospital_bed()
        equipment_data["Estação de Triagem"] = await simulate_triage_station()
        equipment_data["Equipamentos Médicos Diversos"] = await simulate_medical_equipment()
        equipment_data["Ventilador Mecânico"] = await simulate_ventilator()

        # Aguarda 1 segundo antes de atualizar novamente
        await asyncio.sleep(1)

# Função para desenhar a interface gráfica
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

# Função principal
def main():
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=start_asyncio_loop, args=(loop,))
    t.start()

    curses.wrapper(draw_interface)

# Função para iniciar o loop assíncrono
def start_asyncio_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(update_equipment_data())

if __name__ == '__main__':
    main()
