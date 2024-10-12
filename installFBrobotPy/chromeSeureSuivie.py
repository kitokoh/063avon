import os
import sys
import time
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QTextEdit
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon

class FacebookLoginMonitor(QWidget):
    def __init__(self):
        super().__init__()
        
        # Définir les chemins et variables
        self.profile_number = 1
        self.profile_path = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data\\Profil {self.profile_number}\\Default"
        self.log_file = "C:\\bon\\check_facebook_login_log.txt"
        self.robot_exe_path = "C:\\chemin\\vers\\robot.exe"
        self.cookie_file = os.path.join(self.profile_path, "Cookies")
        self.attempts = 0
        self.max_attempts = 60

        # Configuration de la fenêtre principale
        self.setWindowTitle("Surveillance de la Connexion Facebook")
        self.setGeometry(680, 390, 500, 300)
        self.setWindowIcon(QIcon("facebook_icon.png"))  # Icône personnalisée

        # Mise en page principale
        self.layout = QVBoxLayout()

        # Label d'information
        self.info_label = QLabel(f"Vérification de la connexion Facebook pour le profil {self.profile_number}.", self)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.info_label)

        # Affichage du log
        self.log_text = QTextEdit(self)
        self.log_text.setReadOnly(True)
        self.layout.addWidget(self.log_text)

        # Bouton pour démarrer la surveillance
        self.start_button = QPushButton("Démarrer la surveillance", self)
        self.start_button.clicked.connect(self.start_monitoring)
        self.layout.addWidget(self.start_button)

        # Appliquer la mise en page
        self.setLayout(self.layout)

    def write_to_log(self, message):
        # Écrire dans la zone de texte et dans le fichier log
        with open(self.log_file, 'a') as log:
            log.write(message + "\n")
        self.log_text.append(message)

    def start_monitoring(self):
        # Lancer Chrome avec le profil spécifié
        self.write_to_log(f"[INFO] Démarrage de Google Chrome pour le profil {self.profile_number} - {time.strftime('%Y-%m-%d %H:%M:%S')}")
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        chrome_cmd = [chrome_path, f"--user-data-dir={self.profile_path}", "https://www.facebook.com"]
        subprocess.Popen(chrome_cmd)

        # Démarrer la surveillance du cookie
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_cookie)
        self.timer.start(1000)  # Vérifier toutes les 1 seconde

    def check_cookie(self):
        if os.path.exists(self.cookie_file):
            self.write_to_log(f"[INFO] Cookie Facebook détecté pour le profil {self.profile_number} - {time.strftime('%Y-%m-%d %H:%M:%S')}")
            self.info_label.setText("Cookie détecté ! Fermeture de Chrome et lancement de robot.exe.")
            self.timer.stop()

            # Fermer Chrome
            subprocess.call(["taskkill", "/IM", "chrome.exe", "/F"])
            self.write_to_log(f"[INFO] Fermeture de Google Chrome pour le profil {self.profile_number} - {time.strftime('%Y-%m-%d %H:%M:%S')}")

            # Lancer robot.exe
            subprocess.Popen([self.robot_exe_path])
            self.write_to_log(f"[INFO] Lancement de robot.exe après connexion à Facebook - {time.strftime('%Y-%m-%d %H:%M:%S')}")

        else:
            self.attempts += 1
            if self.attempts >= self.max_attempts:
                self.write_to_log(f"[ERREUR] Temps d'attente expiré. Le cookie n'a pas été trouvé.")
                self.info_label.setText("Temps d'attente expiré. Le cookie n'a pas été trouvé.")
                self.timer.stop()

def main():
    app = QApplication(sys.argv)

    # Créer et afficher la fenêtre principale
    window = FacebookLoginMonitor()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
