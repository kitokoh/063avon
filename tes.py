import os
import json
from PyQt5.QtWidgets import (QMainWindow, QAction, QTableWidget, QTableWidgetItem, QPushButton, 
                             QFileDialog, QVBoxLayout, QWidget, QDialog, QLabel, QLineEdit, 
                             QHBoxLayout, QHeaderView, QAbstractItemView, QMessageBox, QComboBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class MediaTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Chemins corrigés pour le dossier média et le fichier JSON
        self.media_folder = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-FB-Robot', 'media', 'media1')
        self.json_file = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-FB-Robot', 'text', 'data.json')
        self.media_list = self.load_media()

        # UI Setup
        layout = QVBoxLayout(self)

        # Label "Liste des media"
        media_label = QLabel("Liste des media:", self)
        layout.addWidget(media_label)

        # Media Table
        self.table = QTableWidget(self)
        layout.addWidget(self.table)

        # Set up the table columns
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Nom', 'Description', 'Preview', 'Action'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.populate_table()

    def load_media(self):
        # Load media files from the directory
        media_files = [f for f in os.listdir(self.media_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.mp4'))]

        # Load descriptions from the JSON file
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as f:
                json_data = json.load(f)
        else:
            json_data = {'posts': []}

        # Create a list of dictionaries containing media info
        media_list = []
        for media in media_files:
            media_info = {
                'nom': media,  # Media name with extension
                'description': '',
                'preview_path': os.path.join(self.media_folder, media)  # Correct path
            }
            # Find the corresponding description in the JSON
            for post in json_data['posts']:
                if post['image'] == media_info['preview_path']:
                    media_info['description'] = post['text']
                    break
            media_list.append(media_info)

        return media_list

    def populate_table(self):
        # Populate the table with media items
        self.table.setRowCount(len(self.media_list))

        for row, media in enumerate(self.media_list):
            # Nom column (File name with extension)
            self.table.setItem(row, 0, QTableWidgetItem(media['nom']))

            # Description column
            self.table.setItem(row, 1, QTableWidgetItem(media['description']))

            # Preview column (Image or Video)
            preview_label = QLabel()
            if media['nom'].endswith(('.png', '.jpg', '.jpeg')):
                pixmap = QPixmap(media['preview_path']).scaled(100, 100, Qt.KeepAspectRatio)
                preview_label.setPixmap(pixmap)
            elif media['nom'].endswith('.mp4'):
                preview_label.setText('Video File (Click to Preview)')
                preview_label.setStyleSheet("background-color: lightgray;")
                preview_label.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(row, 2, preview_label)

            # Action column (Edit and Delete buttons)
            edit_button = QPushButton('Edit')
            edit_button.clicked.connect(lambda checked, m=media: self.update_media(m))
            self.table.setCellWidget(row, 3, edit_button)

    def update_media(self, media):
        dialog = UpdateMediaDialog(media, self)
        if dialog.exec_():  # Modal dialog
            # If user clicked Save in the dialog
            self.save_description(media)
            self.populate_table()  # Reload the table to reflect changes

    def save_description(self, media):
        # Load the existing JSON data
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as f:
                json_data = json.load(f)
        else:
            json_data = {'posts': []}

        # Update or add media entry
        for post in json_data['posts']:
            if post['image'] == media['preview_path']:
                post['text'] = media['description']
                break
        else:
            # Add new entry if not found
            json_data['posts'].append({
                'text': media['description'],
                'image': media['preview_path']
            })

        # Save back to JSON file
        with open(self.json_file, 'w') as f:
            json.dump(json_data, f, indent=4)

class UpdateMediaDialog(QDialog):
    def __init__(self, media, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f'Edit Media {media["nom"]}')
        self.media = media
        self.layout = QVBoxLayout(self)

        # Media preview
        self.image_preview = QLabel(self)
        if media['nom'].endswith(('.png', '.jpg', '.jpeg')):
            self.image_preview.setPixmap(QPixmap(media['preview_path']).scaled(150, 150, Qt.KeepAspectRatio))
        elif media['nom'].endswith('.mp4'):
            self.image_preview.setText('Video File')  # Placeholder for video files
        self.layout.addWidget(self.image_preview)

        # Description input field
        self.description_input = QLineEdit(self)
        self.description_input.setText(media['description'])
        self.layout.addWidget(self.description_input)

        # Browse button to change the image (optional feature)
        self.browse_button = QPushButton('Browse Image', self)
        self.browse_button.clicked.connect(self.change_image)
        self.layout.addWidget(self.browse_button)

        # Save button
        self.save_button = QPushButton('Save', self)
        self.save_button.clicked.connect(self.save_changes)
        self.layout.addWidget(self.save_button)

        # Delete button
        self.delete_button = QPushButton('Delete')
        self.delete_button.clicked.connect(self.delete_media)
        self.layout.addWidget(self.delete_button)

    def change_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_name:
            self.image_preview.setPixmap(QPixmap(file_name).scaled(150, 150, Qt.KeepAspectRatio))
            self.media['preview_path'] = file_name  # Update the media path with the new image path

    def save_changes(self):
        # Save the updated description
        self.media['description'] = self.description_input.text()
        # Close the dialog and return a positive response
        self.accept()

    def delete_media(self):
        response = QMessageBox.question(self, 'Confirm Delete', 
                                         f"Are you sure you want to delete {self.media['nom']}?", 
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if response == QMessageBox.Yes:
            self.reject()  # Close dialog
            # Remove media from JSON
            self.parent().remove_media(self.media)

class GroupTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        label = QLabel("Liste des Groupes:", self)
        layout.addWidget(label)

        # Placeholder content for the groups table
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Nom du Groupe', 'Action'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.populate_table()

    def populate_table(self):
        # Sample group data
        group_data = [{'name': 'Group 1'}, {'name': 'Group 2'}, {'name': 'Group 3'}]
        self.table.setRowCount(len(group_data))

        for row, group in enumerate(group_data):
            # Nom du Groupe column
            self.table.setItem(row, 0, QTableWidgetItem(group['name']))

            # Action column (Edit buttons for groups)
            edit_button = QPushButton('Edit')
            edit_button.clicked.connect(lambda checked, g=group: self.edit_group(g))
            self.table.setCellWidget(row, 1, edit_button)

    def edit_group(self, group):
        # Placeholder function to edit group
        QMessageBox.information(self, 'Edit Group', f'Edit Group: {group["name"]}')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AI FB ROBOT Pro')
        self.resize(900, 600)

        # Create Menus
        menubar = self.menuBar()

        # Media Menu
        media_menu = menubar.addMenu('Media')
        media_action = QAction('View Media', self)
        media_action.triggered.connect(self.open_media)
        media_menu.addAction(media_action)

        # Group Menu (New)
        group_menu = menubar.addMenu('Group')
        group_action = QAction('View Groups', self)
        group_action.triggered.connect(self.open_group)
        group_menu.addAction(group_action)

    def open_media(self):
        self.setCentralWidget(MediaTable(self))

    def open_group(self):
        self.setCentralWidget(GroupTable(self))

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
