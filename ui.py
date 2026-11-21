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
    QListWidget
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

        self.setWindowTitle("Texture Importer and Material Creator")
        self.setMinimumWidth(450)
        self.setMinimumHeight(480)
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

        # Création du QListWidget pour afficher les texture sélectionné
        self.texture_list_box = QListWidget()
        self.texture_list_box.setVisible(False)

        # Appelle la fonction browse_textures
        self.browse_texture_button.clicked.connect(self.browse_textures)

        # Ajoute les widgets dans le layout texture group
        self.texture_group_layout.addWidget(self.texture_files_label)
        self.texture_group_layout.addWidget(self.browse_texture_button)
        self.texture_group_layout.addWidget(self.texture_list_box)


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

        # QComboxBox qui affiche les mat existants
        self.existing_material_box = QComboBox()
        self.existing_material_box.setFixedHeight(self.height_value)
        # Hidden au départ
        self.existing_material_box.setVisible(False)

        # Si on selectionne le radio button use existing mat on affiche le QComboBox
        self.radio_button_use_existing_material.toggled.connect(
            self.existing_material_box.setVisible
        )

        # Ajoute les widgets dans le layout du material mode
        self.material_mode_layout.addWidget(self.material_mode_label)
        self.material_mode_layout.addWidget(self.radio_button_create_new_material)
        self.material_mode_layout.addWidget(self.radio_button_use_existing_material)
        self.material_mode_layout.addWidget(self.existing_material_box)

        # Layout de material type 
        self.material_type_layout = QVBoxLayout()
        self.material_type_label = QLabel("Material Type")
        self.material_name_label = QLabel("Material Name")

        # QComboBox qui affiche les material Type
        self.material_type_box = QComboBox()
        self.material_type_box.setFixedHeight(self.height_value)

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

        self.texture_list_box.setVisible(True)

        files_to_browse, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Textures",
            "",
            "Image Files (*.png *.jpg *.jpeg *.tif *.tiff *.tga *.exr)"
        )

        if files_to_browse:
            # Garde les chemins complets
            self.texture_paths = files_to_browse

            # Récupere juste le nom des fichiers (pour afficher dans la box)
            texture_file_names = [os.path.basename(file) for file in files_to_browse]

            # Affiche les noms dans QListWidget
            self.texture_list_box.clear()

            # Ajoute les files sélectionner à la liste de texture
            self.texture_list_box.addItems(texture_file_names)




    def create_message(self, message_type):

        if message_type == "name_warning":
            QMessageBox.warning(
                self,
                "WARNING",
                "Please add a name to your new material."

            )

        elif message_type == "done":
            QMessageBox.information(
                self,
                "Material Created",
                "Material created succesfully."
            )
        


