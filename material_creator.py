from maya import cmds


def get_existing_materials():
    """Fonction qui récupère les matériaux déjà existant dans le fichier Maya."""

    # Récupère les materials
    materials = cmds.ls(materials=True)
    return materials

def get_material_type(material_name):
    """Récupère le type d'un material existant dans Maya."""

    return cmds.nodeType(material_name)

# Dict des types de matériaux qu'on peut créer
material_types = {
    "Arnold Standard Surface" : "aiStandardSurface",
    "Standard Surface" : "standardSurface",
    "Lambert" : "lambert",
    "Blinn" : "blinn",
    "Phong" : "phong"

}