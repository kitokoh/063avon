from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class UpdateMediaDialog(QDialog):
    def __init__(self, media, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f'Edit Media {media["nom"]}')
        self.media = media
        self.layout = QVBoxLayout(self)

        self.image_preview = QLabel(self)
        if media['nom'].endswith(('.png', '.jpg', '.jpeg')):
            self.image_preview.setPixmap(QPixmap(media['preview_path']).scaled(150, 150, Qt.KeepAspectRatio))
        elif media['nom'].endswith('.mp4'):
            self.image_preview.setText('Video File')
        self.layout.addWidget(self.image_preview)

        self.description_input = QLineEdit(self)
        self.description_input.setText(media['description'])
        self.layout.addWidget(self.description_input)

        self.browse_button = QPushButton('Browse Image', self)
        self.browse_button.clicked.connect(self.change_image)
        self.layout.addWidget(self.browse_button)

        self.save_button = QPushButton('Save', self)
        self.save_button.clicked.connect(self.save_changes)
        self.layout.addWidget(self.save_button)

    def change_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_name:
            self.image_preview.setPixmap(QPixmap(file_name).scaled(150, 150, Qt.KeepAspectRatio))
            self.media['preview_path'] = file_name

    def save_changes(self):
        self.media['description'] = self.description_input.text()
        self.accept()
