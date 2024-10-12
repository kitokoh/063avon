import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon  # Importer QIcon pour définir l'icône de la fenêtre
from ui.header import HeaderSection
from ui.footer import FooterSection
from ui.login import LoginModule
from home import HomePage  # Assurez-vous d'importer le module d'accueil

class Nova360ProApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nova360Pro - Connexion")
        self.setGeometry(100, 100, 800, 600)
        # Définir l'icône de la fenêtre
        self.setWindowIcon(QIcon('resources/icons/robot-512.png'))  # Spécifiez le chemin de l'icône

        # Widget central
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layout principal
        self.main_layout = QVBoxLayout(self.central_widget)

        # Initialiser les modules
        self.header = HeaderSection()  # En-tête
        self.footer = FooterSection()  # Pied de page
        self.login_module = LoginModule()  # Module de connexion

        # Connecter le signal de connexion réussie
        self.login_module.connection_successful.connect(self.show_home)

        # Afficher le module de connexion
        self.show_login()

    def show_login(self):
        # Ajouter l'en-tête, le module de connexion et le pied de page
        self.main_layout.addWidget(self.header)  # Ajouter l'en-tête
        self.main_layout.addWidget(self.login_module)  # Ajouter le module de connexion
        self.main_layout.addWidget(self.footer)  # Ajouter le pied de page

    def show_home(self):
        # Effacer l'en-tête, le module de connexion et le pied de page
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget in (self.login_module, self.header, self.footer):
                self.main_layout.removeWidget(widget)
                widget.deleteLater()  # Libérer la mémoire

        # Ajouter la page d'accueil
        self.home_module = HomePage()  # Assurez-vous d'avoir un module HomePage
        self.main_layout.addWidget(self.home_module)  # Ajouter la page d'accueil

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Nova360ProApp()
    window.show()  # Assurez-vous d'afficher la fenêtre
    sys.exit(app.exec_())
