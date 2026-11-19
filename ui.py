from PySide6.QtWidgets import (
    QWidget,
    QLineEdit,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QGridLayout,
    QMessageBox,
    QGroupBox,
    QComboBox
)
from PySide6.QtCore import Qt
import importer_creator

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

        self.setWindowTitle("Texture Importer and Material Creator")
        self.setMinimumWidth(450)
        self.setMinimumHeight(350)
        self.create_ui()

    def create_ui(self):

        # Création du layout principal
        self.main_layout = QVBoxLayout(self)
        
        # Création des 2 sections de l'outil
        self.texture_group_box = QGroupBox("Texture Importer")
        self.material_group_box = QGroupBox("Material Creator")

        # Création des layouts des group box et ajoute les group box au layout
        self.texture_group_layout = QVBoxLayout()
        self.material_group_layout = QVBoxLayout()


        # Création du QPushButton
        self.create_material_button = QPushButton("Create Material")

        # Ajout les widgets au layout
        self.main_layout.addWidget(self.texture_group_box)
        self.main_layout.addWidget(self.material_group_box)
        self.main_layout.addWidget(self.create_material_button)
        


