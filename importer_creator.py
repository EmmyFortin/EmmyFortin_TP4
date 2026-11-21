from maya import cmds

# Si possible je voudrais avoir deux fichier de logique .py un pour les textures et un pour les matériaux à valider avec le prof

texture_types = {
    "Base Color" : ["basecolor", "albedo", "diffuse", "color", "diff", "dif", "d" ],
    "Normal" : ["normal", "nrm", "n" ],
    "Roughness" : ["roughness", "rough", "r"],
    "Metallic" : ["metallic", "metalness", "m"]
}