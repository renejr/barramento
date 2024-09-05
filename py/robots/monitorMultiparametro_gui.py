import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QProgressBar, QVBoxLayout, QGridLayout, QPushButton
from PyQt5.QtCore import Qt, QThread
from monitorMultiparametro import MonitorSimulator  # Importe a classe do simulador

class MonitorGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simulador de Monitor Multiparâmetro")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Criando a thread do simulador
        self.simulator_thread = QThread()
        self.simulator = MonitorSimulator()
        self.simulator.moveToThread(self.simulator_thread)
        # Conectando o sinal aos slots
        self.simulator.data_updated.connect(self.update_data)
        self.simulator_thread.started.connect(self.simulator.start) 

        # Inicialize data_labels e progress_bars aqui
        self.data_labels = {}
        self.progress_bars = {}

        self.init_ui()

    def init_ui(self):
        grid_layout = QGridLayout(self.central_widget)

        # Criando os boxes dos sinais vitais
        self.create_vital_sign_box("Frequência Cardíaca (bpm)", "heart_rate", grid_layout, 0, 0)
        self.create_vital_sign_box("Pressão Arterial Sistólica (mmHg)", "systolic_bp", grid_layout, 0, 1)
        self.create_vital_sign_box("Pressão Arterial Diastólica (mmHg)", "diastolic_bp", grid_layout, 1, 0)
        self.create_vital_sign_box("Saturação de Oxigênio (%)", "oxygen_saturation", grid_layout, 1, 1)
        self.create_vital_sign_box("Temperatura Corporal (°C)", "body_temperature", grid_layout, 2, 0)
        self.create_vital_sign_box("Frequência Respiratória (rpm)", "respiratory_rate", grid_layout, 2, 1)

        # Criando os botões
        self.btn_start = QPushButton("Iniciar", self)
        self.btn_start.clicked.connect(self.start_simulation)
        grid_layout.addWidget(self.btn_start, 3, 0)

        self.btn_pause = QPushButton("Pausar", self)
        self.btn_pause.clicked.connect(self.pause_simulation)
        self.btn_pause.setEnabled(False)  # Começa desabilitado
        grid_layout.addWidget(self.btn_pause, 3, 1)

        self.btn_stop = QPushButton("Parar", self)
        self.btn_stop.clicked.connect(self.stop_simulation)
        self.btn_stop.setEnabled(False)  # Começa desabilitado
        grid_layout.addWidget(self.btn_stop, 4, 0)

        self.btn_exit = QPushButton("Sair", self)
        self.btn_exit.clicked.connect(self.close)
        grid_layout.addWidget(self.btn_exit, 4, 1)

    def create_vital_sign_box(self, label_text, data_key, layout, row, col):
        vbox = QVBoxLayout()
        label = QLabel(label_text)
        vbox.addWidget(label)

        # Não é mais necessário inicializar data_labels e progress_bars aqui
        self.data_labels[data_key] = QLabel("0")
        self.data_labels[data_key].setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.data_labels[data_key])

        self.progress_bars[data_key] = QProgressBar()
        self.progress_bars[data_key].setRange(0, 100)
        vbox.addWidget(self.progress_bars[data_key])

        layout.addLayout(vbox, row, col)

    def update_data(self, data):
        # Código dentro da função - indentado com 4 espaços
        self.data_labels["heart_rate"].setText(f"{data['heart_rate']:.2f}")
        self.data_labels["systolic_bp"].setText(f"{data['systolic_bp']:.2f}")
        self.data_labels["diastolic_bp"].setText(f"{data['diastolic_bp']:.2f}")
        self.data_labels["oxygen_saturation"].setText(f"{data['oxygen_saturation']:.2f}")
        self.data_labels["body_temperature"].setText(f"{data['body_temperature']:.2f}")
        self.data_labels["respiratory_rate"].setText(f"{data['respiratory_rate']:.2f}")

        # Lógica da barra de progresso (FAZER PARA CADA SINAL VITAL):
        self.update_progress_bar("heart_rate", data['heart_rate'], 60, 100)
        self.update_progress_bar("systolic_bp", data['systolic_bp'], 90, 140)
        # ... (Implementar lógica para os outros sinais vitais)

    def update_progress_bar(self, data_key, value, min_limit, max_limit):
        # ... (mesmo código do update_progress_bar anterior)
        pass  # Implemente a lógica da barra de progresso aqui

    def start_simulation(self):
        self.simulator_thread.start()
        self.btn_start.setEnabled(False)
        self.btn_pause.setEnabled(True)
        self.btn_stop.setEnabled(True)

    def stop_simulation(self):
        self.simulator.stop()
        self.simulator_thread.quit()  # Encerra a thread
        self.simulator_thread.wait()  # Aguarda a thread finalizar
        self.btn_start.setEnabled(True)
        self.btn_pause.setEnabled(False)
        self.btn_stop.setEnabled(False)

    def pause_simulation(self):
        # Lógica para pausar/retomar a simulação (ainda a ser implementada)
        pass 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MonitorGUI()
    window.show()
    sys.exit(app.exec_())
