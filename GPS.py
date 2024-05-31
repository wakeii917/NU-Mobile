import sys
import serial
import pynmea2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGroupBox, QLabel, QPushButton
from PyQt5.QtCore import QTimer

class GPSWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_gps_data)
        self.timer.start(1000)  # Mise à jour toutes les secondes

    def init_ui(self):
        self.setWindowTitle("GPS Data")

        # Layout principal
        vbox = QVBoxLayout()

        # GroupBox pour les données GPS
        gps_groupbox = QGroupBox("GPS Data")
        gps_layout = QVBoxLayout()

        self.latitude_label = QLabel("Latitude: ")
        self.longitude_label = QLabel("Longitude: ")
        self.speed_label = QLabel("Speed: ")

        gps_layout.addWidget(self.latitude_label)
        gps_layout.addWidget(self.longitude_label)
        gps_layout.addWidget(self.speed_label)

        gps_groupbox.setLayout(gps_layout)
        vbox.addWidget(gps_groupbox)

        self.setLayout(vbox)

    def update_gps_data(self):
        try:
            # Ouverture de la communication série avec le port du GPS (ajustez le port COM en fonction de votre système)
            with serial.Serial('COM3', 9600, timeout=1) as ser:
                # Lecture des données NMEA depuis le port série
                sentence = ser.readline().decode('ascii')

                # Analyse de la phrase NMEA
                msg = pynmea2.parse(sentence)

                if isinstance(msg, pynmea2.GGA):
                    latitude = msg.latitude
                    longitude = msg.longitude
                    speed = msg.speed * 1.852  # Conversion des nœuds en km/h

                    self.latitude_label.setText(f"Latitude: {latitude:.6f}")
                    self.longitude_label.setText(f"Longitude: {longitude:.6f}")
                    self.speed_label.setText(f"Speed: {speed:.2f} km/h")

        except Exception as e:
            print("Error:", e)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Main Window")

        layout = QVBoxLayout()

        # Création de la première colonne de boutons
        groupbox1 = QGroupBox("Column 1")
        layout1 = QVBoxLayout()

        # Ajout des boutons
        for i in range(1, 4):
            button = QPushButton(f"Button {i}")
            layout1.addWidget(button)

        groupbox1.setLayout(layout1)

        # Création de la deuxième colonne avec le widget GPS
        groupbox2 = QGroupBox("Column 2")
        layout2 = QVBoxLayout()

        gps_widget = GPSWidget()
        layout2.addWidget(gps_widget)

        groupbox2.setLayout(layout2)

        layout.addWidget(groupbox1)
        layout.addWidget(groupbox2)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
