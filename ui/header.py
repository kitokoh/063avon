from PyQt5.QtWidgets import QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QFrame, QPushButton
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, pyqtSignal

class HeaderSection(QFrame):
    # Signal émis lorsque le bouton de menu est cliqué
    menu_toggled = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QFrame {
                border: 3px solid #4CAF50;
                border-radius: 10px;
                background-color: white;
                box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.2);
            }
        """)
        layout = QHBoxLayout(self)

        title_label = QLabel(self.tr("AI Marketing Automation"))
        title_label.setFont(QFont("Arial", 28, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2E7D32; padding: 10px;")
        layout.addWidget(title_label)

        # Logo du menu
        menu_logo_label = QLabel(self)
        menu_pixmap = QPixmap("resources/icons/robot-icons-30497.png")
        menu_logo_label.setPixmap(menu_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        menu_logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(menu_logo_label)

        # Nom de l'application et slogan
        app_info_layout = QVBoxLayout()
        app_name_label = QLabel(self.tr("Nova360 AI"))
        app_name_label.setFont(QFont("Arial", 24, QFont.Bold))
        app_name_label.setAlignment(Qt.AlignCenter)
        app_name_label.setStyleSheet("color: #2E7D32;")
        app_info_layout.addWidget(app_name_label)

        subtitle_label = QLabel(self.tr("AI Marketing & Management Auto"))
        subtitle_label.setFont(QFont("Arial", 12))
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #555555;")
        app_info_layout.addWidget(subtitle_label)
        layout.addLayout(app_info_layout)

        # Logo GIF (plus grand)
        gif_logo_label = QLabel(self)
        gif_pixmap = QPixmap("resources/icons/robot-256.gif")
        gif_logo_label.setPixmap(gif_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        gif_logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(gif_logo_label)

        # Barre de recherche
        search_bar = QLineEdit()
        search_bar.setPlaceholderText(self.tr("Rechercher..."))
        search_bar.setFont(QFont("Arial", 14))
        search_bar.setStyleSheet("""
            QLineEdit {
                border: 2px solid #CCCCCC;
                border-radius: 8px;
                padding: 8px;
                background-color: white;
            }
        """)
        layout.addWidget(search_bar)

        # Bouton de menu toggle
        toggle_button = self.create_button(self.tr("≡"), "resources/icons/menu-icon.png", 24)
        toggle_button.clicked.connect(self.on_toggle_clicked)
        layout.addWidget(toggle_button)

    def create_button(self, text, icon_path, icon_size):
        button = QPushButton(text)
        button.setFont(QFont("Arial", 16, QFont.Bold))
        button.setIcon(QIcon(QPixmap(icon_path).scaled(icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        button.setStyleSheet("""
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
        return button

    def on_toggle_clicked(self):
        self.menu_toggled.emit()  # Émettre le signal lorsque le bouton de menu est cliqué
