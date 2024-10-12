import json
import csv
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton,
                             QHeaderView, QAbstractItemView, QLineEdit, QHBoxLayout, QCheckBox,
                             QMenu, QAction, QDialog, QFormLayout, QDialogButtonBox, QMessageBox)
from PyQt5.QtCore import Qt  
from group_manager import GroupTable
# Import du header, footer et menu secondaire
from ui.header import HeaderSection  
from ui.footer import FooterSection  
from ui.secondry_menu import SecondaryMenu  

class EditInstanceDialog(QDialog):
    def __init__(self, instance, parent=None):
        super().__init__(parent)
        self.instance = instance
        self.setWindowTitle("Éditer Instance")
        self.layout = QFormLayout(self)



        self.name_field = QLineEdit(instance['name'])
        self.description_field = QLineEdit(instance['description'])
        self.user_field = QLineEdit(instance['user'])
        self.expire_date_field = QLineEdit(instance['expire_date'])

        self.layout.addRow("Nom :", self.name_field)
        self.layout.addRow("Description :", self.description_field)
        self.layout.addRow("Utilisateur :", self.user_field)
        self.layout.addRow("Date d'expiration :", self.expire_date_field)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def get_instance_data(self):
        return {
            "name": self.name_field.text(),
            "description": self.description_field.text(),
            "user": self.user_field.text(),
            "expire_date": self.expire_date_field.text()
        }

class InstanceTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.instance_list = self.load_instances()  # Charger les instances
        self.visible_columns = ['Select', 'Nom Instance', 'Description', 'User', 'Expire Date', 'Actions']

        layout = QVBoxLayout(self)


        # Ajouter le header
        header = HeaderSection(self)
        layout.addWidget(header)

        # Menu secondaire
        self.secondary_menu = SecondaryMenu(self)
        self.secondary_menu.menu_selected.connect(self.change_content)
        layout.addWidget(self.secondary_menu)

        # Disposition en haut pour le titre, la barre de recherche et les boutons
        top_layout = QHBoxLayout()

        # Titre
        instance_label = QLabel("Liste des Instances:", self)
        instance_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        top_layout.addWidget(instance_label)

        # Barre de recherche
        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderText("Rechercher dans les instances...")
        self.search_field.textChanged.connect(self.filter_table)
        self.search_field.setStyleSheet("padding: 5px; font-size: 14px;")
        top_layout.addWidget(self.search_field)

        # Bouton Ajouter Instance
        self.add_instance_button = QPushButton('Ajouter Instance', self)
        self.add_instance_button.setStyleSheet("background-color: #28a745; color: white; padding: 5px 10px;")
        self.add_instance_button.clicked.connect(self.add_new_instance)
        top_layout.addWidget(self.add_instance_button)

        # Bouton Exporter CSV
        self.export_button = QPushButton('Exporter CSV', self)
        self.export_button.setStyleSheet("background-color: #17a2b8; color: white; padding: 5px 10px;")
        self.export_button.clicked.connect(self.export_to_csv)
        top_layout.addWidget(self.export_button)

        layout.addLayout(top_layout)

        # Tableau d'instances
        self.table = QTableWidget(self)
        self.table.setColumnCount(len(self.visible_columns))  
        self.table.setHorizontalHeaderLabels(self.visible_columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setStyleSheet(""" 
            QTableWidget { 
                font-size: 14px; 
            } 
            QHeaderView::section { 
                background-color: #007BFF; 
                color: white; 
                padding: 10px; 
            } 
        """)
        layout.addWidget(self.table)

        # Charger les données dans le tableau
        self.populate_table()  

        # Ajouter le footer
        footer = FooterSection(self)
        layout.addWidget(footer)

    def load_instances(self):
        try:
            with open('resources/data/instances.json', 'r') as f:
                data = json.load(f)
                return data.get("instances", [])  
        except (FileNotFoundError, json.JSONDecodeError):
            print("Erreur lors du chargement du fichier 'instances.json'.")
            return []

    def save_instances(self):
        try:
            with open('resources/data/instances.json', 'w') as f:
                json.dump({"instances": self.instance_list}, f, indent=4)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des instances: {e}")

    def populate_table(self):
        self.table.setRowCount(len(self.instance_list))  
        for row, instance in enumerate(self.instance_list):
            if isinstance(instance, dict):  
                # Case à cocher pour la sélection
                checkbox = QCheckBox()
                self.table.setCellWidget(row, 0, checkbox)

                # Remplir les colonnes
                self.table.setItem(row, 1, QTableWidgetItem(instance.get('name', '')))
                self.table.setItem(row, 2, QTableWidgetItem(instance.get('description', '')))
                self.table.setItem(row, 3, QTableWidgetItem(instance.get('user', '')))
                self.table.setItem(row, 4, QTableWidgetItem(instance.get('expire_date', '')))

                # Bouton d'actions (Mise à jour de la licence / Éditer)
                action_button = QPushButton('Actions')
                action_menu = QMenu(self)
                update_license_action = QAction('Mettre à jour la licence', self)
                edit_action = QAction('Start', self)
                action_menu.addAction(update_license_action)
                action_menu.addAction(edit_action)
                action_button.setMenu(action_menu)
                self.table.setCellWidget(row, 5, action_button)

                # Connexion des actions
                update_license_action.triggered.connect(self.update_license)
                edit_action.triggered.connect(self.edit_instance)
            else:
                print(f"Warning: The instance at row {row} is not a dictionary. Skipping...")

    def filter_table(self):
        filter_text = self.search_field.text().lower()
        filtered_instances = [instance for instance in self.instance_list if filter_text in instance.get('name', '').lower()]
        self.table.setRowCount(len(filtered_instances))  
        for row, instance in enumerate(filtered_instances):
            self.table.setItem(row, 1, QTableWidgetItem(instance.get('name', '')))
            self.table.setItem(row, 2, QTableWidgetItem(instance.get('description', '')))
            self.table.setItem(row, 3, QTableWidgetItem(instance.get('user', '')))
            self.table.setItem(row, 4, QTableWidgetItem(instance.get('expire_date', '')))

    def add_new_instance(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        checkbox = QCheckBox()
        self.table.setCellWidget(row_position, 0, checkbox)

        for col in range(1, 5):
            self.table.setItem(row_position, col, QTableWidgetItem("")) 

        action_button = QPushButton('Actions')
        action_menu = QMenu(self)
        update_license_action = QAction('Mettre à jour la licence', self)
        edit_action = QAction('Éditer', self)
        action_menu.addAction(update_license_action)
        action_menu.addAction(edit_action)
        action_button.setMenu(action_menu)
        self.table.setCellWidget(row_position, 5, action_button)

        # Connexion des actions
        update_license_action.triggered.connect(self.update_license)
        edit_action.triggered.connect(self.edit_instance)

    def export_to_csv(self):
        try:
            with open('data/instances.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Nom', 'Description', 'User', 'Expire Date'])  # Écrire l'en-tête
                for instance in self.instance_list:
                    writer.writerow([instance['name'], instance['description'], instance['user'], instance['expire_date']])
            QMessageBox.information(self, "Succès", "Les données ont été exportées avec succès au format CSV.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'exportation : {e}")

    def contact_support(self):
        # Implémenter une fonction pour contacter le support
        print("Contacter le support...")

    def update_license(self):
        selected_rows = self.table.selectionModel().selectedRows()
        for row in selected_rows:
            instance_name = self.table.item(row.row(), 1).text()  
            print(f"Mise à jour de la licence pour l'instance : {instance_name}")

    def edit_instance(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Avertissement", "Veuillez sélectionner une instance à éditer.")
            return
        row = selected_rows[0].row()
        instance_data = {
            "name": self.table.item(row, 1).text(),
            "description": self.table.item(row, 2).text(),
            "user": self.table.item(row, 3).text(),
            "expire_date": self.table.item(row, 4).text()
        }
        dialog = EditInstanceDialog(instance_data, self)
        if dialog.exec_() == QDialog.Accepted:
            updated_instance = dialog.get_instance_data()
            self.instance_list[row] = updated_instance
            self.populate_table()  
            self.save_instances()  

    def change_content(self, menu_name):
        if menu_name == "instances":
            self.populate_table()  # Affiche la table des instances
        elif menu_name == "media":
            self.display_media()  # Ajoutez le code pour afficher les médias
        elif menu_name == "groups":
            self.display_groups()  # Ajoutez le code pour afficher les groupes

    def display_media(self):
        # Code pour afficher la liste des médias
        print("Affichage de la liste des médias...")

    def display_groups(self):
        # Code pour afficher la liste des groupes
        #self.setCentralWidget(GroupTable(self))  # Affiche la table des groupes

        print("Affichage de la liste des groupes...")

# N'oubliez pas d'importer QApplication et d'initialiser votre application
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = InstanceTable()
    window.show()
    sys.exit(app.exec_())
