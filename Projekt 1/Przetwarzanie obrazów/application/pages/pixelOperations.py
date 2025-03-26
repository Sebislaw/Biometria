import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
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
            "equalization": {
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

        elif page_key == "mixing":
            # Left half: Preview of the added (second) image
            left_frame = tk.Frame(self.content_area)
            left_frame.place(relx=0.25, rely=0.5, relwidth=0.45, relheight=1, anchor="center")
            # A label to show the second image (or a placeholder text)
            self.mixing_preview_label = tk.Label(left_frame, text="Brak obrazu do mieszania")
            self.mixing_preview_label.pack(expand=True, fill="both")

            # Right half: Controls (slider and load button)
            right_frame = tk.Frame(self.content_area)
            right_frame.place(relx=0.75, rely=0.5, relwidth=0.45, relheight=1, anchor="center")
            controls_frame = tk.Frame(right_frame)
            controls_frame.pack(expand=True, fill="x", padx=10, pady=10)

            # Slider for alpha mixing (0.0 to 1.0, default 0.5)
            # self.mix_alpha = tk.DoubleVar(value=0.5)
            slider = tk.Scale(
                controls_frame,
                variable=self.main_app.mixing_alpha,
                from_=0.0,
                to=1.0,
                resolution=0.01,
                orient="horizontal",
                label="Waga (0=drugi, 1=pierwszy)",
                command=lambda e: self.update_mix()
            )
            slider.pack(fill="x", pady=5)

            # Button to load the second image
            tk.Button(controls_frame, text="Wczytaj drugi obraz",
                      command=self.load_second_image).pack(pady=5)


            if self.main_app.added_image:
                self.update_mix()
            else:
                self.show_default_image()
            # Update the mix result on slider change
            self.mixing_preview_label.bind("<Configure>", self.update_second_image_preview)

        elif page_key == "exponential":
            # Controls container
            controls_frame = tk.Frame(self.content_area)
            controls_frame.place(relx=0.5, rely=0.3, relwidth=0.8, relheight=0.2, anchor="center")
            # Dropdown for channel
            exp_channel_var = self.main_app.exp_channel_var
            channels = ["wszystkie", "czerwony", "zielony", "niebieski"]
            channel_menu = tk.OptionMenu(controls_frame, exp_channel_var, *channels)
            channel_menu.place(relx=0.05, rely=0.2, relwidth=0.4, relheight=0.5)
            # Entry for exponent
            exp_val = self.main_app.exp_val
            exp_entry = tk.Entry(controls_frame, textvariable=exp_val)
            exp_entry.place(relx=0.55, rely=0.2, relwidth=0.4, relheight=0.5)
            # Button to apply transformation
            tk.Button(self.content_area, text="Zastosuj transformację wykładniczą",
                      command=lambda: self.apply_exponential_transform(exp_val.get(), exp_channel_var.get()) if exp_val.get() > 0 else None
                      ).place(relx=0.5, rely=0.6, relwidth=0.4, relheight=0.1, anchor="center")
            self.apply_exponential_transform(exp_val.get(), exp_channel_var.get())

        elif page_key == "logarithm":
            controls_frame = tk.Frame(self.content_area)
            controls_frame.place(relx=0.5, rely=0.3, relwidth=0.8, relheight=0.2, anchor="center")
            # Dropdown for channel
            log_channel_var = self.main_app.log_channel_var
            channels = ["wszystkie", "czerwony", "zielony", "niebieski"]
            channel_menu = tk.OptionMenu(controls_frame, log_channel_var, *channels)
            channel_menu.place(relx=0.05, rely=0.2, relwidth=0.4, relheight=0.5)
            # Entry for exponent
            log_val = self.main_app.log_var
            log_entry = tk.Entry(controls_frame, textvariable=log_val)
            log_entry.place(relx=0.55, rely=0.2, relwidth=0.4, relheight=0.5)
            # Button to apply transformation
            tk.Button(self.content_area, text="Zastosuj transformację logarytmiczną",
                      command=lambda: self.apply_logarithmic_transform(log_val.get(), log_channel_var.get()) if log_val.get() > 0 else None
                      ).place(relx=0.5, rely=0.6, relwidth=0.4, relheight=0.1, anchor="center")
            self.apply_logarithmic_transform(log_val.get(), log_channel_var.get())

        elif page_key == "equalization":
            # Controls container
            controls_frame = tk.Frame(self.content_area)
            controls_frame.place(relx=0.5, rely=0.3, relwidth=0.8, relheight=0.2, anchor="center")

            # Dropdown for channel
            eq_channel_var = self.main_app.eq_channel_var
            channels = ["wszystkie", "czerwony", "zielony", "niebieski"]
            channel_menu = tk.OptionMenu(controls_frame, eq_channel_var, *channels)
            channel_menu.place(relx=0.5, rely=0.2, relwidth=0.4, relheight=0.5, anchor="center")

            # Button to apply histogram equalization
            tk.Button(self.content_area, text="Wyrównaj histogram",
                      command=lambda: self.apply_histogram_equalization(eq_channel_var.get())
                      ).place(relx=0.5, rely=0.6, relwidth=0.4, relheight=0.1, anchor="center")
            self.apply_histogram_equalization(eq_channel_var.get())

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

    ####################################################################################################################

    def load_second_image(self):
        from tkinter import filedialog
        import os

        # Open file dialog to select the second image
        image_path = filedialog.askopenfilename(
            title="Wybierz drugi obraz",
            initialdir=os.getcwd(),
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")]
        )
        if not image_path:
            return  # User cancelled

        try:
            image = Image.open(image_path)

            # Force update to get correct dimensions
            self.mixing_preview_label.update_idletasks()

            # Get target container's dimensions
            w = self.mixing_preview_label.winfo_width()
            h = self.mixing_preview_label.winfo_height()

            if w == 0 or h == 0:
                w, h = self.main_app.original_image.size  # Fallback to original image size

            margin_factor = 0.95
            target_w = int(w * margin_factor)
            target_h = int(h * margin_factor)

            # Get original image dimensions
            img_w, img_h = image.size

            # Calculate scale factor to maintain aspect ratio
            scale_factor = min(target_w / img_w, target_h / img_h)
            new_w = int(img_w * scale_factor)
            new_h = int(img_h * scale_factor)

            # Resize while maintaining aspect ratio
            image = image.resize((new_w, new_h), Image.Resampling.LANCZOS)

            # Store the resized image
            self.main_app.added_image = image

            # Update the left preview label
            preview = ImageTk.PhotoImage(image)
            self.mixing_preview_label.config(image=preview, text="")
            self.mixing_preview_label.image = preview

            # Update the mix result
            self.update_mix()
        except Exception as e:
            print("Error loading second image:", e)

    def update_second_image_preview(self, event=None):
        if self.main_app.added_image is None:
            return
        # Ensure the mixing_preview_label is rendered so its dimensions are available
        image = self.main_app.added_image
        self.mixing_preview_label.update_idletasks()
        w = self.mixing_preview_label.winfo_width()
        h = self.mixing_preview_label.winfo_height()
        # Get original image dimensions
        img_w, img_h = image.size
        # Calculate a scale factor that is 1 if image fits, or less than 1 if image is too large
        scale_factor = min(1, w / img_w, h / img_h)
        new_size = (int(img_w * scale_factor), int(img_h * scale_factor))
        resized_image = image.resize(new_size, Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)
        self.mixing_preview_label.config(image=photo, text="")
        self.mixing_preview_label.image = photo

    def update_mix(self):
        # Ensure both images exist; if not, show the original in the right panel
        if self.main_app.original_image_array is None:
            return
        if not hasattr(self.main_app, "added_image"):
            self.update_right_panel(self.main_app.original_image_array)
            return
        if self.main_app.added_image is None:
            return

        # Get the original image array (as float32)
        orig_arr = self.main_app.original_image_array.astype(np.float32)
        # Get the added image as a NumPy array, resizing if necessary
        added_img = self.main_app.added_image
        # Resize the added image to match the original if dimensions differ
        if added_img.size != self.main_app.original_image.size:
            added_img = added_img.resize(self.main_app.original_image.size, Image.Resampling.LANCZOS)
        added_arr = np.array(added_img).astype(np.float32)

        # Retrieve alpha value: alpha for the original image, (1 - alpha) for the added image.
        alpha = self.main_app.mixing_alpha.get()
        mixed = np.clip(alpha * orig_arr + (1 - alpha) * added_arr, 0, 255).astype(np.uint8)
        self.update_right_panel(mixed)
        if self.main_app.added_image:
            self.update_second_image_preview()

    ####################################################################################################################

    def apply_exponential_transform(self, exponent, channel):
        if self.main_app.original_image_array is None:
            return
        import numpy as np
        orig = self.main_app.original_image_array.astype(np.float32)
        norm = orig / 255.0
        transformed = np.power(norm, exponent) * 255.0
        if channel != "wszystkie":
            ch_idx = {"czerwony": 0, "zielony": 1, "niebieski": 2}[channel]
            new_img = orig.copy()
            new_img[:, :, ch_idx] = transformed[:, :, ch_idx]
            result = new_img
        else:
            result = transformed
        result = np.clip(result, 0, 255).astype(np.uint8)
        self.update_right_panel(result)

    ####################################################################################################################

    def apply_logarithmic_transform(self, exponent, channel):
        if self.main_app.original_image_array is None:
            return
        import numpy as np
        orig = self.main_app.original_image_array.astype(np.float32)
        norm = orig / 255.0
        # Standard logarithmic transform: log(1 + x)/log(1+max) where max=255, then apply exponent
        transformed = np.power(np.log1p(norm * 255.0) / np.log(256), exponent) * 255.0
        if channel != "wszystkie":
            ch_idx = {"czerwony": 0, "zielony": 1, "niebieski": 2}[channel]
            new_img = orig.copy()
            new_img[:, :, ch_idx] = transformed[:, :, ch_idx]
            result = new_img

        else:
            result = transformed
        result = np.clip(result, 0, 255).astype(np.uint8)
        self.update_right_panel(result)

    ####################################################################################################################

    def apply_histogram_equalization(self, channel):
        if self.main_app.original_image_array is None:
            print("No image loaded!")
            return

        import numpy as np

        img = self.main_app.original_image_array.copy()

        # Helper function to equalize one channel
        def equalize_channel(arr):
            # Flatten, compute histogram
            hist, _ = np.histogram(arr, bins=256, range=(0, 255))
            cdf = hist.cumsum()  # cumulative distribution function
            cdf_normalized = (cdf / cdf[-1]) * 255
            # Map original values to equalized
            arr_eq = np.interp(arr.flatten(), np.arange(256), cdf_normalized).reshape(arr.shape).astype(np.uint8)
            return arr_eq

        if channel == "wszystkie":
            # Equalize all channels independently
            for c in range(3):
                img[:, :, c] = equalize_channel(img[:, :, c])
        else:
            ch_idx = {"czerwony": 0, "zielony": 1, "niebieski": 2}[channel]
            img[:, :, ch_idx] = equalize_channel(img[:, :, ch_idx])

        self.update_right_panel(img)