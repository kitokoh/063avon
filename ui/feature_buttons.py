from PyQt5.QtWidgets import QPushButton, QHBoxLayout
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt

class FeatureButtons(QHBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        features = [
            ("FB Robot Pro", "resources/icons/facebook-icon-png-770.png", "#E91E63"),
            ("WhatsApping", "resources/icons/whatsapp-512.png", "#4CAF50"),
            ("Blogging", "resources/icons/article-marketing-3-512.gif", "#4CAF50"),
            # Add other buttons here...
        ]

        for text, icon, color in features:
            button = QPushButton(text)
            button.setFont(QFont("Arial", 14))
            button.setIcon(QIcon(QPixmap(icon).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
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
            """)
            self.addWidget(button)

    def lighten_color(self, color):
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, r + 30)
        g = min(255, g + 30)
        b = min(255, b + 30)
        return f'#{r:02x}{g:02x}{b:02x}'
