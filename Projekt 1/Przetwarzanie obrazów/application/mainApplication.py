import tkinter as tk
from PIL import Image, ImageTk

from application.pages.readSavePicture import ReadSavePicture
from application.pages.pixelOperations import PixelOperations
from application.pages.graphicalFiltering import GraphicalFiltering
from application.pages.morphologicalOperations import MorphologicalOperations
from application.pages.statistics import Statistics

# Application
class MainApplication(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Przetwarzanie obrazów")
        # self.geometry("600x500")
        self.geometry("1280x720")

        # Attributes to store images
        self.original_image = None
        self.original_image_array = None
        self.modified_image = None
        self.modified_image_array = None

        # Values to remember ---------------
        self.grey_slider_value = tk.IntVar(value=0)
        self.brightness_value = tk.IntVar(value=0)
        self.contrast_value = tk.IntVar(value=0)
        self.bin_thresh_value = tk.IntVar(value=128)
        self.red_slider_value = tk.IntVar(value=0)
        self.green_slider_value = tk.IntVar(value=0)
        self.blue_slider_value = tk.IntVar(value=0)

        self.mean_size = tk.IntVar(value=3)
        self.mean_center = tk.IntVar(value=1)
        self.gaussian_size = tk.IntVar(value=3)
        self.gaussian_sigma = tk.DoubleVar(value=1.0)
        self.sharpening_center = tk.IntVar(value=5)
        self.custom_size = tk.IntVar(value=3)
        self.custom_kernel_size = tk.IntVar(value=3)
        self.custom_kernel = None

        self.custom_struct_elem = None

        self.bin_thresh_value_statistics = tk.IntVar(value=128)
        # ----------------------------------

        #---------------------------------------------------------------------------------------------------------------

        # Top part of the application
        top_application_part = tk.Frame(self)
        top_application_part.place(relwidth=1.0, relheight=0.6)

        # Top toolbar
        main_top_bar = tk.Frame(top_application_part, bd=2, relief=tk.RAISED)
        main_top_bar.place(relwidth=1)

        # Central area for images
        central_area = tk.Frame(top_application_part, bd=2, relief=tk.FLAT)
        central_area.place(relx=0, rely=0.0, y=40, height=-40, relwidth=1.0, relheight=1)

        # Left panel
        self.left_panel = tk.Label(central_area, text="Oryginalny obraz", bd=1, relief=tk.GROOVE)
        self.left_panel.place(relx=0, rely=0, relwidth=0.5, relheight=1.0)

        # Right panel
        self.right_panel = tk.Label(central_area, text="Obraz po modyfikacji", bd=1,  relief=tk.GROOVE)
        self.right_panel.place(relx=0.5, rely=0, relwidth=0.5, relheight=1.0)

        # ---------------------------------------------------------------------------------------------------------------

        # Bottom part for subpages
        self.subpage_area = tk.Frame(self, bd=2, relief=tk.SUNKEN)
        self.subpage_area.place(relx=0, rely=0.6, relwidth=1.0, relheight=0.4)

        # ---------------------------------------------------------------------------------------------------------------

        # Initialization of subpages with reference to the main application
        self.pages = {
            "Wczytaj / Zapisz": ReadSavePicture(self.subpage_area, main_app=self),
            "Operacje na pikselach": PixelOperations(self.subpage_area, main_app=self),
            "Filtry Graficzne": GraphicalFiltering(self.subpage_area, main_app=self),
            "Operacje morfologiczne": MorphologicalOperations(self.subpage_area, main_app=self),
            "Statystyki": Statistics(self.subpage_area, main_app=self)
        }

        # Buttons to change the pages
        for page_name in self.pages:
            btn = tk.Button(main_top_bar, text=page_name,
                            command=lambda key=page_name: self.show_page(key))
            btn.pack(side=tk.LEFT, padx=5, pady=5)
        btn = tk.Button(main_top_bar, text="Zapisz zmiany", command=self.save_changes)
        btn.pack(side=tk.RIGHT, padx=5, pady=5)

        # Default page
        self.show_page("Wczytaj / Zapisz")
        self.last_page = "Wczytaj / Zapisz"

        # Listening to the left panel change
        self.left_panel.bind("<Configure>", lambda e: self.schedule_image_update())

    ####################################################################################################################

    def show_page(self, page_key):
        for page in self.pages.values():
            page.pack_forget()
        page_obj = self.pages[page_key]
        page_obj.pack(fill=tk.BOTH, expand=True)
        self.last_page = page_key
        # If the page has a build_subpage method and a recorded last subpage, call it.
        if hasattr(page_obj, 'build_subpage'):
            last_subpage = getattr(page_obj, 'last_subpage_key', None)
            if last_subpage is not None:
                page_obj.build_subpage(last_subpage)

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

    def update_left_panel_image(self):
        """Update the left panel with the original image (or saved changes)."""
        if self.original_image:
            panel_width = self.left_panel.winfo_width()
            panel_height = self.left_panel.winfo_height()
            if panel_width > 0 and panel_height > 0:
                image = self.original_image.copy()
                iw, ih = image.size
                scale = min(panel_width / iw, panel_height / ih)
                new_size = (int(iw * scale), int(ih * scale))
                image = image.resize(new_size, Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.left_panel.config(image=photo)
                self.left_panel.image = photo

    def update_right_panel_image(self):
        if self.modified_image:
            panel_width = self.right_panel.winfo_width()
            panel_height = self.right_panel.winfo_height()
            if panel_width > 0 and panel_height > 0:
                image = self.modified_image.copy()
                iw, ih = image.size
                scale = min(panel_width / iw, panel_height / ih)
                new_size = (int(iw * scale), int(ih * scale))
                image = image.resize(new_size, Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.right_panel.config(image=photo)
                self.right_panel.image = photo

    ####################################################################################################################

    def save_changes(self):
        if self.modified_image is not None:
            # Save the modified image as the new original image.
            self.original_image = self.modified_image.copy()
            self.original_image_array = self.modified_image_array.copy() if self.modified_image_array is not None else None
            self.update_left_panel_image()
            self.clear_values()

    def clear_values(self):
        self.grey_slider_value = tk.IntVar(value=0)
        self.brightness_value = tk.IntVar(value=0)
        self.contrast_value = tk.IntVar(value=0)
        self.bin_thresh_value = tk.IntVar(value=128)
        self.red_slider_value = tk.IntVar(value=0)
        self.green_slider_value = tk.IntVar(value=0)
        self.blue_slider_value = tk.IntVar(value=0)

        self.mean_size = tk.IntVar(value=3)
        self.mean_center = tk.IntVar(value=1)
        self.gaussian_size = tk.IntVar(value=3)
        self.gaussian_sigma = tk.DoubleVar(value=1.0)
        self.sharpening_center = tk.IntVar(value=5)
        self.custom_size = tk.IntVar(value=3)
        self.custom_kernel_size = tk.IntVar(value=3)
        self.custom_kernel = None

        self.custom_struct_elem = None

        self.bin_thresh_value_statistics = tk.IntVar(value=128)

        # Refresh the page
        self.pages[self.last_page].show_subpage(self.pages[self.last_page].last_subpage_key)
    ####################################################################################################################
