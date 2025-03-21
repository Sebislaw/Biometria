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
        self.slider_update_id = None

        super().__init__(master, main_app, subpages, default_page)

    ####################################################################################################################

    def build_subpage(self, page_key):

        if page_key == "greyscale":

            # btn_greyscale = tk.Button(self.content_area, text="Konwertuj do odcieni szarości", command=self.convert_greyscale)
            # btn_greyscale.place(relx=0.5, rely=0.5, relwidth=0.2, relheight=0.3, anchor="center")

            # Create a slider to adjust greyscale level
            # 0 = original image, 100 = full greyscale
            self.grey_slider_var = tk.IntVar(value=self.main_app.grey_slider_value)
            slider = tk.Scale(
                self.content_area,
                from_=0,
                to=100,
                orient="horizontal",
                variable=self.grey_slider_var,
                label="Greyscale level",
                command=self.on_slider_change  # Called on slider movement
            )
            slider.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.5, anchor="center")

            # You may also add a label or button if needed
            # Optionally, you can call convert_greyscale_with_slider() right away:
            self.convert_greyscale_with_slider()
        else:
            tk.Label(self.content_area, text="Podstrona pusta").pack()

    ####################################################################################################################

    def on_slider_change(self, event=None):
        """
        Called every time the slider is moved. Cancels any pending update
        and schedules a new update after 500ms of inactivity.
        """
        # Save the current slider value
        self.main_app.grey_slider_value = self.grey_slider_var.get()
        if self.slider_update_id is not None:
            self.after_cancel(self.slider_update_id)
        self.slider_update_id = self.after(250, self.convert_greyscale_with_slider)

    def convert_greyscale_with_slider(self):
        """
        Blends the original image with its greyscale version based on the slider value.
        """
        # Check that the original image array is loaded
        if self.main_app.original_image_array is None:
            print("No image loaded!")
            return

        # Get the slider value: 0 means 0% greyscale (original), 100 means 100% greyscale.
        slider_val = self.grey_slider_var.get()
        alpha = slider_val / 100.0  # blending factor

        # Get the original image array (assumed shape: (H, W, 3))
        orig_arr = self.main_app.original_image_array.astype(np.float32)

        # Create a full greyscale version: average across the RGB channels.
        grey = orig_arr.mean(axis=2).astype(np.uint8)
        grey_rgb = np.stack((grey,) * 3, axis=-1).astype(np.float32)

        # Blend: (1 - alpha)*original + alpha*greyscale, clip values to [0,255]
        blended = np.clip((1 - alpha) * orig_arr + alpha * grey_rgb, 0, 255).astype(np.uint8)

        # Create a Pillow image from the blended array
        blended_img = Image.fromarray(blended)

        # Save the modified image and its array in the main application
        self.main_app.modified_image = blended_img
        self.main_app.modified_image_array = blended

        # Update the right panel with the modified image
        self.main_app.update_right_panel_image()
     ##################
    def convert_greyscale(self):
        # Check that the original image array is loaded
        if self.main_app.original_image_array is None:
            print("No image loaded!")
            return

        # Convert to greyscale by averaging the RGB channels
        img_arr = self.main_app.original_image_array
        grey = img_arr.mean(axis=2).astype(np.uint8)
        # Re-stack to 3 channels for display
        grey_rgb = np.stack((grey,) * 3, axis=-1)

        # Create a Pillow image from the greyscale array
        grey_img = Image.fromarray(grey_rgb)

        # Save the modified image (greyscale) in the main app
        self.main_app.modified_image = grey_img
        self.main_app.modified_image_array = grey_rgb

        # Update the right panel with the modified image
        self.main_app.update_right_panel_image()
