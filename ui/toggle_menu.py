from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import QRect, QPropertyAnimation, QEasingCurve

class ToggleMenu(QWidget):
    def __init__(self, parent=None):
        super(ToggleMenu, self).__init__(parent)

        self.setGeometry(0, 80, 200, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #4CAF50; /* Couleur de fond principale */
                border: 1px solid #388E3C; /* Bordure pour un meilleur contraste */
                border-radius: 10px; /* Coins arrondis */
            }
            QPushButton {
                background-color: #66BB6A; /* Couleur des boutons */
                color: white;
                border: none;
                padding: 15px;
                text-align: left;
                font-size: 16px;
                border-radius: 5px; /* Coins arrondis pour les boutons */
            }
            QPushButton:hover {
                background-color: #81C784; /* Couleur au survol */
            }
        """)

        # Layout du menu toggle
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # Exemple de boutons avec traduction
        buttons = [
            (self.tr("Accueil"), "home"),
            (self.tr("Paramètres"), "settings"),
            (self.tr("Aide"), "help"),
            (self.tr("À propos"), "info"),
            (self.tr("Quitter"), "exit")
        ]

        for text, icon in buttons:
            button = QPushButton(text)
            layout.addWidget(button)

        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

    def toggle(self):
        if self.isVisible():
            self.animation.setStartValue(QRect(0, 80, 200, 600))
            self.animation.setEndValue(QRect(0, 80, 0, 600))
            self.animation.start()
            self.setVisible(False)
        else:
            self.setVisible(True)
            self.animation.setStartValue(QRect(0, 80, 0, 600))
            self.animation.setEndValue(QRect(0, 80, 200, 600))
            self.animation.start()
