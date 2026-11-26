import os 
import sys
import importlib

# Ajoute le dossier des fichiers au path 
absolute_file_path = os.path.abspath(__file__)
absolute_folder_path = os.path.dirname(absolute_file_path)
sys.path.append(absolute_folder_path)

# Fichier style
style_path = os.path.join(absolute_folder_path, "style.qss")

import ui
import texture_importer
import material_creator

# Recharge les modules
importlib.reload(texture_importer)
importlib.reload(material_creator)
importlib.reload(ui)

def main():
    global material_tool_window

    try:
        material_tool_window.close()

    except Exception:
        pass

    material_tool_window = ui.TextureImporterMaterialCreator()
    
    with open(style_path, "r", encoding="utf-8") as f:
        material_tool_window.setStyleSheet(f.read())
    material_tool_window.show()

main()