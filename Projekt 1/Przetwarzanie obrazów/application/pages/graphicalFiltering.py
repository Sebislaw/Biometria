import tkinter as tk
from application.pages.baseSubpage import BaseSubpage

# Strona
class GraphicalFiltering(BaseSubpage):

    def __init__(self, master, main_app):
        # Definicja podstron
        subpages = {
            "1": {
                "label": "1"
            }
        }
        # Podstrona domyślna
        default_page = "1"
        super().__init__(master, main_app, subpages, default_page)

    ####################################################################################################################

    def build_subpage(self, page_key):
        if page_key == "1":

            btn_wczytaj = tk.Button(self.content_area, text="1a")
            btn_wczytaj.place(relx=0.3, rely=0.4, relwidth=0.1, relheight=0.2)

            btn_wyczysc = tk.Button(self.content_area, text="1b")
            btn_wyczysc.place(relx=0.6, rely=0.4, relwidth=0.1, relheight=0.2)

        else:
            tk.Label(self.content_area, text="Podstrona pusta").pack()

    ####################################################################################################################