import sys
import time
import struct
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import pyqtgraph as pg  # Importe o pyqtgraph para gráficos

from ventiladorMecanico import VentiladorSimulator  # Importe a classe do simulador

class VentiladorGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simulador de Ventilador Mecânico")
        self.setGeometry(0, 0, 1366, 1024)  # Define a resolução da janela

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.simulator = VentiladorSimulator()
        #self.simulator_thread = None

        self.paused = False  # Variável de controle de pausa
        self.simulator_thread = QThread()  # Crie a thread aqui
        self.simulator.moveToThread(self.simulator_thread)
        self.simulator_thread.started.connect(self.simulator.generate_data)
        self.simulator.data_updated.connect(self.update_data)

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

        self.btn_stop = QPushButton("Parar")
        self.btn_stop.clicked.connect(self.stop_simulation)
        self.btn_stop.setEnabled(False)  # Começa desabilitado
        navbar_layout.addWidget(self.btn_stop)

        self.btn_exit = QPushButton("Sair")
        self.btn_exit.clicked.connect(self.close_application)
        navbar_layout.addWidget(self.btn_exit)

        # ... (adicione botões para Gravar e Sair) ...

        layout.addLayout(navbar_layout, 0, 0, 1, 2)  # Adiciona a barra de navegação

    def create_graphs(self, layout):
        # Crie os gráficos usando pyqtgraph
        self.graph_widget = pg.GraphicsLayoutWidget()

        # Exemplo: gráfico de frequência respiratória
        self.plot_rr = self.graph_widget.addPlot(title="Frequência Respiratória (RR)")
        self.curve_rr = self.plot_rr.plot(pen='b')  # Crie a curva AQUI!
        self.data_rr = []

        # -- Box do Volume Corrente --
        self.vc_label = QLabel("VC: --")  # Inicializa com "--"
        self.vc_label.setStyleSheet("background-color: lightblue; font-size: 16px; padding: 10px;")
        self.vc_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.vc_label, 2, 0)  # Adiciona abaixo do gráfico de FR

        # ... (crie outros gráficos para Volume Corrente, etc.) ...

        layout.addWidget(self.graph_widget, 1, 0)  # Adiciona os gráficos na segunda linha

    def create_alarm_box(self, layout):
            self.alarm_label = QLabel("Sem Alarmes")
            self.alarm_label.setStyleSheet("background-color: lightgreen; font-size: 16px; padding: 10px;")
            self.alarm_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.alarm_label, 3, 0, 1, 2)  # Caixa de alarmes na quarta linha

    def start_simulation(self):
        if not self.simulator_thread.isRunning():  # Verifica se a thread já está em execução
            self.simulator.start()
            self.simulator_thread.start()

            self.btn_start.setEnabled(False)
            self.btn_pause.setEnabled(True)
            self.btn_stop.setEnabled(True)

        self.paused = False

    def stop_simulation(self):
            self.simulator.stop()
            if self.simulator_thread.isRunning():
                self.simulator_thread.quit()
                self.simulator_thread.wait()  # Aguarda a thread terminar

            self.btn_start.setEnabled(True)
            self.btn_pause.setEnabled(False)
            self.btn_stop.setEnabled(False)

    def pause_simulation(self):
            if not self.paused:
                self.simulator.stop()
                self.btn_pause.setText("Continuar")
                self.paused = True
            else:
                self.simulator.start()
                self.btn_pause.setText("Pausar")
                self.paused = False

    def update_data(self, data):
        # Desempacota os dados recebidos
        respiratory_rate, tidal_volume, inspiratory_pressure, fio2, ventilation_mode, alarm_string, timestamp = data

        # Atualiza os gráficos
        self.data_rr.append(respiratory_rate)
        self.curve_rr.setData(self.data_rr)

        # ... (atualize os outros gráficos) ...

        # Atualiza o box do Volume Corrente
        self.vc_label.setText(f"VC: {tidal_volume:.2f} mL")

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
