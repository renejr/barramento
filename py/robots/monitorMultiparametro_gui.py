import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QGridLayout, QPushButton
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

        # Initialize data_labels, progress_bars, and alert_labels here
        self.data_labels = {}
        self.alert_labels = {}  # Add this line to initialize alert_labels

        self.paused = False  # Variável de controle de pausa

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

        self.data_labels[data_key] = QLabel("0")
        self.data_labels[data_key].setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.data_labels[data_key])

        # Crie um QLabel para a mensagem de alerta
        self.alert_labels[data_key] = QLabel("Sem Alarmes") 
        self.alert_labels[data_key].setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.alert_labels[data_key])

        layout.addLayout(vbox, row, col)

    def update_data(self, data):
        # Código dentro da função - indentado com 4 espaços
        self.data_labels["heart_rate"].setText(f"{data['heart_rate']:.2f}")
        self.data_labels["systolic_bp"].setText(f"{data['systolic_bp']:.2f}")
        self.data_labels["diastolic_bp"].setText(f"{data['diastolic_bp']:.2f}")
        self.data_labels["oxygen_saturation"].setText(f"{data['oxygen_saturation']:.2f}")
        self.data_labels["body_temperature"].setText(f"{data['body_temperature']:.2f}")
        self.data_labels["respiratory_rate"].setText(f"{data['respiratory_rate']:.2f}")

        self.alert_labels["heart_rate"].setText(self.check_alarms("heart_rate", data['heart_rate'], 50, 110))
        self.alert_labels["systolic_bp"].setText(self.check_alarms("systolic_bp", data['systolic_bp'], 90, 140))
        self.alert_labels["diastolic_bp"].setText(self.check_alarms("diastolic_bp", data['diastolic_bp'], 50, 100))
        self.alert_labels["oxygen_saturation"].setText(self.check_alarms("oxygen_saturation", data['oxygen_saturation'], 90, 100))
        self.alert_labels["body_temperature"].setText(self.check_alarms("body_temperature", data['body_temperature'], 35.0, 38.0))
        self.alert_labels["respiratory_rate"].setText(self.check_alarms("respiratory_rate", data['respiratory_rate'], 10, 25))

        # ... (Repetir para outros sinais vitais)

    def check_alarms(self, data_key, value, min_limit, max_limit):
        print(data_key, value, min_limit, max_limit)

        # Código de verificação de alertas
        if value < min_limit:
            self.alert_labels[data_key].setStyleSheet("background-color: lightcoral; font-size: 16px; padding: 10px;")
            return f"{data_key.upper()} BAIXO!"
        elif value > max_limit:
            self.alert_labels[data_key].setStyleSheet("background-color: lightcoral; font-size: 16px; padding: 10px;")
            return f"{data_key.upper()} ALTO!"
        else:
            self.alert_labels[data_key].setStyleSheet("background-color: lightgreen; font-size: 16px; padding: 10px;")
            return "Sem Alarmes"

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
        if not self.paused:
            self.simulator.stop()  # Pause the simulator
            self.btn_pause.setText("Continuar")
            self.paused = True
        else:
            self.simulator.start()  # Resume the simulator
            self.btn_pause.setText("Pausar")
            self.paused = False
 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MonitorGUI()
    window.show()
    sys.exit(app.exec_())
