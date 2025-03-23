import tkinter as tk
from PIL import Image
from abc import ABC, abstractmethod

class BaseSubpage(tk.Frame, ABC):

    def __init__(self, master, main_app, subpages, default_subpage_key):
        """
        :param master: Rodzic (np. obszar, w którym osadzona jest strona)
        :param main_app: Referencja do głównej aplikacji (do wspólnych funkcji)
        :param subpages: Słownik konfiguracji podstron (np. {"read_save": {"label": "Wczytaj/usuń obraz"}, ...})
        :param default_subpage_key: Klucz podstrony domyślnej
        """
        super().__init__(master)
        self.main_app = main_app
        self.subpages = subpages
        self.default_subpage_key = default_subpage_key
        self.last_subpage_key = default_subpage_key

        # Górny pasek strony (wspólny układ)
        self.top_bar = tk.Frame(self, bd=2, relief=tk.RAISED)
        self.top_bar.pack(side=tk.TOP, fill=tk.X)

        # Tworzymy przyciski przełączające podstrony
        for key, page in self.subpages.items():
            btn = tk.Button(self.top_bar, text=page["label"], command=lambda k=key: self.show_subpage(k))
            btn.pack(side=tk.LEFT, padx=2, pady=2)

        # Obszar podstrony (wspólny)
        self.content_area = tk.Frame(self, relief=tk.FLAT)
        self.content_area.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Wyświetlamy domyślną podstronę
        self.show_subpage(self.default_subpage_key)

    def show_subpage(self, subpage_key):
        # Czyścimy obszar podstrony
        for widget in self.content_area.winfo_children():
            widget.destroy()
        self.last_subpage_key = subpage_key
        # Wywołujemy metodę specyficzną dla danej klasy
        self.build_subpage(subpage_key)

    def show_default_image(self):
        if self.main_app.original_image is None:
            return
        array = self.main_app.original_image_array.copy()
        image = Image.fromarray(array)
        self.main_app.modified_image = image
        self.main_app.modified_image_array = array
        self.main_app.update_right_panel_image()

    def update_right_panel(self, array):
        if self.main_app.modified_image is None:
            return
        image = Image.fromarray(array)
        self.main_app.modified_image = image
        self.main_app.modified_image_array = array
        self.main_app.update_right_panel_image()

    @abstractmethod
    def build_subpage(self, subpage_key):
        """
        Metoda abstrakcyjna, która powinna być implementowana w klasach dziedziczących.
        Powinna utworzyć zawartość obszaru self.content_area w zależności od subpage_key.
        """
        pass