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
            self.show_default_image()
            btn_read = tk.Button(self.content_area, text="Wczytaj", command=self.load_image)
            btn_read.place(relx=0.3, rely=0.5, relwidth=0.2, relheight=0.3, anchor="center")
            btn_write = tk.Button(self.content_area, text="Wyczyść", command=self.clear_image)
            btn_write.place(relx=0.7, rely=0.5, relwidth=0.2, relheight=0.3, anchor="center")
        elif page_key == "save_changes":
            self.show_default_image()
            btn_write = tk.Button(self.content_area, text="Zapisz zmiany", command=self.write_image)
            btn_write.place(relx=0.5, rely=0.5, relwidth=0.2, relheight=0.3, anchor="center")
        else:
            tk.Label(self.content_area, text="Podstrona pusta").pack()

    ####################################################################################################################

    def load_image(self):

        IMAGE_PATH = "pictures/20241228_191601.jpg"

        try:
            image = Image.open(IMAGE_PATH)
            # Store the image and its NumPy array in the main application as original
            self.main_app.original_image = image
            self.main_app.original_image_array = np.array(image)

            # Initially, set the modified image as a copy of the original
            self.main_app.modified_image = image.copy()
            self.main_app.modified_image_array = np.array(image)

            # Update both panels
            self.main_app.update_left_panel_image()
            self.main_app.update_right_panel_image()

            self.main_app.clear_values()

        except Exception as e:
            print("Błąd przy wczytywaniu obrazu:", e)

    ####################################################################################################################

    def clear_image(self):

        self.main_app.left_panel.config(image='')
        self.main_app.left_panel.image = None
        self.main_app.original_image = None
        self.main_app.original_image_array = None

        self.main_app.right_panel.config(image='')
        self.main_app.right_panel.image = None
        self.main_app.modified_image = None
        self.main_app.modified_image_array = None

        self.main_app.clear_values()

    ####################################################################################################################

    def write_image(self):
        if self.main_app.original_image is not None:
            self.main_app.original_image.save("pictures/test.jpg")