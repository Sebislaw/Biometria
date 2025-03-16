import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
from application.pages.baseSubpage import BaseSubpage

# Strona
class PixelOperations(BaseSubpage):

    def __init__(self, master, main_app):
        # Definicja podstron
        subpages = {
            "greyscale": {
                "label": "Konwersja do odcieni szarości"
            },
            "brightness": {
                "label": "Korekta jasności"
            },
            "contrast": {
                "label": "Korekta kontrastu"
            },
            "negative": {
                "label": "Negatyw"
            },
            "binarization": {
                "label": "Binaryzacja"
            },
        }
        # Podstrona domyślna
        default_page = "greyscale"
        super().__init__(master, main_app, subpages, default_page)

    ####################################################################################################################

    def build_subpage(self, page_key):
        if page_key == "read_save":

            btn_wczytaj = tk.Button(self.content_area, text="Wczytaj")
            btn_wczytaj.place(relx=0.3, rely=0.4, relwidth=0.1, relheight=0.2)

            btn_wyczysc = tk.Button(self.content_area, text="Wyczyść")
            btn_wyczysc.place(relx=0.6, rely=0.4, relwidth=0.1, relheight=0.2)

        else:
            tk.Label(self.content_area, text="Podstrona pusta").pack()

    ####################################################################################################################
