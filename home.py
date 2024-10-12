import sys
import subprocess

from PyQt5.QtWidgets import (
    QApplication, QAction, QMainWindow, QLabel, QPushButton, QVBoxLayout, 
    QHBoxLayout, QWidget, QLineEdit, QScrollArea, QFrame, QMenu, QMenuBar, QMessageBox
)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from main_fb_robot import FaceMainWindow  # Importez votre page d'accueil

class HomePage(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuration principale de la fenêtre
        self.setWindowTitle("AI FB ROBOT PRO - Marketing Automation")
        self.setGeometry(100, 100, 1280, 800)  # Taille de la fenêtre
        self.setStyleSheet("background-color: #F5F5F5;")
        # Définir l'icône de la fenêtre
        self.setWindowIcon(QIcon('resources/icons/robot-icons-30497.png'))  # Spécifiez le chemin de l'icône

        # Créer un widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layout principal en vertical
        main_layout = QVBoxLayout()

        # Menu en-tête
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        # Ajouter des menus à la barre de menu
        file_menu = self.menu_bar.addMenu("Fichier")
        edit_menu = self.menu_bar.addMenu("Édition")
        view_menu = self.menu_bar.addMenu("Vue")
        settings_menu = self.menu_bar.addMenu("Paramètres")

        # Créer des actions de menu
        exit_action = QAction("Quitter", self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction("Nouvelle")
        file_menu.addAction("Ouvrir")
        file_menu.addAction(exit_action)

        edit_menu.addAction("Copier")
        edit_menu.addAction("Coller")

        view_menu.addAction("Aperçu")
        
        # Action pour changer de thème
        theme_action = QAction("Changer de thème", self)
        theme_action.triggered.connect(self.change_theme)
        settings_menu.addAction(theme_action)

        # Layout pour l'en-tête
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(10, 10, 10, 10)

        # Ajouter un cadre 3D pour l'en-tête
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                border: 3px solid #4CAF50;
                border-radius: 10px;
                background-color: white;
                box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.2);
            }
        """)
        header_frame.setLayout(header_layout)

        # Titre de l'application
        title_label = QLabel("AI Marketing Automation")
        title_label.setFont(QFont("Arial", 28, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2E7D32; padding: 10px;")
        header_layout.addWidget(title_label)

        # Logo du menu
        menu_logo_label = QLabel(self)
        menu_pixmap = QPixmap("resources/icons/robot-icons-30497.png")
        menu_logo_label.setPixmap(menu_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        menu_logo_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(menu_logo_label)

        # Nom de l'application et slogan
        app_info_layout = QVBoxLayout()
        app_name_label = QLabel("Nova360 AI")
        app_name_label.setFont(QFont("Arial", 24, QFont.Bold))
        app_name_label.setAlignment(Qt.AlignCenter)
        app_name_label.setStyleSheet("color: #2E7D32;")
        app_info_layout.addWidget(app_name_label)

        # Slogan mis à jour
        subtitle_label = QLabel("AI Marketing & Management Auto") 
        subtitle_label.setFont(QFont("Arial", 12))
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #555555;")
        app_info_layout.addWidget(subtitle_label)

        header_layout.addLayout(app_info_layout)

        # Logo GIF (plus grand)
        gif_logo_label = QLabel(self)
        gif_pixmap = QPixmap("resources/icons/robot-256.gif")  
        gif_logo_label.setPixmap(gif_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        gif_logo_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(gif_logo_label)

        # Barre de recherche
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Rechercher...")
        search_bar.setFont(QFont("Arial", 14))
        search_bar.setStyleSheet("""
            QLineEdit {
                border: 2px solid #CCCCCC;
                border-radius: 8px;
                padding: 8px;  
                background-color: white;
            }
        """)
        header_layout.addWidget(search_bar)

        # Bouton de menu toggle
        toggle_button = QPushButton("≡")
        toggle_button.setFont(QFont("Arial", 16, QFont.Bold))
        toggle_button.setIcon(QIcon(QPixmap("resources/icons/menu-icon.png").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #2E7D32;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        toggle_button.clicked.connect(self.toggle_side_menu)
        header_layout.addWidget(toggle_button)

        # Ajouter l'en-tête au layout principal
        main_layout.addWidget(header_frame)

        # Espacement avant les boutons
        main_layout.addSpacing(20)

        # Menu latéral rétractable
        self.side_menu = QWidget(self)
        self.side_menu.setGeometry(0, 80, 200, 600)  # Positionné un peu plus haut
        self.side_menu.setStyleSheet("""
            QWidget {
                background-color: #4CAF50;
            }
            QPushButton {
                background-color: #66BB6A;
                color: white;
                border: none;
                padding: 15px;
                text-align: left;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #81C784;
            }
        """)
        self.side_menu.setVisible(False)  # Cache le menu latéral au départ

        self.side_menu_animation = QPropertyAnimation(self.side_menu, b"geometry")
        self.side_menu_animation.setDuration(500)
        self.side_menu_animation.setEasingCurve(QEasingCurve.InOutQuad)

        # Ajouter des boutons au menu latéral
        side_menu_layout = QVBoxLayout()
        side_menu_layout.setContentsMargins(10, 10, 10, 10)
        self.side_menu.setLayout(side_menu_layout)

        # Boutons du menu latéral
        side_buttons = [
            ("Accueil", "resources/icons/home-icon.png"),
            ("Paramètres", "resources/icons/settings-icon.png"),
            ("Aide", "resources/icons/help-icon.png"),
            ("À propos", "resources/icons/info-icon.png"),
            ("Quitter", "resources/icons/exit-icon.png"),
        ]

        for text, icon in side_buttons:
            button = QPushButton(text)
            button.setFont(QFont("Arial", 14))
            button.setIcon(QIcon(QPixmap(icon).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
            button.setIconSize(QPixmap(icon).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation).size())
            button.clicked.connect(lambda _, btn=text: self.side_menu_action(btn))
            side_menu_layout.addWidget(button)

        # Layout pour les icônes et boutons du milieu
        middle_layout = QHBoxLayout()

        # Liste des fonctionnalités avec leurs icônes et couleur
        features = [
            ("FB Robot Pro", "resources/icons/facebook-icon-png-770.png", "#E91E63", self.open_facebook),
            ("WhatsApping", "resources/icons/whatsapp-512.png", "#4CAF50", self.open_whatsapp),
            ("Blogging", "resources/icons/article-marketing-3-512.gif", "#4CAF50", self.open_blogging),
            ("Insta Pro", "resources/icons/pink-message-icon-12055.png", "#4CAF50", self.open_instagram),
            ("Ads Pro", "resources/icons/promotion-icon-png-3422.png", "#4CAF50", self.open_whatsapp),
            ("Branding", "resources/icons/robotic-process-automation.png", "#4CAF50", self.open_whatsapp),
            ("Emailing", "resources/icons/pink-message-icon-12045.png", "#4CAF50", self.open_whatsapp),
        ]


        # Ajouter des boutons avec animation et icônes dynamiques
        for text, icon, color, func in features:
            button = QPushButton(text)
            button.setFont(QFont("Arial", 14))  # Taille de police réduite
            button.setIcon(QIcon(QPixmap(icon).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)))  # Icônes plus petites
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: 2px solid #CCCCCC;
                    border-radius: 15px;
                    padding: 10px;
                    min-width: 150px;
                    min-height: 150px;
                }}
                QPushButton:hover {{
                    background-color: {self.lighten_color(color)};
                    transform: scale(1.05); 
                }}
                QPushButton:pressed {{
                    background-color: {color};
                }}
            """)
            button.clicked.connect(func)  # Connecter chaque bouton à sa fonction respective

            middle_layout.addWidget(button)

        main_layout.addLayout(middle_layout)

        # Duplication des boutons avec modifications
        duplicate_features = [
            ("Twitter Bot", "resources/icons/twitter-icon.png", "#1DA1F2"),
            ("LinkedIn Pro", "resources/icons/linkedin-icon.png", "#0077B5"),
            ("Pinterest Bot", "resources/icons/pinterest-icon.png", "#BD081C"),
            ("Snapchat Bot", "resources/icons/snapchat-icon.png", "#FFFC00"),
            ("TikTok Pro", "resources/icons/tiktok-icon.png", "#010101"),
            ("Reddit Bot", "resources/icons/reddit-icon.png", "#FF4500"),
            ("YouTube Pro", "resources/icons/youtube-icon.png", "#FF0000"),
        ]

        duplicate_layout = QHBoxLayout()

        for text, icon, color in duplicate_features:
            button = QPushButton(text)
            button.setFont(QFont("Arial", 14))  # Taille de police réduite
            button.setIcon(QIcon(QPixmap(icon).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)))  # Icônes plus petites
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: 2px solid #CCCCCC;
                    border-radius: 15px;
                    padding: 10px;
                    min-width: 150px;
                    min-height: 150px;
                }}
                QPushButton:hover {{
                    background-color: {self.lighten_color(color)};
                    transform: scale(1.05); 
                }}
                QPushButton:pressed {{
                    background-color: {color};
                }}
            """)
            duplicate_layout.addWidget(button)

        main_layout.addLayout(duplicate_layout)

        # Ajouter un titre "Gestion Auto"
        gestion_auto_label = QLabel("Gestion Auto")
        gestion_auto_label.setFont(QFont("Arial", 20, QFont.Bold))
        gestion_auto_label.setAlignment(Qt.AlignCenter)
        gestion_auto_label.setStyleSheet("color: #2E7D32;")
        main_layout.addWidget(gestion_auto_label)

        # Section des boutons du bas
        bottom_layout = QHBoxLayout()

        bottom_buttons = [
            ("Chat Bot", "#4CAF50"),
            ("Auto GES", "#4CAF50"),
            ("Whats Contact", "#4CAF50"),
            ("GES Auto", "#4CAF50"),
            ("SAV", "#E91E63"),
            ("ERP", "#4CAF50"),
            ("GÉD360", "#E91E63")
        ]

        for text, color in bottom_buttons:
            button = QPushButton(text)
            button.setFont(QFont("Arial", 14))
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    padding: 20px;
                    border-radius: 15px;
                }}
                QPushButton:hover {{
                    background-color: {self.lighten_color(color)};
                    transform: scale(1.05);
                }}
            """)
            button.clicked.connect(lambda _, btn=text: self.show_message(btn))  
            bottom_layout.addWidget(button)

        main_layout.addLayout(bottom_layout)

        # Créer un pied de page modernisé
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(10, 10, 10, 10)

        footer_frame = QFrame()
        footer_frame.setStyleSheet("""
            QFrame {
                border: none;
                background-color: #2E7D32;
            }
        """)
        footer_frame.setLayout(footer_layout)

        # Texte du footer
        footer_text = QLabel("Politique de confidentialité | © 2024 Nova360 Pro - Tous droits réservés")
        footer_text.setFont(QFont("Arial", 10))
        footer_text.setAlignment(Qt.AlignCenter)
        footer_text.setStyleSheet("color: white;")

        # Boutons dans le footer
        privacy_button = QPushButton("Politique de confidentialité")
        privacy_button.setFont(QFont("Arial", 10))
        privacy_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #81C784;
            }
        """)
        privacy_button.clicked.connect(lambda: self.open_link("https://www.example.com/privacy"))

        terms_button = QPushButton("Termes et Conditions")
        terms_button.setFont(QFont("Arial", 10))
        terms_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #81C784;
            }
        """)
        terms_button.clicked.connect(lambda: self.open_link("https://www.example.com/terms"))

        footer_layout.addWidget(privacy_button)
        footer_layout.addWidget(footer_text)
        footer_layout.addWidget(terms_button)

        main_layout.addWidget(footer_frame)

        # Ajouter le layout principal au widget central
        central_widget.setLayout(main_layout)

        self.show()
# Fonction pour ouvrir Facebook Robot
    def open_nova360(self):
        #self.hide()  # Masquer le module de connexion
        self.home_page = HomePage()  # Remplacez ceci par votre classe de page d'accueil
        self.home_page.show()  # Afficher la page d'accueil
    def open_facebook(self):
        #self.hide()  # Masquer le module de connexion
        self.face_main = FaceMainWindow()  # Remplacez ceci par votre classe de page d'accueil
        self.face_main.show()  # Afficher la page d'accueil
        # subprocess.Popen([sys.executable, "main_fb_robot.py"])

    # Fonction pour ouvrir WhatsApping
    def open_whatsapp(self):
        subprocess.Popen([sys.executable, "whatsapp.py"])

    # Fonction pour ouvrir Blogging
    def open_blogging(self):
        subprocess.Popen([sys.executable, "blogging.py"])

    # Fonction pour ouvrir Insta Pro
    def open_instagram(self):
        subprocess.Popen([sys.executable, "insta_pro.py"])
    def lighten_color(self, color):
        # Fonction pour éclaircir une couleur
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, r + 30)
        g = min(255, g + 30)
        b = min(255, b + 30)
        return f'#{r:02x}{g:02x}{b:02x}'

    def toggle_side_menu(self):
        # Animation pour afficher ou masquer le menu latéral
        if self.side_menu.isVisible():
            self.side_menu_animation.setStartValue(QRect(0, 80, 200, 600))
            self.side_menu_animation.setEndValue(QRect(0, 80, 0, 600))
            self.side_menu_animation.start()
            self.side_menu.setVisible(False)
        else:
            self.side_menu.setVisible(True)
            self.side_menu_animation.setStartValue(QRect(0, 80, 0, 600))
            self.side_menu_animation.setEndValue(QRect(0, 80, 200, 600))
            self.side_menu_animation.start()

    def show_message(self, button_text):
        # Afficher un message lorsque l'un des boutons est cliqué
        QMessageBox.information(self, "Info", f"Vous avez cliqué sur {button_text}!")

    def open_link(self, url):
        # Ouvrir un lien dans le navigateur par défaut
        import webbrowser
        webbrowser.open(url)

    def side_menu_action(self, action):
        # Actions pour les boutons du menu latéral
        if action == "Accueil":
            QMessageBox.information(self, "Accueil", "Bienvenue à l'accueil!")
        elif action == "Paramètres":
            QMessageBox.information(self, "Paramètres", "Ouvrir les paramètres...")
        elif action == "Aide":
            QMessageBox.information(self, "Aide", "Ouvrir l'aide...")
        elif action == "À propos":
            QMessageBox.information(self, "À propos", "AI FB ROBOT PRO v1.0\n© 2024 Nova360 Pro")
        elif action == "Quitter":
            self.close()

    def change_theme(self):
        # Changer de thème (exemple simple)
        current_color = self.centralWidget().styleSheet()
        new_color = "#2196F3" if "background-color: #F5F5F5;" in current_color else "#F5F5F5"
        self.setStyleSheet(f"background-color: {new_color};")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomePage()
    sys.exit(app.exec_())
