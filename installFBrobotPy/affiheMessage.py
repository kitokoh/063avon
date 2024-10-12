import sys
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QProgressBar, QPushButton, QTimer
)
from PyQt5.QtCore import Qt

class InstallationWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI FB Robot Pro - Kurulum Basarili")
        self.setGeometry(680, 390, 560, 300)  # Centrer la fenêtre

        # Mise en page principale
        self.layout = QVBoxLayout()

        # Ajout du logo
        self.logo_label = QLabel("AI FB Robot Pro - Basariyla Kuruldu", self)
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.logo_label)

        # Barre de progression pour simuler le chargement
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.layout.addWidget(self.progress_bar)

        # Bouton pour démarrer le processus
        self.start_button = QPushButton("Démarrer l'installation", self)
        self.start_button.clicked.connect(self.start_installation)
        self.layout.addWidget(self.start_button)

        # Label d'information pour les messages
        self.info_label = QLabel("", self)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.info_label)

        # Appliquer la mise en page
        self.setLayout(self.layout)

    def start_installation(self):
        # Désactiver le bouton pendant l'installation
        self.start_button.setEnabled(False)
        
        # Lancer la simulation du processus d'installation
        self.info_label.setText("Lisans anahtariniz hazirlaniyor...")
        self.simulate_loading(30, self.connect_email_server)

    def simulate_loading(self, steps, next_step_callback):
        # Simule le chargement en incrémentant la barre de progression
        self.progress = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.update_progress(steps, next_step_callback))
        self.timer.start(100)

    def update_progress(self, steps, next_step_callback):
        if self.progress < 100:
            self.progress += int(100 / steps)
            self.progress_bar.setValue(self.progress)
        else:
            self.timer.stop()
            next_step_callback()

    def connect_email_server(self):
        # Simule la connexion au serveur d'email
        self.info_label.setText("E-posta sunucusu ile baglanti kuruluyor...")
        self.simulate_loading(20, self.installation_complete)

    def installation_complete(self):
        # Message final une fois l'installation terminée
        self.progress_bar.setValue(100)
        self.info_label.setText("AI FB Robot Pro basariyla kuruldu!\nLisans anahtariniz e-postaniza gonderilecektir.")
        self.start_button.setText("Fermer")
        self.start_button.setEnabled(True)
        self.start_button.clicked.connect(self.close)

def main():
    app = QApplication(sys.argv)

    # Créer et afficher la fenêtre
    window = InstallationWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
