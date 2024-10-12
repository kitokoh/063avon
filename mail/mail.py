import smtplib
import json
import os

class Mailer:
    def __init__(self):
        """Initialise les paramètres et charge les informations nécessaires."""
        self.load_credentials()
        self.load_email_content()
        self.load_user_email()

    def load_credentials(self):
        """Charge les identifiants de connexion depuis i.txt (dans le même dossier)."""
        current_dir = os.path.dirname(os.path.abspath(__file__))  # Dossier courant de mail.py
        i_txt_path = os.path.join(current_dir, 'i.txt')

        # Lire le contenu du fichier i.txt
        self.credentials = {}
        if not os.path.exists(i_txt_path):
            raise FileNotFoundError(f"Le fichier 'i.txt' est introuvable dans {current_dir}.")
        
        with open(i_txt_path, 'r') as file:
            for line in file:
                key, value = line.strip().split('=')
                self.credentials[key] = value

        # Vérifier les identifiants nécessaires
        required_keys = ['server', 'port', 'username', 'password']
        for key in required_keys:
            if key not in self.credentials:
                raise ValueError(f"Clé {key} manquante dans le fichier 'i.txt'.")

    def load_email_content(self):
        """Charge le contenu des e-mails depuis le fichier JSON 'email_content.json'."""
        current_dir = os.path.dirname(os.path.abspath(__file__))  # Dossier courant de mail.py
        email_content_path = os.path.join(current_dir, 'email_content.json')

        if not os.path.exists(email_content_path):
            raise FileNotFoundError(f"Le fichier 'email_content.json' est introuvable dans {current_dir}.")
        
        with open(email_content_path, 'r') as file:
            self.email_content = json.load(file)

    def load_user_email(self):
        """Charge l'e-mail des utilisateurs depuis le fichier 'users.json' dans le dossier 'data'."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Dossier racine du projet
        users_path = os.path.join(project_root, 'data', 'users.json')

        if not os.path.exists(users_path):
            raise FileNotFoundError(f"Le fichier 'users.json' est introuvable dans {users_path}.")
        
        with open(users_path, 'r') as file:
            self.users = json.load(file)

    def send_email(self, username, email_type):
        """Envoie un e-mail à l'utilisateur spécifié basé sur le type d'e-mail."""
        if username not in self.users:
            print(f"L'utilisateur {username} n'existe pas dans 'users.json'.")
            return

        # Obtenir l'e-mail du client
        to_email = self.users[username]

        if email_type not in self.email_content:
            print(f"Le type d'e-mail '{email_type}' n'existe pas dans 'email_content.json'.")
            return

        # Préparer le sujet et le corps de l'e-mail
        subject = self.email_content[email_type]['subject'].format(username=username)
        body = self.email_content[email_type]['body'].format(username=username)

        # Composer l'e-mail avec un design simple
        full_message = f"From: {self.credentials['username']}\n"
        full_message += f"To: {to_email}\n"
        full_message += f"Subject: {subject}\n\n"
        full_message += f"Bonjour {username},\n\n{body}\n\n"
        full_message += f"Cordialement,\n\nNova360Pro Team\n"

        # Envoi de l'e-mail
        try:
            with smtplib.SMTP(self.credentials['server'], int(self.credentials['port'])) as server:
                server.starttls()  # Utilisation de TLS
                server.login(self.credentials['username'], self.credentials['password'])
                server.sendmail(self.credentials['username'], to_email, full_message)
                print(f"Email de type '{email_type}' envoyé à {to_email} avec succès !")
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'e-mail: {e}")

# Test du mailer en utilisant un type d'e-mail et un utilisateur spécifique
if __name__ == "__main__":
    mailer = Mailer()
    mailer.send_email(username="client1", email_type="mail1")
