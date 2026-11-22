from maya import cmds
import os
import re

# Si possible je voudrais avoir deux fichier de logique .py un pour les textures et un pour les matériaux à valider avec le prof
# Demander au prof si on est obligé de faire modification en live update car ça pourrait tout faire exploser

def detect_texture_type(file_name):
    """Détecte le type de texture à partir du nom du fichier."""

    # Récupère le file_name, retire les espaces sup, l'extension et met tout en minuscule
    file_name = os.path.splitext(file_name)[0].strip().lower()

    # Sépare différentes partie du nom pour avoir une détection plus fiable (utilisation de re )
    # on enleve les caractère spéciaux pour garder uniquement les parties du nom
    name_parts = re.split(r"[_\-\s]+", file_name)

    # Détecte le type de texture map selon le nom et le dict
    for texture_type, keynames in texture_types.items():
        # vérifie dans tout les keynames du dict car un type a plusieurs keyname
        for keyname in keynames:
            if keyname in name_parts:
                return texture_type
            
    # Si aucun keyname correspond au nom du fichier on retourne unknown
    return "Unknown"

def get_existing_materials():
    """Fonction qui récupère les matériaux déjà existant dans le fichier Maya."""

    # Récupère les materials
    materials = cmds.ls(materials=True)
    return materials

def get_material_type(material_name):
    """Récupère le type d'un material existant dans Maya."""

    return cmds.nodeType(material_name)

    





















































# Dictionnaire des types de textures possibles
# doit rajouter les préfixes pour convention UE
texture_types = {
    "Base Color" : [
        "basecolor", "base_color", "albedo", "diffuse",
        "color", "diff", "dif", "col"
    ],

    "Normal" : [
        "normal", "nrm", "normalgl",
        "normaldx","nor"
    ],

    "Roughness" : [
        "roughness", "rough", "rgh"
    ],

    "Metallic" : [
        "metallic", "metalness", "metal", "mtl"
    ],

    "Ambient Occlusion" : [
        "ao","ambient", "occlusion",
        "ambientocclusion", "ambient_occlusion"
    ],

    "Height" : [
        "height", "displacement", "disp", "heightmap"
    ],

    "Opacity" : [
        "opacity", "alpha", "transparency", "mask"

    ],

    "Emissive" : [
        "emissive", "emission", "emit"
    ],

    "Specular" : [
        "specular", "spec"
    ],

    "Glossiness" : [
        "glossiness", "gloss", "glossmap", 
        "gloss_map", "glossy"
    ],

    "ARM" : [
        "arm"
    ],

    "ORM" : [
        "orm"
    ]
}

# Dict des types de matériaux qu'on peut créer
material_types = {
    "Arnold Standard Surface" : "aiStandardSurface",
    "Standard Surface" : "standardSurface",
    "Lambert" : "lambert",
    "Blinn" : "blinn",
    "Phong" : "phong"

}