import tkinter as tk

from PIL import Image, ImageTk
import numpy as np
from application.pages.pixelOperations import PixelOperations
from application.pages.graphicalFiltering import GraphicalFiltering
from application.pages.readSavePicture import ReadSavePicture

# Aplikacja
class MainApplication(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Przetwarzanie obrazów")
        self.geometry("600x500")

        # Atrybuty do przechowywania obrazu
        self.original_image = None
        self.original_image_array = None
        self.modified_image = None
        self.modified_image_array = None

        # Values to remember ---------------
        self.grey_slider_value = 0
        # ----------------------------------

        #---------------------------------------------------------------------------------------------------------------

        # Górna część aplikacji
        top_application_part = tk.Frame(self)
        top_application_part.place(relwidth=1.0, relheight=0.6)

        # Górny pasek aplikacji
        main_top_bar = tk.Frame(top_application_part, bd=2, relief=tk.RAISED)
        main_top_bar.place(relwidth=1)

        # Centralny obszar na panele
        central_area = tk.Frame(top_application_part, bd=2, relief=tk.FLAT)
        central_area.place(relx=0, rely=0.0, y=40, height=-40, relwidth=1.0, relheight=1)

        # Lewy panel
        self.left_panel = tk.Label(central_area, text="Oryginalny obraz", bd=1, relief=tk.GROOVE)
        self.left_panel.place(relx=0, rely=0, relwidth=0.5, relheight=1.0)

        # Prawy panel
        self.right_panel = tk.Label(central_area, text="Obraz po modyfikacji", bd=1, relief=tk.GROOVE)
        self.right_panel.place(relx=0.5, rely=0, relwidth=0.5, relheight=1.0)

        # ---------------------------------------------------------------------------------------------------------------

        # Dolna część na strony
        self.subpage_area = tk.Frame(self, bd=2, relief=tk.SUNKEN)
        self.subpage_area.place(relx=0, rely=0.6, relwidth=1.0, relheight=0.4)

        # ---------------------------------------------------------------------------------------------------------------

        # Inicjalizacja stron – przekazujemy referencję do głównej aplikacji (main_app=self)
        self.pages = {
            "Wczytaj / Zapisz": ReadSavePicture(self.subpage_area, main_app=self),
            "Operacje na pikselach": PixelOperations(self.subpage_area, main_app=self),
            "Filtry Graficzne": GraphicalFiltering(self.subpage_area, main_app=self)
        }

        # Przyciski do zmiany stron
        for page_name in self.pages:
            btn = tk.Button(main_top_bar, text=page_name,
                            command=lambda key=page_name: self.show_page(key))
            btn.pack(side=tk.LEFT, padx=5, pady=5)
        btn = tk.Button(main_top_bar, text="Zapisz zmiany", command=self.save_changes)
        btn.pack(side=tk.RIGHT, padx=5, pady=5)

        # Wyświetlenie domyślnej strony
        self.show_page("Wczytaj / Zapisz")

        # Nasłuchiwanie zmiany rozmiaru lewego panelu
        self.left_panel.bind("<Configure>", lambda e: self.schedule_image_update())

    ####################################################################################################################

    def show_page(self, page_key):
        # Ukrycie wszystkich stron i wyświetlenie wybranej
        for page in self.pages.values():
            page.pack_forget()
        self.pages[page_key].pack(fill=tk.BOTH, expand=True)

    ####################################################################################################################

    def update_left_panel_image(self):
        """Update the left panel with the original image (or saved changes)."""
        if self.original_image:
            panel_width = self.left_panel.winfo_width()
            panel_height = self.left_panel.winfo_height()
            if panel_width > 0 and panel_height > 0:
                # Make a copy to avoid altering the original
                image = self.original_image.copy()
                image.thumbnail((panel_width, panel_height), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.left_panel.config(image=photo)
                self.left_panel.image = photo  # Keep reference

    def update_right_panel_image(self):
        """Przeskalowuje oryginalny obraz do aktualnych wymiarów lewego panelu i wyświetla go."""
        if self.modified_image:
            panel_width = self.right_panel.winfo_width()
            panel_height = self.right_panel.winfo_height()
            if panel_width > 0 and panel_height > 0:
                # Tworzymy kopię oryginalnego obrazu, aby nie modyfikować go na stałe
                image = self.modified_image.copy()
                # Przeskalowanie z zachowaniem proporcji (Image.Resampling.LANCZOS zapewnia wysoką jakość)
                image.thumbnail((panel_width, panel_height), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.right_panel.config(image=photo)  # Usuwamy ewentualny tekst
                self.right_panel.image = photo  # Przechowujemy referencję, aby obraz nie został usunięty

    def save_changes(self):
        """
        When the user presses "Zapisz zmiany", update the left image so that it matches the right (modified) one.
        """
        if self.modified_image is not None:
            # Save the modified image as the new original image.
            self.original_image = self.modified_image.copy()
            self.original_image_array = self.modified_image_array.copy() if self.modified_image_array is not None else None
            self.update_left_panel_image()
            self.clear_values()

    def clear_values(self):
        self.grey_slider_value = 0

    ####################################################################################################################

    def schedule_image_update(self):
        """Schedules a single update for both panels after 500ms of inactivity."""
        if self.original_image is None:
            return
        # Cancel any previously scheduled update
        if hasattr(self, "resize_after_id"):
            self.after_cancel(self.resize_after_id)
        # Schedule a new update after 500ms
        self.resize_after_id = self.after(250, self.update_panels)

    def update_panels(self):
        """Update both left and right panels at once."""
        self.update_left_panel_image()
        self.update_right_panel_image()
    ####################################################################################################################
