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
            },
            "colour_channels": {
                "label": "Kanały kolorów"
            },
            "mixing": {
                "label": "Mieszanie obrazów"
            },
            "exponential": {
                "label": "Eksponenta"
            },
            "logarithm": {
                "label": "Logarytm"
            },
            "uniform": {
                "label": "Wyrównanie histogramu"
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

        elif page_key == "colour_channels":
            # Red channel slider
            slider_red = tk.Scale(
                self.content_area,
                from_=-255,
                to=255,
                orient="horizontal",
                variable=self.main_app.red_slider_value,
                label="Czerwony",
                command=lambda e: self.on_slider_change(self.adjust_color_channels_with_slider)
            )
            slider_red.place(relx=0.5, rely=0.3, relwidth=0.8, relheight=0.5, anchor="center")

            # Green channel slider
            slider_green = tk.Scale(
                self.content_area,
                from_=-255,
                to=255,
                orient="horizontal",
                variable=self.main_app.green_slider_value,
                label="Zielony",
                command=lambda e: self.on_slider_change(self.adjust_color_channels_with_slider)
            )
            slider_green.place(relx=0.5, rely=0.65, relwidth=0.8, relheight=0.5, anchor="center")

            # Blue channel slider
            slider_blue = tk.Scale(
                self.content_area,
                from_=-255,
                to=255,
                orient="horizontal",
                variable=self.main_app.blue_slider_value,
                label="Niebieski",
                command=lambda e: self.on_slider_change(self.adjust_color_channels_with_slider)
            )
            slider_blue.place(relx=0.5, rely=1, relwidth=0.8, relheight=0.5, anchor="center")

            self.adjust_color_channels_with_slider()

        else:
            tk.Label(self.content_area, text="Podstrona pusta").pack()

    def on_slider_change(self, update_func):
        if self.slider_update_id is not None:
            self.after_cancel(self.slider_update_id)
        self.slider_update_id = self.after(250, update_func)

    ####################################################################################################################

    def convert_greyscale_with_slider(self):
        if self.main_app.original_image_array is None:
            print("No image loaded!")
            return
        alpha = self.main_app.grey_slider_value.get() / 100.0
        orig_arr = self.main_app.original_image_array.astype(np.int16)
        grey = orig_arr.mean(axis=2).astype(np.uint8)
        grey_rgb = np.stack((grey,) * 3, axis=-1).astype(np.int16)
        blended = np.clip((1 - alpha) * orig_arr + alpha * grey_rgb, 0, 255).astype(np.uint8)
        self.update_right_panel(blended)

    ####################################################################################################################

    def adjust_brightness_with_slider(self):
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

    ####################################################################################################################

    def adjust_color_channels_with_slider(self):
        if self.main_app.original_image_array is None:
            print("No image loaded!")
            return

        # Get slider values for each color channel
        red_val = self.main_app.red_slider_value.get()
        green_val = self.main_app.green_slider_value.get()
        blue_val = self.main_app.blue_slider_value.get()

        # Create a copy of the original image
        modified_arr = self.main_app.original_image_array.astype(np.int16).copy()

        # Adjust each color channel separately
        modified_arr[:, :, 0] = np.clip(modified_arr[:, :, 0] + red_val, 0, 255).astype(np.int16)  # Red channel (adjusted)
        modified_arr[:, :, 1] = np.clip(modified_arr[:, :, 1] + green_val, 0, 255).astype(np.int16)  # Green channel (adjusted)
        modified_arr[:, :, 2] = np.clip(modified_arr[:, :, 2] + blue_val, 0, 255).astype(np.int16)  # Blue channel (adjusted)

        # Update the right panel with the modified image
        modified_arr = modified_arr.astype(np.uint8)
        self.update_right_panel(modified_arr)