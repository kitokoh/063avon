import os
import shutil
from PyQt5.QtWidgets import QFileDialog, QMessageBox

class AddMedia:
    def __init__(self, media_folder):
        self.media_folder = media_folder

    def add_media(self):
        # Options de la boîte de dialogue
        options = QFileDialog.Options()
        options |= QFileDialog.ExistingFiles

        # Boîte de dialogue pour sélectionner des fichiers
        files, _ = QFileDialog.getOpenFileNames(None, self.tr("Sélectionnez les fichiers à ajouter"), "", 
                                                self.tr("Images (*.png *.jpg *.jpeg);;Vidéos (*.mp4);;Tous les fichiers (*)"), options=options)
        if files:
            self._move_and_rename_files(files)

    def _move_and_rename_files(self, files):
        try:
            # Vérifier les fichiers existants dans le dossier des médias
            existing_files = [f for f in os.listdir(self.media_folder) if f.split('.')[0].isdigit()]
            max_number = max([int(f.split('.')[0]) for f in existing_files], default=0)

            # Déplacer et renommer les fichiers
            for file in files:
                max_number += 1
                new_file_name = f"{max_number}{os.path.splitext(file)[1]}"
                new_file_path = os.path.join(self.media_folder, new_file_name)
                shutil.copy(file, new_file_path)

            # Afficher un message de confirmation
            QMessageBox.information(None, self.tr("Médias ajoutés"), 
                                    self.tr(f"{len(files)} fichiers ont été ajoutés avec succès!"), QMessageBox.Ok)

        except Exception as e:
            # Gérer les erreurs et afficher un message d'erreur
            QMessageBox.critical(None, self.tr("Erreur"), 
                                 self.tr(f"Une erreur est survenue lors de l'ajout des fichiers : {str(e)}"), QMessageBox.Ok)

    def tr(self, message):
        # Méthode pour la traduction
        return message
