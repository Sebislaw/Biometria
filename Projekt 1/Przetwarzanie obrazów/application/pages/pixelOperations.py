import tkinter as tk
import numpy as np
from application.pages.baseSubpage import BaseSubpage

# Page
class PixelOperations(BaseSubpage):

    def __init__(self, master, main_app):
        # Subpage definition
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
            }
        }
        # Default subpage
        default_subpage = "greyscale"
        self.slider_update_id = None
        super().__init__(master, main_app, subpages, default_subpage)

    ####################################################################################################################

    def build_subpage(self, page_key):

        if page_key == "greyscale":
            slider = tk.Scale(
                self.content_area,
                from_=0,
                to=100,
                orient="horizontal",
                variable=self.main_app.grey_slider_value,
                label="Procent konwersji do szarości",
                command=lambda e: self.on_slider_change(self.convert_greyscale_with_slider)
            )
            slider.place(relx=0.5, rely=0.4, relwidth=0.8, relheight=0.5, anchor="center")
            self.convert_greyscale_with_slider()

        elif page_key == "brightness":
            slider = tk.Scale(
                self.content_area,
                from_=-255,
                to=255,
                orient="horizontal",
                variable=self.main_app.brightness_value,
                label="Dodana jasność",
                command=lambda e: self.on_slider_change(self.adjust_brightness_with_slider)
            )
            slider.place(relx=0.5, rely=0.4, relwidth=0.8, relheight=0.5, anchor="center")
            self.adjust_brightness_with_slider()

        elif page_key == "contrast":
            slider = tk.Scale(
                self.content_area,
                from_=-100,
                to=200,
                orient="horizontal",
                variable=self.main_app.contrast_value,
                label="Korekta kontrastu",
                command=lambda e: self.on_slider_change(self.adjust_contrast_with_slider)
            )
            slider.place(relx=0.5, rely=0.4, relwidth=0.8, relheight=0.5, anchor="center")
            self.adjust_contrast_with_slider()

        elif page_key == "negative":
            btn = tk.Button(self.content_area, text="Negatyw", command=self.convert_negative)
            btn.place(relx=0.5, rely=0.5, relwidth=0.2, relheight=0.3, anchor="center")
            self.show_default_image()

        elif page_key == "binarization":
            slider = tk.Scale(
                self.content_area,
                from_= 0,
                to=255,
                orient="horizontal",
                variable=self.main_app.bin_thresh_value,
                label="Binaryzacja",
                command=lambda e: self.on_slider_change(self.binarize_with_slider)
            )
            slider.place(relx=0.5, rely=0.4, relwidth=0.8, relheight=0.5, anchor="center")
            self.binarize_with_slider()

        else:
            tk.Label(self.content_area, text="Podstrona pusta").pack()

    def on_slider_change(self, update_func):
        if self.slider_update_id is not None:
            self.after_cancel(self.slider_update_id)
        self.slider_update_id = self.after(250, update_func)

    ####################################################################################################################

    def convert_greyscale_with_slider(self):
        """
        Blends the original image with its greyscale version based on the slider value.
        """
        # Check that the original image array is loaded
        if self.main_app.original_image_array is None:
            print("No image loaded!")
            return
        alpha = self.main_app.grey_slider_value.get() / 100.0
        orig_arr = self.main_app.original_image_array.astype(np.float32)
        grey = orig_arr.mean(axis=2).astype(np.uint8)
        grey_rgb = np.stack((grey,) * 3, axis=-1).astype(np.float32)
        blended = np.clip((1 - alpha) * orig_arr + alpha * grey_rgb, 0, 255).astype(np.uint8)
        self.update_right_panel(blended)

    ####################################################################################################################

    def adjust_brightness_with_slider(self):
        """Adjusts the brightness of the image based on the slider value and updates the right panel."""
        if self.main_app.original_image_array is None:
            print("No image loaded!")
            return
        slider_val = self.main_app.brightness_value.get()
        brightness_offset = slider_val
        orig_arr = self.main_app.original_image_array.astype(np.int16)
        bright_arr = orig_arr + brightness_offset
        bright_arr = np.clip(bright_arr, 0, 255).astype(np.uint8)
        self.update_right_panel(bright_arr)

    ####################################################################################################################

    def adjust_contrast_with_slider(self):
        if self.main_app.original_image_array is None:
            print("No image loaded!")
            return
        contrast = self.main_app.contrast_value.get()
        factor = (contrast + 100) / 100.0
        orig_arr = self.main_app.original_image_array.astype(np.float32)
        mean_val = orig_arr.mean(axis=(0, 1), keepdims=True)
        adjusted = mean_val + factor * (orig_arr - mean_val)
        adjusted = np.clip(adjusted, 0, 255).astype(np.uint8)
        self.update_right_panel(adjusted)

    ####################################################################################################################

    def convert_negative(self):
        if self.main_app.original_image_array is None:
            print("No image loaded!")
            return
        orig_arr = self.main_app.original_image_array.astype(np.uint8)
        negative = 255 - orig_arr
        self.update_right_panel(negative)

    ####################################################################################################################

    def binarize_with_slider(self):
        # Binarization slider: value from 0 to 255 used as threshold
        if self.main_app.original_image_array is None:
            print("No image loaded!")
            return
        threshold = self.main_app.bin_thresh_value.get()
        orig_arr = self.main_app.original_image_array.astype(np.float32)
        # Convert to grayscale first
        grey = orig_arr.mean(axis=2)
        binary = np.where(grey < threshold, 0, 255).astype(np.uint8)
        binary_rgb = np.stack((binary,) * 3, axis=-1)
        self.update_right_panel(binary_rgb)