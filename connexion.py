from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Se connecter")
        self.setStyleSheet("background-color: #f0f0f0;")  # Couleur de fond

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

        self.create_header()
        self.create_login_form()
        self.create_footer()

    def create_header(self):
        header = QLabel("Bienvenue dans Mon Application")
        header.setFont(QFont("Arial", 24))
        header.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(header)

    def create_login_form(self):
        form_layout = QVBoxLayout()
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        self.username_input.setFixedWidth(300)
        self.layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedWidth(300)
        self.layout.addWidget(self.password_input)

        login_button = QPushButton("Se connecter")
        login_button.setFont(QFont("Arial", 14))
        login_button.clicked.connect(self.login)
        self.layout.addWidget(login_button)

        create_account_button = QPushButton("Créer un compte")
        create_account_button.setFont(QFont("Arial", 14))
        create_account_button.clicked.connect(self.create_account)
        self.layout.addWidget(create_account_button)

    def create_footer(self):
        footer = QLabel("© 2024 Mon Application. Tous droits réservés.")
        footer.setFont(QFont("Arial", 10))
        footer.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(footer)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        # Logique de connexion ici
        if username == "admin" and password == "admin":  # Remplacez par votre logique de vérification
            QMessageBox.information(self, "Connexion réussie", "Bienvenue, " + username + "!")
        else:
            QMessageBox.warning(self, "Erreur de connexion", "Nom d'utilisateur ou mot de passe incorrect.")

    def create_account(self):
        # Logique pour rediriger vers la création de compte
        QMessageBox.information(self, "Créer un compte", "Redirection vers la page de création de compte.")

