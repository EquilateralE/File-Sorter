import customtkinter as ctk
from tkinter import filedialog
import os

from .sorter import classer_fichier  # ou from .sorter import ... selon ton arborescence

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class FileSorterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("LoreHelper - Classement IA Gemini")
        self.geometry("500x340")
        self.resizable(False, False)

        # Titre
        self.label_title = ctk.CTkLabel(self, text="📂 Classement IA avec Gemini", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_title.pack(pady=(22, 10))

        # Sélection de fichier
        self.file_path = ctk.StringVar()
        self.entry = ctk.CTkEntry(self, width=280, textvariable=self.file_path, placeholder_text="Sélectionne un fichier...", state="readonly")
        self.entry.pack(pady=6)

        self.btn_browse = ctk.CTkButton(self, text="Parcourir", width=100, command=self.browse_file)
        self.btn_browse.pack()

        # Bouton Classer
        self.btn_classer = ctk.CTkButton(self, text="Classer", width=180, height=38, state="disabled", command=self.classer)
        self.btn_classer.pack(pady=(22, 8))

        # Résultat Catégorie
        self.label_result = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=13), wraplength=470, justify="left")
        self.label_result.pack()

        # Quitter
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

def main():
    app = FileSorterApp()
    app.mainloop()

if __name__ == "__main__":
    main()
