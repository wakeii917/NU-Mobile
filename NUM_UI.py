import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout, QGroupBox, QFrame, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, QPropertyAnimation, QRect, Qt, QTime
from PyQt5.QtWebEngineWidgets import QWebEngineView


class Slideshow(QWidget):
    def __init__(self, image_paths):
        super().__init__()
        self.image_paths = image_paths
        self.current_index = 0
        self.transitioning = False  # Flag qui indique si une transition est en cours

        self.init_ui()
        self.start_timer()

    def init_ui(self):
        self.setWindowTitle("Slideshow")

        # Layout principal
        vbox = QVBoxLayout()

        # QLabel pour afficher les images
        self.current_image_label = QLabel(self)
        self.next_image_label = QLabel(self)

        self.current_image_label.setFixedSize(650, 450)
        self.next_image_label.setFixedSize(650, 450)
        self.next_image_label.setVisible(False)  # Masquer le QLabel au départ

        self.update_image_labels(0)  # Initialize with the first image

        # Boutons précédent et suivant
        hbox = QHBoxLayout()
        prev_button = QPushButton("Précédent", self)
        next_button = QPushButton("Suivant", self)

        prev_button.clicked.connect(self.show_prev_image)
        next_button.clicked.connect(self.show_next_image)

        # Ajustements des boutons pour être plus larges et placés un peu plus bas
        prev_button.setFixedSize(200, 45)
        prev_button.setStyleSheet("border-radius:9px; backgroud-color:#808bc2; color:#fff; font-family: Lexend Exa; font-size:20px;")
        next_button.setFixedSize(200, 45)
        next_button.setStyleSheet("border-radius:9px; backgroud-color:#808bc2; color:#fff; font-family: Lexend Exa;font-size:20px;")
  

        hbox.addWidget(prev_button)
        hbox.addWidget(next_button)

        # Ajouter un espace entre les boutons et les images
        hbox.addSpacing(50)

        vbox.addWidget(self.current_image_label)
        vbox.addWidget(self.next_image_label)
        vbox.addLayout(hbox)
        
        # Ajouter un espace en bas
        vbox.addSpacing(25)

        self.setLayout(vbox)
        self.setFixedSize(650, 550)  # Fixer la taille de la fenêtre

    def start_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_next_image)
        self.timer.start(4000)  # Changer d'image toutes les 4 secondes

    def update_image_labels(self, next_index):
        current_pixmap = QPixmap(self.image_paths[self.current_index])
        next_pixmap = QPixmap(self.image_paths[next_index])

        self.current_image_label.setPixmap(current_pixmap.scaled(800, 600, aspectRatioMode=True))
        self.next_image_label.setPixmap(next_pixmap.scaled(800, 600, aspectRatioMode=True))

        self.current_image_label.setGeometry(0, 0, 800, 600)
        self.next_image_label.setGeometry(800, 0, 800, 600)  # Position de la prochaine image en dehors de l'écran

    def show_prev_image(self):
        if not self.transitioning:  # évite plusieurs transitions en même temps
            next_index = (self.current_index - 1) % len(self.image_paths)
            self.animate_transition(next_index, direction=-1)

    def show_next_image(self):
        if not self.transitioning:  # évite plusieurs transitions en même temps
            next_index = (self.current_index + 1) % len(self.image_paths)
            self.animate_transition(next_index, direction=1)

    def animate_transition(self, next_index, direction=1):
        self.transitioning = True  # active le flag de transition

        self.update_image_labels(next_index)

        self.current_animation = QPropertyAnimation(self.current_image_label, b"geometry")
        self.next_animation = QPropertyAnimation(self.next_image_label, b"geometry")

        self.current_animation.setDuration(1000)
        self.next_animation.setDuration(1000)

        if direction == 1:  # Défilement vers la gauche
            self.current_animation.setStartValue(QRect(0, 0, 800, 600))
            self.current_animation.setEndValue(QRect(-800, 0, 800, 600))

            self.next_animation.setStartValue(QRect(800, 0, 800, 600))
            self.next_animation.setEndValue(QRect(0, 0, 800, 600))
        else:  # Défilement vers la droite
            self.current_animation.setStartValue(QRect(0, 0, 800, 600))
            self.current_animation.setEndValue(QRect(800, 0, 800, 600))

            self.next_animation.setStartValue(QRect(-800, 0, 800, 600))
            self.next_animation.setEndValue(QRect(0, 0, 800, 600))

        self.next_image_label.setVisible(True)  # Afficher le QLabel avant de commencer l'animation
        self.current_animation.start()
        self.next_animation.start()

        self.current_animation.finished.connect(lambda: self.finish_transition(next_index))
        self.next_animation.finished.connect(lambda: self.finish_transition(next_index))

    def finish_transition(self, next_index):
        self.current_index = next_index  # Update l'index pour l'image prochaine
        self.transitioning = False  # Reset le flag de transition
        self.update_image_labels(next_index)
        self.next_image_label.setVisible(False)  # Masquer le QLabel après l'animation


class StartWindow(QWidget):
    
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre
        self.setWindowTitle("StartScreen")
        self.showFullScreen()
        self.setStyleSheet("background-color: #191D32;") 

        # Layout principal en deux colonnes
        layout = QHBoxLayout()

        # Colonne 1 : Image
        self.image_label = QLabel(self)
        self.image = QPixmap("LOGO1.png").scaled(900, 1800, Qt.KeepAspectRatio)
        self.image_label.setPixmap(self.image)

        col1 = QVBoxLayout()
        col1.addWidget(self.image_label,alignment=Qt.AlignCenter)

        # Colonne 2 : Liste de boutons
        col2 = QVBoxLayout()

        # Création d'un QFrame pour entourer tous les boutons
        frame = QFrame(self)
        frame.setFixedSize(600,300)
        frame.setStyleSheet("background-color: #e2e2e2; border-radius: 30px; border: 15px solid #fff;")
        frame_layout = QVBoxLayout(frame)  # Layout pour les boutons à l'intérieur du cadre

        for i in range(1, 3):
            button = QPushButton(f"Mode {i}")
            button.setFixedSize(500,100)
            button.clicked.connect(lambda checked, building=f"Mode {i}": self.launch_MainWindow())

            button.setStyleSheet("""
                    QPushButton {
                        font-size: 36px;
                        font-family: Lexend Exa;
                       
                        color: #2b2b2b;
                        background-color: transparent;
                        border: none; 
                        padding: 5px 10px;
                        margin: 5px;
                    }

                    QPushButton:hover {
                        background-color: #808bc2;
                    }
                """)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Ajuste la taille du bouton

            # Ajout du bouton au layout du cadre
            frame_layout.addWidget(button, alignment=Qt.AlignCenter)

        # Ajout du cadre avec les boutons au layout principal
        col2.addWidget(frame, alignment=Qt.AlignCenter)  # Alignement au centre
        # Ajout des colonnes au layout principal
        layout.addLayout(col1)
        layout.addLayout(col2)

        self.setLayout(layout)

    def launch_MainWindow(self):
        self.main_window = MainWindow()
        self.main_window.show()

class MainWindow(QWidget):
    
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre
        self.setWindowTitle("Accueil")
        self.showFullScreen()
        self.setStyleSheet("background-color: #191D32;") 

        # Layout principal en deux colonnes
        layout = QHBoxLayout()

        # Colonne 1 : Image
        self.image_label = QLabel(self)
        self.image = QPixmap("LOGO1.png").scaled(900, 1800, Qt.KeepAspectRatio)
        self.image_label.setPixmap(self.image)

        col1 = QVBoxLayout()
        col1.addWidget(self.image_label,alignment=Qt.AlignCenter)

        # Colonne 2 : Liste de boutons
        col2 = QVBoxLayout()

        # Création d'un QFrame pour entourer tous les boutons
        frame = QFrame(self)
        frame.setFixedSize(600,900)
        frame.setStyleSheet("background-color: #e2e2e2; border-radius: 30px; border: 15px solid #fff;")
        frame_layout = QVBoxLayout(frame)  # Layout pour les boutons à l'intérieur du cadre

        for i in range(1, 7):
            button = QPushButton(f"Batiment {i}")
            button.setFixedSize(500,100)
            button.clicked.connect(lambda checked, building=f"Batiment {i}": self.launch_conduite_auto(building))

            button.setStyleSheet("""
                    QPushButton {
                        font-size: 36px;
                        font-family: Lexend Exa;
                       
                        color: #2b2b2b;
                        background-color: transparent;
                        border: none; 
                        padding: 5px 10px;
                        margin: 5px;
                    }

                    QPushButton:hover {
                        background-color: #808bc2;
                    }
                """)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Ajuste la taille du bouton

            # Ajout du bouton au layout du cadre
            frame_layout.addWidget(button, alignment=Qt.AlignCenter)

        # Ajout du cadre avec les boutons au layout principal
        col2.addWidget(frame, alignment=Qt.AlignCenter)  # Alignement au centre
        # Ajout des colonnes au layout principal
        layout.addLayout(col1)
        layout.addLayout(col2)

        self.setLayout(layout)

    def launch_conduite_auto(self, building_name):
        self.conduite_auto_window = ConduiteAutoWindow(building_name)
        self.conduite_auto_window.show()


class ConduiteAutoWindow(QWidget):
    def __init__(self, building_name):
        super().__init__()
        # Configuration de la fenêtre
        self.setWindowTitle("Conduite Auto")
        self.showFullScreen()
        self.setStyleSheet("background-color: #191D32;")

        #latitudes et longitudes initiales 
        self.latitude = 47.23784881934657
        self.longitude = -1.55413561067741

        # Layout principal en grille
        layout = QGridLayout()

        # Colonne 1 : Image
        self.image_label = QLabel(self)
        self.image = QPixmap("LOGO1.png").scaled(550, 900, Qt.KeepAspectRatio)
        self.image_label.setPixmap(self.image)
        layout.addWidget(self.image_label, 0, 0, 1, 2) 

        groupbox_gps = QGroupBox()
        groupbox_gps.setStyleSheet(""" 
            QGroupBox {
                border: 6px solid #fff; 
                border-radius: 9px; 
                padding: 5px; 
                background-color: #e2e2e2;   
            } 
            QLabel {
                font-size: 22px;
                font-family: Lexend Exa;
                color: #2b2b2b;
                background-color: #fff;
                border: transparent;
                padding: 5px 10px; 
                margin: 2px;
                border-radius: 9px;
            }
        """)
        layout.addWidget(groupbox_gps, 1, 0)

        # Layout interne pour le groupbox GPS
        groupbox_gps_layout = QVBoxLayout()
        frame_gps = QFrame()
        frame_gps.setStyleSheet("background-color: white; border-radius: 9px;")
        frame_gps_layout = QVBoxLayout(frame_gps)

        # Labels pour afficher les données GPS
        self.latitude_label = QLabel(f"Latitude: {self.latitude}")
        self.longitude_label = QLabel(f"Longitude: {self.longitude}")
        self.speed_label = QLabel("Speed: -- km/h")

        frame_gps_layout.addWidget(self.latitude_label)
        frame_gps_layout.addWidget(self.longitude_label)
        frame_gps_layout.addWidget(self.speed_label)

        groupbox_gps_layout.addWidget(frame_gps)
        groupbox_gps.setLayout(groupbox_gps_layout) 
        

        # Colonne 2 : Température, humidité, heure
        groupbox_weather = QGroupBox()
        groupbox_weather.setFixedSize(480,540)
        groupbox_weather.setStyleSheet(""" 
             QGroupBox {
                border: 6px solid #fff; 
                border-radius: 9px; 
                padding: 5px; 
                background-color: #e2e2e2;   
                } 
            QLabel {
                font-size: 22px;
                font-family: Lexend Exa;
                color: #2b2b2b;
                background-color:fff;
                border: 1px solid #365486;
                padding: 5px 10px; 
                margin: 2px;
                border-radius: 9px;
                }
        """)

        groupbox_weather_layout = QVBoxLayout()

        frame = QFrame()  # Créer une frame pour englober les labels
        frame.setFixedSize(440,500)
        frame.setStyleSheet("background-color: white; border-radius:9px;")  # Couleur de fond de la frame

        frame_layout = QVBoxLayout(frame)  # Layout pour la frame
        frame_layoutH = QHBoxLayout()
        frame_layoutH1 = QHBoxLayout()
        frame_layoutH2 = QHBoxLayout()

        # Logo pour la température
        self.temperature_label = QLabel("Température: 25°C")
        self.temperature_label.setStyleSheet("background-color: transparent; border: none;")  # Supprime le fond et la bordure
        frame_layoutH.addWidget(self.temperature_label)

        temperature_logo_label = QLabel()
        temperature_logo_label.setStyleSheet("border:none;")
        temperature_logo = QPixmap("temperature_logo.png").scaledToHeight(50)  # Insérez le chemin de votre logo
        temperature_logo_label.setPixmap(temperature_logo)
        frame_layoutH.addWidget(temperature_logo_label,alignment=Qt.AlignCenter)

        frame_layout.addLayout(frame_layoutH)

        # Logo pour l'humidité
        self.humidity_label = QLabel("Humidité: 45 %")
        self.humidity_label.setStyleSheet("background-color: transparent; border: none;")  # Supprime le fond et la bordure
        frame_layoutH1.addWidget(self.humidity_label)

        humidity_logo_label = QLabel()
        humidity_logo_label.setStyleSheet("border:none;")
        humidity_logo = QPixmap("humidity_logo.png").scaledToHeight(50)  # Insérez le chemin de votre logo
        humidity_logo_label.setPixmap(humidity_logo)
        frame_layoutH1.addWidget(humidity_logo_label,alignment=Qt.AlignCenter)

        frame_layout.addLayout(frame_layoutH1)

        # Logo pour l'heure
        self.time_label = QLabel()
        self.time_label.setStyleSheet("background-color: transparent; border: none;")
        frame_layoutH2.addWidget(self.time_label)

        time_logo_label = QLabel()
        time_logo_label.setStyleSheet("border:none;")
        time_logo = QPixmap("time_logo.png").scaledToHeight(50)  # Insérez le chemin de votre logo
        time_logo_label.setPixmap(time_logo)
        frame_layoutH2.addWidget(time_logo_label,alignment=Qt.AlignCenter)

        frame_layout.addLayout(frame_layoutH2)
        

        # Ajout de la frame au layout du groupbox
        groupbox_weather_layout.addWidget(frame)
        groupbox_weather.setLayout(groupbox_weather_layout)
   
        layout.addWidget(groupbox_weather, 0, 1)
        
        # Colonne 3 : Deux images côte à côte, label et diaporama
        groupbox_images = QGroupBox()
        groupbox_images.setFixedSize(800,450)
        groupbox_images.setStyleSheet(""" 
            QGroupBox {
                border: 6px solid #fff;
                border-radius: 9px;
                padding: 5px;
                background-color: #e2e2e2;
            }
            QLabel{
                font-size: 42px;
                font-family: Lexend Exa;
                color: #2b2b2b;
                background-color: transparent;
                border: transparent;
                padding: 5px 10px;
                margin: 2px;
                border-radius: 9px;
            }
        """)
        groupbox_images_layout = QVBoxLayout()

        # Création de la frame pour les images et le label de destination
        frame_images = QFrame()
        frame_images.setStyleSheet("background-color: white; border-radius: 9px;")
        frame_images_layout = QVBoxLayout(frame_images)  # Layout pour les éléments dans la frame

        # Layout pour les images
        images_layout = QHBoxLayout()

        # Première image
        self.image1_label = QLabel(self)
        self.image1 = QPixmap("arr1.png").scaled(300, 300, Qt.KeepAspectRatio)
        self.image1_label.setPixmap(self.image1)

        # Deuxième image
        self.image2_label = QLabel(self)
        self.image2 = QPixmap("arr2.png").scaled(300, 300, Qt.KeepAspectRatio)
        self.image2_label.setPixmap(self.image2)

        # Ajout des images au layout des images
        images_layout.addWidget(self.image1_label, alignment=Qt.AlignCenter)
        images_layout.addWidget(self.image2_label, alignment=Qt.AlignCenter)

        # Ajout du layout des images à la frame
        frame_images_layout.addLayout(images_layout)

        # Label de destination
        self.destination_label = QLabel()
        self.destination_label.setText(f"Destination: {building_name}")
        frame_images_layout.addWidget(self.destination_label, alignment=Qt.AlignCenter)

        # Ajout de la frame au layout du groupbox
        groupbox_images_layout.addWidget(frame_images)

        # Appliquer le layout au groupbox
        groupbox_images.setLayout(groupbox_images_layout)

        # Ajouter le groupbox au layout principal
        layout.addWidget(groupbox_images, 1, 2)


        # Diaporama
        groupbox_slideshow = QGroupBox()
        groupbox_slideshow.setFixedSize(800,550)
        groupbox_slideshow.setStyleSheet(""" 
            QGroupBox {
                border: 6px solid #fff;
                border-radius: 9px;
                padding: 5px;
                background-color: white;
            }
            QLabel{
                font-size: 15px;
                font-family: Lexend Exa;
                color: #2b2b2b;
                background-color: transparent;
                border-radius: 15px;
                border: white;
                padding: 5px 5px;
                margin: 2px;
               
            }
        """)
        groupbox_slideshow_layout = QVBoxLayout()
        self.slideshow = Slideshow([
            "4.png"
        ])
        groupbox_slideshow_layout.addWidget(self.slideshow,alignment=Qt.AlignCenter)
        groupbox_slideshow.setLayout(groupbox_slideshow_layout)
        layout.addWidget(groupbox_slideshow, 0, 2)

        # Ajout de la carte Google Maps
        self.map_view = QWebEngineView()
        self.map_view.setFixedSize(450, 500)  # Taille de la carte
        layout.addWidget(self.map_view, 1, 1,alignment=Qt.AlignCenter)  # Insérer dans la troisième ligne, colonnes 1 à 3

        self.setLayout(layout)

        # Afficher la carte Google Maps
        self.show_map()
        # Configure the timer to update the map position
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(10000)  # Update every 5 seconds

        self.time_update_timer = QTimer(self)
        self.time_update_timer.timeout.connect(self.update_time)
        self.time_update_timer.start(1000)
    def update_time(self):
        current_time = QTime.currentTime().toString("HH:mm:ss")
        self.time_label.setText(f"Heure: {current_time}")

    def show_map(self):
        latitude = 47.23784881934657
        longitude = -1.55413561067741
        zoom = 18
        map_url = "https://www.google.com/maps/embed/v1/place?key=AIzaSyD3SKZmyVQpE88FpG9OJ5sfJflaaA8-t2g&q={},{}&zoom={},&maptype=satellite".format(latitude, longitude, zoom) #clé api ajoutée pour accéder 
        html_content = """
        <!DOCTYPE html>
        <html>
        <head><title>Google Maps</title></head>
        <body style="margin:0;padding:0;">
            <iframe width="440px" height="580px" frameborder="0" style="border:0;width:450px;height:600px;" 
                    src="{}" allowfullscreen></iframe>
        </body>
        </html>
        """.format(map_url)
        self.map_view.setHtml(html_content)
        
    def update_position(self):
       
        # ces coordonnées sont mises à des fins de simulation. elles seront remplacés par les coordonnées transmises par le gps NEO6M
        self.latitude += 0.0001  
        self.longitude += 0.0001  
        # actualise la fenetre
        self.show_map()

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = StartWindow()
    main_window.show()
    sys.exit(app.exec_())

