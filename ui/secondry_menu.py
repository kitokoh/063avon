from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal

class SecondaryMenu(QWidget):
    # Signal pour notifier un changement de contenu
    menu_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout pour le menu secondaire (horizontal)
        menu_layout = QHBoxLayout(self)

        # Bouton Instances
        instances_button = QPushButton(self.tr("Robot Pro"), self)
        instances_button.setStyleSheet("""
            QPushButton {
                background-color: #FFC107;
                color: black;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #e0a800;
            }
        """)
        instances_button.clicked.connect(lambda: self.menu_selected.emit("instances"))
        menu_layout.addWidget(instances_button)

        # Bouton Media
        media_button = QPushButton(self.tr("Marketing"), self)
        media_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        media_button.clicked.connect(lambda: self.menu_selected.emit("media"))
        menu_layout.addWidget(media_button)

        # Bouton Groupes
        groups_button = QPushButton(self.tr("On Facebook"), self)
        groups_button.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        groups_button.clicked.connect(lambda: self.menu_selected.emit("groups"))
        menu_layout.addWidget(groups_button)

        self.setLayout(menu_layout)
