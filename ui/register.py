import json
import re
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from mail.mail import Mailer  # Importer la classe Mailer
import hashlib  # Pour le hachage des mots de passe

class RegisterModule(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Mise en page principale
        self.setWindowTitle(self.tr("Créer un compte"))
        self.setFixedSize(600, 500)
        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        # Zone pour l'image
        self.image_label = QLabel(self)
        self.image_label.setPixmap(QPixmap("resources/images/2.jpg").scaled(450, 450, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.layout.addWidget(self.image_label)

        # Mise en page pour le formulaire
        form_layout = QVBoxLayout()

        # Titre du formulaire
        title_label = QLabel(self.tr("Créer un compte"))
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(title_label)

        # Champ de saisie pour le nom d'utilisateur
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText(self.tr("Nom d'utilisateur"))
        self.username_input.setStyleSheet(self.input_style())
        form_layout.addWidget(self.username_input)

        # Champ de saisie pour le mot de passe
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText(self.tr("Mot de passe"))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.input_style())
        form_layout.addWidget(self.password_input)

        # Champ de confirmation du mot de passe
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setPlaceholderText(self.tr("Confirmer le mot de passe"))
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet(self.input_style())
        form_layout.addWidget(self.confirm_password_input)

        # Champ de saisie pour l'e-mail (obligatoire)
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText(self.tr("Adresse e-mail"))
        self.email_input.setStyleSheet(self.input_style())
        form_layout.addWidget(self.email_input)

        # Bouton de création de compte
        self.signup_button = QPushButton(self.tr("Créer un compte"), self)
        self.signup_button.setStyleSheet(self.button_style())
        self.signup_button.clicked.connect(self.create_account)
        form_layout.addWidget(self.signup_button)

        # Ajouter le layout du formulaire à la mise en page principale
        self.layout.addLayout(form_layout)

        # Spacer pour centrer le formulaire
        form_layout.addStretch()

    def input_style(self):
        """Retourne le style CSS pour les champs de saisie."""
        return """
            QLineEdit {
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #007BFF;
                margin-bottom: 15px;
            }
            QLineEdit:focus {
                border: 1px solid #0056b3;
            }
        """

    def button_style(self):
        """Retourne le style CSS pour le bouton."""
        return """
            QPushButton {
                background-color: #007BFF;
                color: white;
                padding: 10px;
                border-radius: 5px;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """

    def load_user_data(self):
        """Charge les données des utilisateurs depuis le fichier JSON."""
        try:
            with open('resources/data/users.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_user_data(self, user_data):
        """Enregistre les données des utilisateurs dans le fichier JSON."""
        with open('resources/data/users.json', 'w') as file:
            json.dump(user_data, file, indent=4)  # Ajouter un indent pour plus de lisibilité

    def validate_email(self, email):
        """Vérifie si l'adresse e-mail est valide."""
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(regex, email)

    def user_exists(self, username, email, user_data):
        """Vérifie si l'utilisateur ou l'e-mail existe déjà."""
        return any(user['username'] == username or user['email'] == email for user in user_data)

    def hash_password(self, password):
        """Renvoie le hash SHA256 du mot de passe."""
        return hashlib.sha256(password.encode()).hexdigest()

    def create_account(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()
        email = self.email_input.text().strip()

        if not username or not password or not confirm_password or not email:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Veuillez remplir tous les champs obligatoires."))
            return

        if password != confirm_password:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Les mots de passe ne correspondent pas."))
            return

        if len(username) < 3:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Le nom d'utilisateur doit comporter au moins 3 caractères."))
            return

        if len(password) < 6:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Le mot de passe doit comporter au moins 6 caractères."))
            return

        if not self.validate_email(email):
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Adresse e-mail invalide."))
            return

        user_data = self.load_user_data()

        if self.user_exists(username, email, user_data):
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Ce nom d'utilisateur ou cette adresse e-mail est déjà pris."))
            return

        # Chiffrement du mot de passe
        hashed_password = self.hash_password(password)

        # Enregistrer le nouvel utilisateur avec e-mail et mot de passe haché
        user_data.append({"username": username, "password": hashed_password, "email": email})
        self.save_user_data(user_data)

        # Envoi d'un e-mail de confirmation
        mailer = Mailer()
        mailer.send_email(email, 'mail1')

        QMessageBox.information(self, self.tr("Succès"), self.tr("Compte créé avec succès ! Vous pouvez maintenant vous connecter."))
        self.clear_fields()
        self.close()  # Fermez le formulaire après la création réussie du compte

    def clear_fields(self):
        """Réinitialise les champs de saisie."""
        self.username_input.clear()
        self.password_input.clear()
        self.confirm_password_input.clear()
        self.email_input.clear()
