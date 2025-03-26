import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image
import numpy as np
from application.pages.baseSubpage import BaseSubpage

# Strona
class ReadSavePicture(BaseSubpage):

    def __init__(self, master, main_app):
        # Subpage definition
        subpages = {
            "read_save": {"label": "Wczytaj/wyczyść obraz"},
            "save_changes": {"label": "Zapisz obraz"}
        }
        # Degault subpage
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
            btn_write = tk.Button(self.content_area, text="Zapisz obraz", command=self.write_image)
            btn_write.place(relx=0.5, rely=0.5, relwidth=0.2, relheight=0.3, anchor="center")
        else:
            tk.Label(self.content_area, text="Podstrona pusta").pack()

    ####################################################################################################################

    def load_image(self):
        # Open a file dialog to select an image file
        # IMAGE_PATH = "pictures/300x300px.jpg"
        IMAGE_PATH = filedialog.askopenfilename(
            title="Wybierz obraz",
            initialdir=os.getcwd(),
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")]
        )
        if not IMAGE_PATH:
            return  # User cancelled

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
            file_path = filedialog.asksaveasfilename(
                title="Zapisz obraz jako",
                initialdir=os.getcwd(),
                defaultextension=".jpg",
                filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")]
            )
            if file_path:
                self.main_app.original_image.save(file_path)