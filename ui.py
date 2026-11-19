from PySide6.QtWidgets import (
    QWidget,
    QLineEdit,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QGridLayout,
    QMessageBox,
    QComboBox
)
from PySide6.QtCore import Qt
# import ficher.py jsp encore comment je vais le nommé

class TextureImporterMaterialCreator(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Texture Importer and Material Creator")
        self.setMinimumWidth(450)
        self.setMinimumHeight(350)

