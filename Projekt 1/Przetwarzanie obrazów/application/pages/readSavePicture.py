import tkinter as tk
from PIL import Image
import numpy as np
from application.pages.baseSubpage import BaseSubpage

# Strona
class ReadSavePicture(BaseSubpage):

    def __init__(self, master, main_app):
        # Definicja podstron
        subpages = {
            "read_save": {"label": "Wczytaj/usuń obraz"},
            "save_changes": {"label": "Zapisz obraz"}
        }
        # Podstrona domyślna
        default_page = "read_save"
        super().__init__(master, main_app, subpages, default_page)

    ####################################################################################################################

    def build_subpage(self, page_key):
        if page_key == "read_save":

            btn_wczytaj = tk.Button(self.content_area, text="Wczytaj", command=self.load_image)
            btn_wczytaj.place(relx=0.3, rely=0.4, relwidth=0.1, relheight=0.2)

            btn_wyczysc = tk.Button(self.content_area, text="Wyczyść", command=self.clear_image)
            btn_wyczysc.place(relx=0.6, rely=0.4, relwidth=0.1, relheight=0.2)

        elif page_key == "save_changes":

            btn_a = tk.Button(self.content_area, text="A", command=self.load_image)
            btn_a.place(relx=0.3, rely=0.4, relwidth=0.1, relheight=0.2)

            btn_b = tk.Button(self.content_area, text="B", command=self.clear_image)
            btn_b.place(relx=0.6, rely=0.4, relwidth=0.1, relheight=0.2)

        else:
            tk.Label(self.content_area, text="Podstrona pusta").pack()

    ####################################################################################################################

    def load_image(self):

        IMAGE_PATH = "pictures/20241228_191601.jpg"

        try:
            image = Image.open(IMAGE_PATH)
            # Zapisywanie obrazu jako numpy array w głównej aplikacji
            self.main_app.image_array = np.array(image)
            # Zapamiętujemy obraz oryginalny (jako obiekt Pillow) do dalszych skalowań
            self.main_app.original_image = image
            # Aktualizujemy lewy panel, aby wyświetlić przeskalowany obraz
            self.main_app.update_left_panel_image()

        except Exception as e:
            print("Błąd przy wczytywaniu obrazu:", e)

    ####################################################################################################################

    def clear_image(self):
        # Czyścimy lewy panel oraz usuwamy zapisane obrazy
        self.main_app.left_panel.config(image='')
        self.main_app.left_panel.image = None
        self.main_app.original_image = None
        self.main_app.image_array = None

    ####################################################################################################################