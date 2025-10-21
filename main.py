import customtkinter as ctk
import subprocess
import sys
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class LoreHelperMain(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("LoreHelper - Menu principal")
        self.geometry("800x500")
        self.resizable(False, False)

        # Titre
        self.title_label = ctk.CTkLabel(self, text="🧭 LoreHelper", font=ctk.CTkFont(size=28, weight="bold"))
        self.title_label.pack(pady=(30, 0))

        # Sous-titre
        self.subtitle_label = ctk.CTkLabel(self, text="Assistant d’organisation de lore et d’écriture", font=ctk.CTkFont(size=14))
        self.subtitle_label.pack(pady=(8, 18))

        # Boutons d’action
        self.classer_btn = ctk.CTkButton(self, text="Classer un fichier", width=220, height=38, font=ctk.CTkFont(size=16), command=self.launch_FileSorter)
        self.classer_btn.pack(pady=10)

        self.quit_btn = ctk.CTkButton(self, text="Quitter", width=220, height=32, font=ctk.CTkFont(size=15), fg_color="#bb2222", hover_color="#aa1111", command=self.quit)
        self.quit_btn.pack(pady=(28, 0))

        # Signature
        self.footer = ctk.CTkLabel(self, text="Développé par SANS Lucas ", font=ctk.CTkFont(size=11, slant="italic"), text_color="#888")
        self.footer.pack(side="bottom", pady=6)

    def launch_FileSorter(self):
        # Lance le GUI du module FileSorter
        path = os.path.join("FileSorter", "gui.py")
        if getattr(sys, 'frozen', False):
            subprocess.Popen(["python", path])
        else:
            import FileSorter.gui
            FileSorter.gui.main()


if __name__ == "__main__":
    app = LoreHelperMain()
    app.mainloop()
