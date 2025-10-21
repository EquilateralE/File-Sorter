import os
import shutil

def deplacer_fichier(fichier, categorie, dossier_base="data/tries"):
    dossier_categorie = os.path.join(dossier_base, categorie)
    os.makedirs(dossier_categorie, exist_ok=True)
    shutil.move(fichier, os.path.join(dossier_categorie, os.path.basename(fichier)))
