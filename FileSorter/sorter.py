import os
import shutil
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image

import google.generativeai as genai

# === CONFIGURATION ===
# Mets ta clé Gemini ici (ou utilise une variable d'env si tu préfères)
GEMINI_API_KEY = "AIzaSyA0ktkRTY0PWrWderiFTdKPERaTBjVnOGY"  # <--- Mets ta clé ici !
BASE_DIR = os.path.join("data", "tries")
os.makedirs(BASE_DIR, exist_ok=True)

genai.configure(api_key=GEMINI_API_KEY)

# === IA - GEMINI IMAGE ===
def classer_image_gemini(image_path):
    try:
        img = Image.open(image_path)
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        prompt = (
            "Classifie cette image dans l'une de ces catégories : Personnages, Objet, Autre.\n"
            "Décris simplement ce que tu vois, puis réponds uniquement par le nom de la catégorie la plus appropriée.\n"
            "Exemple :\n"
            " - Un portrait, une scène avec une personne = Personnages\n"
            " - Un objet seul (arme, artefact, outil, etc.) = Objet\n"
            " - Un paysage, une scène abstraite, tout autre cas = Autre\n"
            "Indique juste : Personnages, Objet, ou Autre."
        )
        response = model.generate_content([prompt, img])
        text = response.text.strip()
        print("Réponse Gemini (image) :", text)
        if "personnage" in text.lower():
            return "Personnages", text
        elif "objet" in text.lower():
            return "Objet", text
        else:
            return "Autre", text
    except Exception as e:
        print("Erreur Gemini image :", e)
        return "Autre", "Erreur Gemini"

# === IA - GEMINI TEXTE ===
def classer_texte_gemini(texte):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        prompt = (
            "Ce texte est-il un chapitre de roman, ou autre chose ? "
            "Réponds uniquement par Chapitres ou Autres.\n\nTexte :\n" + texte[:1200]
        )
        response = model.generate_content(prompt)
        text = response.text.strip()
        print("Réponse Gemini (texte) :", text)
        if "chapitre" in text.lower():
            return "Chapitres", text
        else:
            return "Autres", text
    except Exception as e:
        print("Erreur Gemini texte :", e)
        return "Autres", "Erreur Gemini"

# === FONCTION DE TRI PRINCIPALE ===
def lire_texte_fichier(fichier):
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            contenu = f.read()
        return contenu
    except Exception as e:
        raise Exception(f"Erreur lecture fichier : {e}")

def lire_docx_fichier(fichier):
    from docx import Document
    doc = Document(fichier)
    texte = ""
    for para in doc.paragraphs:
        texte += para.text + "\n"
    return texte


def classer_fichier(fichier):
    ext = os.path.splitext(fichier)[1].lower()
    nom_fichier = os.path.basename(fichier)

    if ext in (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"):
        sous_cat, label = classer_image_gemini(fichier)
        categorie = os.path.join("Image", sous_cat)
    elif ext in (".txt", ".md"):
        contenu = lire_texte_fichier(fichier)
        categorie, label = classer_texte_gemini(contenu)
    elif ext == ".docx":
        contenu = lire_docx_fichier(fichier)
        categorie, label = classer_texte_gemini(contenu)
    else:
        categorie, label = "Autres", "Fichier non analysé"

    # Déplacement dans le dossier
    dossier_categorie = os.path.join(BASE_DIR, categorie)
    os.makedirs(dossier_categorie, exist_ok=True)
    dest = os.path.join(dossier_categorie, nom_fichier)
    try:
        shutil.move(fichier, dest)
    except Exception as e:
        print("Erreur déplacement fichier :", e)
    return categorie, label

# === GUI SIMPLE ===

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class FileSorterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("LoreHelper - Classement IA Gemini")
        self.geometry("500x340")
        self.resizable(False, False)

        self.label_title = ctk.CTkLabel(self, text="📂 Classement IA avec Gemini", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_title.pack(pady=(22, 10))

        self.file_path = ctk.StringVar()
        self.entry = ctk.CTkEntry(self, width=280, textvariable=self.file_path, placeholder_text="Sélectionne un fichier...", state="readonly")
        self.entry.pack(pady=6)

        self.btn_browse = ctk.CTkButton(self, text="Parcourir", width=100, command=self.browse_file)
        self.btn_browse.pack()

        self.btn_classer = ctk.CTkButton(self, text="Classer", width=180, height=38, state="disabled", command=self.classer)
        self.btn_classer.pack(pady=(22, 8))

        self.label_result = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=13), wraplength=470, justify="left")
        self.label_result.pack()

        self.btn_quit = ctk.CTkButton(self, text="Quitter", width=100, fg_color="#bb2222", hover_color="#aa1111", command=self.quit)
        self.btn_quit.pack(side="bottom", pady=10)

    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Choisir un fichier à classer",
            filetypes=[
                ("Text/Images", "*.txt *.md *.jpg *.jpeg *.png *.gif *.bmp *.webp"),
                ("Tous les fichiers", "*.*"),
            ]
        )
        if filename:
            self.file_path.set(filename)
            self.btn_classer.configure(state="normal")
            self.label_result.configure(text="")

    def classer(self):
        fichier = self.file_path.get()
        if not fichier or not os.path.isfile(fichier):
            self.label_result.configure(text="Sélectionne un fichier valide.", text_color="orange")
            return
        try:
            categorie, label = classer_fichier(fichier)
            text = f"✅ Classé dans : {categorie}\n\nRéponse Gemini : {label}"
            self.label_result.configure(text=text, text_color="lightgreen")
        except Exception as e:
            self.label_result.configure(text=f"Erreur : {e}", text_color="red")

if __name__ == "__main__":
    app = FileSorterApp()
    app.mainloop()
