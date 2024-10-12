import sys
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QFrame, QPushButton, QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal, QTranslator, QLocale, QLibraryInfo

class FooterSection(QFrame):
    # Signal émis lors du clic sur les boutons
    privacy_clicked = pyqtSignal()
    terms_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QFrame {
                border: none;
                background-color: #2E7D32;
            }
        """)

        layout = QHBoxLayout(self)

        # Création et configuration des boutons
        privacy_button = self.create_button(self.tr("Politique de confidentialité"))
        privacy_button.clicked.connect(self.on_privacy_clicked)

        terms_button = self.create_button(self.tr("Termes et Conditions"))
        terms_button.clicked.connect(self.on_terms_clicked)

        footer_text = QLabel(self.tr("Politique de confidentialité | © 2024 Nova360 Pro - Tous droits réservés."))
        footer_text.setFont(QFont("Arial", 10))
        footer_text.setAlignment(Qt.AlignCenter)
        footer_text.setStyleSheet("color: white;")

        # Ajouter les widgets au layout
        layout.addWidget(privacy_button)
        layout.addWidget(terms_button)
        layout.addWidget(footer_text)

    def create_button(self, text):
        button = QPushButton(text)
        button.setFont(QFont("Arial", 10))
        button.setStyleSheet("""
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
        return button

    def on_privacy_clicked(self):
        self.privacy_clicked.emit()  # Émettre le signal pour indiquer que le bouton a été cliqué

    def on_terms_clicked(self):
        self.terms_clicked.emit()  # Émettre le signal pour indiquer que le bouton a été cliqué


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Charger la traduction selon la langue du système
    translator = QTranslator()
    system_locale = QLocale.system().name()  # ex : 'fr_FR', 'en_US', etc.
    qm_path = f"lang/{system_locale}/ui/footer.qm"  # Chemin de ton fichier .qm

    if translator.load(qm_path):
        app.installTranslator(translator)

    # Créer et afficher la fenêtre principale
    window = FooterSection()
    window.show()

    sys.exit(app.exec_())
