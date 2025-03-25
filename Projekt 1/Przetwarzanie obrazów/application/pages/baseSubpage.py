import tkinter as tk
from PIL import Image
from abc import ABC, abstractmethod

class BaseSubpage(tk.Frame, ABC):

    def __init__(self, master, main_app, subpages, default_subpage_key):
        super().__init__(master)
        self.main_app = main_app
        self.subpages = subpages
        self.default_subpage_key = default_subpage_key
        self.last_subpage_key = default_subpage_key

        # Top bar
        self.top_bar = tk.Frame(self, bd=2, relief=tk.RAISED)
        self.top_bar.pack(side=tk.TOP, fill=tk.X)

        # Buttons for subpages
        for key, page in self.subpages.items():
            btn = tk.Button(self.top_bar, text=page["label"], command=lambda k=key: self.show_subpage(k))
            btn.pack(side=tk.LEFT, padx=2, pady=2)

        # Content area
        self.content_area = tk.Frame(self, relief=tk.FLAT)
        self.content_area.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Show default subpage
        self.show_subpage(self.default_subpage_key)

    def show_subpage(self, subpage_key):
        for widget in self.content_area.winfo_children():
            widget.destroy()
        self.last_subpage_key = subpage_key
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
        pass