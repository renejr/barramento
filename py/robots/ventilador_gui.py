import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QObject
import pyqtgraph as pg

from ventiladorMecanico import VentiladorSimulator  # Importe a classe do simulador

class Worker(QObject):
    data_updated = pyqtSignal(tuple)
    start_simulator = pyqtSignal()
    stop_simulator = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.simulator = VentiladorSimulator()
        self.simulator.data_updated.connect(self.data_updated.emit)
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.simulator.generate_data)
        self.start_simulator.connect(self.start)
        self.stop_simulator.connect(self.stop)

    def start(self):
        self.simulator.is_running = True
        self.timer.start()

    def stop(self):
        self.simulator.is_running = False
        self.timer.stop()


class VentiladorGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simulador de Ventilador Mecânico")
        self.setGeometry(0, 0, 1366, 1024)  # Define a resolução da janela

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.simulator_thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.simulator_thread)
        self.worker.data_updated.connect(self.update_data)
        self.simulator_thread.start()

        self.paused = False  # Variável de controle de pausa

        self.init_ui()

    def init_ui(self):
        # Layout principal (Grid)
        grid_layout = QGridLayout(self.central_widget)

        # -- Barra de Navegação --
        self.create_navbar(grid_layout)

        # -- Gráficos --
        self.create_graphs(grid_layout)

        # -- Caixa de Alarmes --
        self.create_alarm_box(grid_layout)

    def create_navbar(self, layout):
        navbar_layout = QHBoxLayout()

        self.btn_start = QPushButton("Iniciar")
        self.btn_start.clicked.connect(self.start_simulation)
        navbar_layout.addWidget(self.btn_start)

        self.btn_pause = QPushButton("Pausar")
        self.btn_pause.clicked.connect(self.pause_simulation)
        self.btn_pause.setEnabled(False)  # Começa desabilitado
        navbar_layout.addWidget(self.btn_pause)

        self.btn_gravar = QPushButton("Gravar")
        navbar_layout.addWidget(self.btn_gravar)

        self.btn_stop = QPushButton("Parar")
        self.btn_stop.clicked.connect(self.stop_simulation)
        self.btn_stop.setEnabled(False)  # Começa desabilitado
        navbar_layout.addWidget(self.btn_stop)

        self.btn_exit = QPushButton("Sair")
        self.btn_exit.clicked.connect(self.close_application)
        navbar_layout.addWidget(self.btn_exit)

        self.btn_start.setStyleSheet("""
        QPushButton {
            background-color: lightgreen; 
            font-weight: bold; 
            color: black;
        }
        QPushButton:hover {
            background-color: darkgreen;
            font-weight: bold;
            color: white;
        }
        """)
        self.btn_pause.setStyleSheet("""
        QPushButton {
            background-color: lightblue; 
            font-weight: bold; 
            color: black;
        }
        QPushButton:hover {
            background-color: darkblue;
            font-weight: bold;
            color: white;
        }
        """)
        self.btn_gravar.setStyleSheet("""
        QPushButton {
            background-color: lightyellow; 
            font-weight: bold; 
            color: black;
        }
        QPushButton:hover {
            background-color: yellow;
            font-weight: bold;
            color: black;
        }
        """)
        self.btn_stop.setStyleSheet("""
        QPushButton {
            background-color: darkred; 
            font-weight: bold; 
            color: white;
        }
        QPushButton:hover {
            background-color: red;
            font-weight: bold;
            color: black;
        }
        """)
        self.btn_exit.setStyleSheet("""
        QPushButton {
            background-color: lightgray; 
            font-weight: bold; 
            color: black;
        }
        QPushButton:hover {
            background-color: darkgray;
            font-weight: bold;
            color: white;
        }
        """)

        layout.addLayout(navbar_layout, 0, 0, 1, 2)  # Adiciona a barra de navegação

    def create_graphs(self, layout):
        # Crie os gráficos usando pyqtgraph
        self.graph_widget = pg.GraphicsLayoutWidget()

        # Exemplo: gráfico de frequência respiratória
        self.plot_rr = self.graph_widget.addPlot(title="Frequência Respiratória (RR)", row=0, col=0)  # FR na linha 1, coluna 1
        self.curve_rr = self.plot_rr.plot(pen='b')  # Crie a curva AQUI!
        self.data_rr = []

        # -- Gráfico do Volume Corrente --
        self.plot_vc = self.graph_widget.addPlot(title="Volume Corrente (VC)", row=0, col=1)  # VC na linha 1, coluna 2
        self.curve_vc = self.plot_vc.plot(pen='r')  # Crie a curva do VC (vermelho)
        self.data_vc = []  # Lista para armazenar os dados do VC

        # -- Gráfico da Pressão Inspiratória --
        self.plot_pressure = self.graph_widget.addPlot(title="Pressão Inspiratória (PIns)", row=1, col=0)  # PIns na linha 2, coluna 1
        self.curve_pressure = self.plot_pressure.plot(pen='g')  # Crie a curva (verde)
        self.data_pressure = []  # Lista para armazenar os dados da pressão

        # -- Gráfico do FiO2 --
        self.plot_fio2 = self.graph_widget.addPlot(title="FiO2 (%)", row=1, col=1)  # FiO2 na linha 2, coluna 2
        self.curve_fio2 = self.plot_fio2.plot(pen='y')  # Crie a curva (amarelo)
        self.data_fio2 = []  # Lista para armazenar os dados do FiO2

        # Adicionando os gráficos ao layout em duas linhas:
        layout.addWidget(self.graph_widget, 1, 0, 2, 2)  # Gráficos ocupam 2 linhas e 2 colunas

    def create_alarm_box(self, layout):
        self.alarm_label = QLabel("Sem Alarmes")
        self.alarm_label.setStyleSheet("background-color: lightgreen; font-size: 16px; padding: 10px;")
        self.alarm_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.alarm_label, 3, 0, 1, 2)  # Caixa de alarmes na quarta linha

    def start_simulation(self):
        # Verifica se a thread já foi criada
        if not hasattr(self, 'simulator_thread'):
            print("Criando e iniciando a thread...")
            self.simulator_thread = QThread()
            self.worker = Worker()
            self.worker.moveToThread(self.simulator_thread)
            self.worker.data_updated.connect(self.update_data)
            self.simulator_thread.start()
            self.worker.start_simulator.emit()  # Emite o sinal para iniciar a simulação
        else:
            # Se a thread já existe, apenas emite o sinal para iniciar
            print("Thread já existe, iniciando a simulação...")
            self.worker.start_simulator.emit()

    # Limpa os dados dos gráficos antes de iniciar a simulação
        self.data_rr.clear() 
        self.data_vc.clear()
        self.data_pressure.clear()
        self.data_fio2.clear()

    # Atualiza os gráficos para mostrar que estão vazios
        self.curve_rr.setData(self.data_rr)
        self.curve_vc.setData(self.data_vc)
        self.curve_pressure.setData(self.data_pressure)
        self.curve_fio2.setData(self.data_fio2)

        self.btn_start.setEnabled(False)
        self.btn_pause.setEnabled(True)
        self.btn_stop.setEnabled(True)
        self.paused = False

    def stop_simulation(self):
        self.worker.stop_simulator.emit()  # Emite o sinal para parar a simulação
        if self.simulator_thread.isRunning():
            self.simulator_thread.quit()
            self.simulator_thread.wait()  # Aguarda a thread terminar

        self.btn_start.setEnabled(True)
        self.btn_pause.setEnabled(False)
        self.btn_stop.setEnabled(False)

    def pause_simulation(self):
        if not self.paused:
            self.worker.stop_simulator.emit()  # Emite o sinal para parar a simulação
            self.btn_pause.setText("Continuar")
            self.paused = True
        else:
            self.worker.start_simulator.emit()  # Emite o sinal para continuar a simulação
            self.btn_pause.setText("Pausar")
            self.paused = False

    def update_data(self, data):
        # Desempacota os dados recebidos
        respiratory_rate, tidal_volume, inspiratory_pressure, fio2, ventilation_mode, alarm_string, timestamp = data

        # Atualiza os gráficos
        self.data_rr.append(respiratory_rate)
        self.curve_rr.setData(self.data_rr)

        # Atualiza o gráfico do Volume Corrente
        self.data_vc.append(tidal_volume)
        self.curve_vc.setData(self.data_vc)

        # Atualiza o gráfico da Pressão Inspiratória
        self.data_pressure.append(inspiratory_pressure)
        self.curve_pressure.setData(self.data_pressure)

        # Atualiza o gráfico do FiO2
        self.data_fio2.append(fio2)
        self.curve_fio2.setData(self.data_fio2)

        # Atualiza a caixa de alarmes
        self.alarm_label.setText(alarm_string)
        if alarm_string != "Sem Alarmes":
            self.alarm_label.setStyleSheet("background-color: lightcoral; font-size: 16px; padding: 10px;")
        else:
            self.alarm_label.setStyleSheet("background-color: lightgreen; font-size: 16px; padding: 10px;")

    def close_application(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VentiladorGUI()
    window.show()
    sys.exit(app.exec_())
