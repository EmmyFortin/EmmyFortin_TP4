from PySide6.QtWidgets import (
    QWidget,
    QLineEdit,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QGridLayout,
    QMessageBox,
    QGroupBox,
    QComboBox,
    QStyle,
    QRadioButton,
    QFileDialog,
    QListWidget,
    QTableWidget,
    QTableWidgetItem
)
from PySide6.QtCore import Qt
import importer_creator
import os

import maya.OpenMayaUI as omui
from shiboken6 import wrapInstance

# Pour avoir la fênetre du tool always on top
def maya_main_window():
    pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(int(pointer),QWidget)


class TextureImporterMaterialCreator(QWidget):

    def __init__(self):
        super().__init__(maya_main_window())
        self.setWindowFlags(Qt.Window)
        self.source = None
        # Stock les chemins complets des textures
        self.texture_paths = []
        # Stock juste les noms des textures
        self.texture_file_names = []

        self.setWindowTitle("Texture Importer and Material Creator")
        self.setMinimumWidth(450)
        self.setMinimumHeight(500)
        self.setMaximumHeight(650)
        self.create_ui()

    def create_ui(self):

        # Création du layout principal
        self.main_layout = QVBoxLayout(self)

        # Création des 2 sections de l'outil
        self.texture_group_box = QGroupBox("Texture Importer")
        self.material_group_box = QGroupBox("Material Creator")

        # Variable pour la hauteur des champs
        self.height_value = 25
        
        # Création des layouts des group box
        self.texture_group_layout = QVBoxLayout()
        self.material_group_layout = QVBoxLayout()

        # Ajout des groups box dans les groups layout
        self.texture_group_box.setLayout(self.texture_group_layout)
        self.material_group_box.setLayout(self.material_group_layout)
        

        #### UI DU GROUP BOX TEXTURE ####

        # Label du bouton
        self.texture_files_label = QLabel("Select Texture Files")

        # Création du QPushButton pour browse les textures
        self.browse_texture_button = QPushButton("Browse Textures")
        self.browse_texture_button.setMinimumHeight(80)
        self.browse_texture_button.setIcon(
            self.style().standardIcon(QStyle.SP_DirOpenIcon)
        )

        # Création du QTableWidget pour afficher les texture sélectionné
        self.texture_table_box = QTableWidget(columnCount=2)

        # Définit les noms des colonnes
        self.texture_table_box.setHorizontalHeaderLabels([
            "Texture Name",
            "Texture Map Type"
        ])

        # Combo box qui affichera le type de texture map dans le QTableWidget
        self.texture_type_box = QComboBox()

        self.texture_table_box.setVisible(False)

        # Appelle la fonction browse_textures
        self.browse_texture_button.clicked.connect(self.browse_textures)

        # Ajoute les widgets dans le layout texture group
        self.texture_group_layout.addWidget(self.texture_files_label)
        self.texture_group_layout.addWidget(self.browse_texture_button)
        self.texture_group_layout.addWidget(self.texture_table_box)


        #### UI DU GROUP BOX MATERIAL ####

        self.material_mode_layout = QVBoxLayout()

        # Label du du layout de choix de mat
        # Trouver un meilleur label
        self.material_mode_label = QLabel("Material Mode")

        # Création des QRadioButtons
        self.radio_button_create_new_material = QRadioButton("Create New Material")
        self.radio_button_use_existing_material = QRadioButton("Use Existing Material")

        # Actif par défaut
        self.radio_button_create_new_material.setChecked(True)

        # QComboxBox et QLabel qui affiche les mat existants
        self.existing_material_box_label = QLabel("Select Existing Material")
        self.existing_material_box = QComboBox()
        self.existing_material_box.setFixedHeight(self.height_value)
        # Hidden au départ
        self.existing_material_box.setVisible(False)
        self.existing_material_box_label.setVisible(False)

        # Si on selectionne le radio button use existing mat on affiche le QComboBox
        self.radio_button_use_existing_material.toggled.connect(
            self.update_materials_fields
        )

        # Pour update le nom et le type quand on choisi un autre material dans existing_material_box
        self.existing_material_box.currentTextChanged.connect(
            self.update_materials_fields
        )

        # Ajoute les widgets dans le layout du material mode
        self.material_mode_layout.addWidget(self.material_mode_label)
        self.material_mode_layout.addWidget(self.radio_button_create_new_material)
        self.material_mode_layout.addWidget(self.radio_button_use_existing_material)
        self.material_mode_layout.addWidget(self.existing_material_box_label)
        self.material_mode_layout.addWidget(self.existing_material_box)
        

        # Layout de material type 
        self.material_type_layout = QVBoxLayout()
        self.material_type_label = QLabel("Material Type")
        self.material_name_label = QLabel("Material Name")

        # QComboBox qui affiche les material Type
        self.material_type_box = QComboBox()
        self.material_type_box.setFixedHeight(self.height_value)

        # Ajoute la liste des materials qu'on peut créer (dict material_types)
        self.material_type_box.addItems(importer_creator.material_types.keys())

        # QLineEdit du nom du material 
        self.material_name_field = QLineEdit()
        self.material_name_field.setFixedHeight(self.height_value)

        # Ajoute les widgets dans le layout du material type
        self.material_type_layout.addWidget(self.material_type_label)
        self.material_type_layout.addWidget(self.material_type_box)
        self.material_type_layout.addWidget(self.material_name_label)
        self.material_type_layout.addWidget(self.material_name_field)


        # Ajout des sous layouts dans le material group layout
        self.material_group_layout.addLayout(self.material_mode_layout)
        self.material_group_layout.addLayout(self.material_type_layout)

        # Création du QPushButton pour la création du material
        self.create_material_button = QPushButton("Create Material")

        # Ajout les widgets et les sub layout au layout
        self.main_layout.addWidget(self.texture_group_box)
        self.main_layout.addWidget(self.material_group_box)
        self.main_layout.addWidget(self.create_material_button)

    def browse_textures(self):
        """Ouvre l'explorateur pour sélectionner des textures."""

        self.texture_table_box.setVisible(True)

        files_to_browse, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Textures",
            "",
            "Image Files (*.png *.jpg *.jpeg *.tif *.tiff *.tga *.exr)"
        )

        # Si des fichiers sont browser
        if files_to_browse:
            # Garde les chemins complets
            self.texture_paths = files_to_browse

            # Récupere juste le nom des fichiers (pour afficher dans la box)
            self.texture_file_names = [os.path.basename(file) for file in files_to_browse]

            # Efface les anciennes textures sans supprimer les labels des colonnes
            self.texture_table_box.clearContents()

            # Définit le nombre de lignes selon le nombre de textures sélectionnés
            self.texture_table_box.setRowCount(len(self.texture_file_names))

            # Ajoute chaque texture sélectionnée dans la premiere colonne de la table box
            for row, file_name in enumerate(self.texture_file_names):
                self.texture_table_box.setItem(
                    row, 0, QTableWidgetItem(file_name)
                )

            # Appelle la fonction transmit_texture_info
            self.display_texture_types()


    def display_texture_types(self):
        """Détecte et affiche les types de textures sélectionnées."""

        # Pour chaque texture sélectionnée
        for row, file_name in enumerate(self.texture_file_names):
            # Récupère le type de texture détecté
            texture_type = importer_creator.detect_texture_type(file_name)

            # On ajoute les types de texture map disponible dans le texture_type_box 
            self.texture_type_box.addItems(
                ["Unknown"] + list(importer_creator.texture_types.keys())
            )

            # Détecte le texture type de la texture sélectionné
            self.texture_type_box.setCurrentText(texture_type)

            # Ajoute le QComboBox dans la deuxième colonne de la table
            self.texture_table_box.setCellWidget(row, 1, self.texture_type_box)

            # Si le type de texture détecté n'est pas connu (pas dans dict)
            # On appelle create_message avec le type de message unknown texture
            if texture_type == "Unknown":
                self.create_message("unknown_texture", file_name)

    def transmit_texture_infos(self):
        """Récupère et transmet les infos des textures."""

        # Stock les infos des textures
        texture_info = []

        # Récupère les données et les stock dans texture_info
        for row, file_path in enumerate(self.texture_paths):
            # Check toutes les textures types box (QComboBox) et les textures type
            texture_type_box = self.texture_table_box.cellWidget(row,1)
            texture_type = texture_type_box.currentText()

            # Ajout à texture_info
            texture_info.append((file_path, texture_type))

        return texture_info

    def update_materials_fields(self, checked):
        """Met à jour les champs selon le mode de matériaux choisi."""

        # Affiche ou cache le existing_material_box 
        self.existing_material_box.setVisible(checked)
        self.existing_material_box_label.setVisible(checked)

        # J'hésite à juste les hide totalement, si je les hide pas faudrait update pareil les valeurs des champs sans permettre leur modifications.

        # Active ou désactive le champ de nom (car si mat existe déjà, y déja un nom) et le material_type_box (car le type de mat est déjà définit)
        self.material_name_field.setEnabled(not checked)
        
        self.material_type_box.setEnabled(not checked)

        # J'aime pas le disable state du QLineEdit donc je le change comme css
        self.material_name_field.setStyleSheet("""
            QLineEdit:disabled {
                background-color: #4B4B4B;
                color: #999999;
                border: none;
            }
        """)

        # on doit update la liste des materials existants
        if checked:
            self.update_existing_materials()

    def update_existing_materials(self):
        """Met à jour la liste des matériaux existant dans Maya."""

        # Récupère les matériaux dans la scène avec la fonction get_existing_materials dans importer_creator
        materials = importer_creator.get_existing_materials()

        # Vide la liste pour pas avoir de double
        self.existing_material_box.clear()

        # Ajout les materiaux dans exisiting material box
        self.existing_material_box.addItems(materials)

        # Pour le material sélectionner dans le existing_material_box
        material_name = self.existing_material_box.currentText()

        if material_name:
            # Récupère le type du mat
            material_type = importer_creator.get_material_type(material_name)

            # Affiche son nom
            self.material_name_field.setText(material_name)

            # Affiche son type (check le dict material_types dans importer creator)
            for current_material_name, maya_material_type in importer_creator.material_types.items():
                if maya_material_type == material_type:
                    self.material_type_box.setCurrentText(current_material_name)
                    # on arrete quand on trouve
                    break

    def transmit_material_infos(self):
        """Récupère et transmet les infos des matériaux."""

        # Vérifie quel mode de création de matérial est choisi
        if self.radio_button_create_new_material.isChecked():
            # Récupère le type choisi dans material_type_box
            material_type = self.material_type_box.currentText()
            print(material_type)

            # Récupère le nom du nouveau material
            material_name = self.material_name_field.text().strip()

        elif self.radio_button_use_existing_material.isChecked():
            print("exist mat")

            # Récupère le nom du material existant sélectionné dans le existing material box
            material_name = self.existing_material_box.currentText()



    def create_message(self, message_type, unknown_texture_message = ""):

        if message_type == "name_warning":
            QMessageBox.warning(
                self,
                "WARNING",
                "Please add a name to your new material."

            )

        elif message_type == "unknown_texture":
            QMessageBox.warning(
                self,
                "Unknown Texture",
                f"Could not detect the texture type for : {unknown_texture_message}"
            )

        elif message_type == "done":
            QMessageBox.information(
                self,
                "Material Created",
                "Material created succesfully."
            )

    def create_material(self):
        """Récupère les infos des textures et des matériaux et créer le material."""

        # Récupère les infos des textures
        self.transmit_texture_infos()
        # Récupère les infos du material
        self.transmit_material_infos()



