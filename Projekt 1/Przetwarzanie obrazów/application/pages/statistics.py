import tkinter as tk
import numpy as np
from application.pages.baseSubpage import BaseSubpage

# Page
class Statistics(BaseSubpage):

    def __init__(self, master, main_app):
        # Subpage definition
        subpages = {
            "histogram": {
                "label": "Histogram"
            },
            "projections": {
                "label": "Projekcje"
            },
            "colours": {
                "label": "Kolory"
            }
        }
        # Default subpage
        default_subpage = "histogram"
        self.slider_update_id = None
        super().__init__(master, main_app, subpages, default_subpage)

    ####################################################################################################################

    def build_subpage(self, page_key):

        if page_key == "histogram":
            if self.main_app.original_image_array is None:
                return
            self.canvas = tk.Canvas(self.content_area, bg=self.content_area.cget("bg"))
            self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.canvas.bind("<Configure>", self.draw_histograms)
            self.convert_greyscale()

        elif page_key == "projections":
            if self.main_app.modified_image_array is None:
                return
            slider = tk.Scale(
                self.content_area,
                from_= 0,
                to=255,
                orient="vertical",
                variable=self.main_app.bin_thresh_value_statistics,
                label="Próg progowania",
                command=lambda e: self.on_slider_change(self.binarize_with_slider)
            )
            slider.place(relx=0.5, rely=0.5, relwidth=0.82, relheight=1, anchor="center")
            self.binarize_with_slider()

        elif page_key == "colours":
            if self.main_app.original_image_array is None:
                return

            from PIL import Image, ImageTk
            import numpy as np

            orig = self.main_app.original_image_array.copy()

            # Create Red, Green, and Blue images
            red = orig.copy()
            red[:, :, 1] = 0
            red[:, :, 2] = 0

            green = orig.copy()
            green[:, :, 0] = 0
            green[:, :, 2] = 0

            blue = orig.copy()
            blue[:, :, 0] = 0
            blue[:, :, 1] = 0

            # Create canvas widgets to hold images with relative border thickness
            red_canvas = tk.Canvas(self.content_area)
            green_canvas = tk.Canvas(self.content_area)
            blue_canvas = tk.Canvas(self.content_area)

            # Position canvases
            red_canvas.place(relx=0.17, rely=0.5, relwidth=0.3, relheight=0.9, anchor="center")
            green_canvas.place(relx=0.5, rely=0.5, relwidth=0.3, relheight=0.9, anchor="center")
            blue_canvas.place(relx=0.83, rely=0.5, relwidth=0.3, relheight=0.9, anchor="center")

            def update_images(event=None):
                for canvas, img_data in zip([red_canvas, green_canvas, blue_canvas], [red, green, blue]):
                    w = canvas.winfo_width()
                    h = canvas.winfo_height()

                    # Calculate border thickness relative to width
                    border_thickness = int(w * 0.02)  # 2% of width

                    # Maintain aspect ratio
                    img_h, img_w = img_data.shape[:2]
                    scale_factor = min((w - 2 * border_thickness) / img_w, (h - 2 * border_thickness) / img_h)
                    new_w = int(img_w * scale_factor)
                    new_h = int(img_h * scale_factor)

                    resized_img = ImageTk.PhotoImage(Image.fromarray(img_data).resize((new_w, new_h)))

                    # Center image
                    canvas.create_image(w // 2, h // 2, image=resized_img, anchor="center")

                    # Save reference to prevent garbage collection
                    canvas.image = resized_img

            # Bind resizing event
            red_canvas.bind("<Configure>", update_images)
            green_canvas.bind("<Configure>", update_images)
            blue_canvas.bind("<Configure>", update_images)

            self.convert_greyscale()

    def on_slider_change(self, update_func):
        if self.slider_update_id is not None:
            self.after_cancel(self.slider_update_id)
        self.slider_update_id = self.after(250, update_func)

    ####################################################################################################################

    def convert_greyscale(self):
        """
        Blends the original image with its greyscale version based on the slider value.
        """
        # Check that the original image array is loaded
        if self.main_app.original_image_array is None:
            print("No image loaded!")
            return
        alpha = 1
        orig_arr = self.main_app.original_image_array.astype(np.float32)
        grey = orig_arr.mean(axis=2).astype(np.uint8)
        grey_rgb = np.stack((grey,) * 3, axis=-1).astype(np.float32)
        blended = np.clip((1 - alpha) * orig_arr + alpha * grey_rgb, 0, 255).astype(np.uint8)
        self.update_right_panel(blended)

    def draw_histograms(self, event=None):

        orig = self.main_app.original_image_array
        grey = np.mean(orig, axis=2).astype(np.uint8)
        hist_brightness, _ = np.histogram(grey, bins=256, range=(0, 255))
        hist_red, _ = np.histogram(orig[:, :, 0], bins=256, range=(0, 255))
        hist_green, _ = np.histogram(orig[:, :, 1], bins=256, range=(0, 255))
        hist_blue, _ = np.histogram(orig[:, :, 2], bins=256, range=(0, 255))

        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        # Margins as percentages of canvas dimensions
        margin_left = 0.05 * w
        margin_right = 0.05 * w
        margin_top = 0.15 * h
        margin_bottom = 0.15 * h

        col_width = (w - margin_left - margin_right) / 4.0
        available_height = h - margin_top - margin_bottom

        titles = ["Jasność", "Czerwony", "Zielony", "Niebieski"]
        colors = ["black", "red", "green", "blue"]
        hists = [hist_brightness, hist_red, hist_green, hist_blue]
        max_val = max(hist_brightness.max(), hist_red.max(), hist_green.max(), hist_blue.max()) or 1

        col_spacing = 0.02 * w  # 2% of the canvas width as spacing
        col_width = (w - margin_left - margin_right - (3 * col_spacing)) / 4.0  # Adjusted column width

        for idx in range(4):
            x0 = margin_left + idx * (col_width + col_spacing)

            # Draw border around each plot
            self.canvas.create_rectangle(x0, margin_top, x0 + col_width, h - margin_bottom,
                                         outline="black", width=1)

            # Draw title with a smaller font
            self.canvas.create_text(x0 + col_width / 2, margin_top / 2, text=titles[idx],
                                    fill=colors[idx], font=("Helvetica", 10, "bold"))

            # Draw tick marks and labels
            for tick, label in zip([0, 128, 255], ["0", "128", "255"]):
                tick_x = x0 + (tick / 255.0) * col_width
                self.canvas.create_line(tick_x, h - margin_bottom - 5, tick_x, h - margin_bottom, fill="black")
                self.canvas.create_text(tick_x, h - margin_bottom + 10, text=label,
                                        fill="black", font=("Helvetica", 8))
            binw = col_width / 256.0
            for i, count in enumerate(hists[idx]):
                bh = (count / max_val) * (available_height - 20)  # reserve space for ticks
                self.canvas.create_rectangle(x0 + i * binw, h - margin_bottom - bh,
                                             x0 + (i + 1) * binw, h - margin_bottom,
                                             fill=colors[idx], outline=colors[idx])

    ####################################################################################################################

    def binarize_with_slider(self):
        # Binarization slider: value from 0 to 255 used as threshold
        if self.main_app.original_image_array is None:
            print("No image loaded!")
            return
        threshold = self.main_app.bin_thresh_value_statistics.get()
        orig_arr = self.main_app.original_image_array.astype(np.float32)
        # # Convert to grayscale first
        grey = orig_arr.mean(axis=2)
        binary = np.where(grey < threshold, 0, 255).astype(np.uint8)
        binary_rgb = np.stack((binary,) * 3, axis=-1)

        # Binarize the modified image at threshold 128
        # grey = np.mean(orig_arr, axis=2).astype(np.uint8)
        # binary = np.where(grey < self.main_app.bin_thresh_value_statistics.get(), 0, 255).astype(np.uint8)
        self.proj_col = (binary == 0).sum(axis=0)  # black pixel count per column
        self.proj_row = (binary == 0).sum(axis=1)  # black pixel count per row

        # Create two canvases: left for column projections, right for row projections.
        self.left_canvas = tk.Canvas(self.content_area, bg=self.content_area.cget("bg"))
        self.right_canvas = tk.Canvas(self.content_area, bg=self.content_area.cget("bg"))
        self.left_canvas.place(relx=0, rely=0, relwidth=0.5, relheight=1)
        self.right_canvas.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

        self.left_canvas.bind("<Configure>", self.draw_projections)
        self.right_canvas.bind("<Configure>", self.draw_projections)

        self.update_right_panel(binary_rgb)

    def draw_projections(self, event=None):
        self.left_canvas.delete("all")
        self.right_canvas.delete("all")

        # Define canvas sizes relative to the window
        self.left_canvas.place(relx=0.25, rely=0, relwidth=0.25, relheight=1)  # 80% height
        self.right_canvas.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

        # Left canvas (Row Projection)
        lw = self.left_canvas.winfo_width()
        lh = self.left_canvas.winfo_height()
        m_left = 0.05 * lw
        m_right = 0.05 * lw
        m_top = 0.15 * lh
        m_bottom = 0.15 * lh
        avail_w = lw - m_left - m_right
        avail_h = lh - m_top - m_bottom

        # Draw border and title
        self.left_canvas.create_rectangle(m_left, m_top, m_left + avail_w, m_top + avail_h, outline="black")
        self.left_canvas.create_text(lw / 2, m_top / 2, text="Projekcja pozioma", font=("Helvetica", 10),
                                fill="black")

        num_rows = len(self.proj_row)
        bin_h = avail_h / num_rows
        max_row = self.proj_row.max() or 1

        for i, count in enumerate(self.proj_row):
            bar_w = (count / max_row) * avail_w
            self.left_canvas.create_rectangle(m_left + avail_w - bar_w,
                                         m_top + i * bin_h,
                                         m_left + avail_w,
                                         m_top + (i + 1) * bin_h,
                                         fill="black", outline="black")

        # Right canvas (Column Projection)
        rw = self.right_canvas.winfo_width()
        rh = self.right_canvas.winfo_height()
        m_left_r = 0.05 * rw
        m_right_r = 0.05 * rw
        m_top_r = 0.15 * rh
        m_bottom_r = 0.15 * rh
        avail_w_r = rw - m_left_r - m_right_r
        avail_h_r = rh - m_top_r - m_bottom_r

        # Draw border and title
        self.right_canvas.create_rectangle(m_left_r, m_top_r, m_left_r + avail_w_r, m_top_r + avail_h_r,
                                           outline="black")
        self.right_canvas.create_text(rw / 2, m_top_r / 2, text="Projekcja pionowa", font=("Helvetica", 10),
                                      fill="black")

        num_cols = len(self.proj_col)
        bin_w = avail_w_r / num_cols
        max_col = self.proj_col.max() or 1

        for i, count in enumerate(self.proj_col):
            bar_h = (count / max_col) * avail_h_r
            self.right_canvas.create_rectangle(m_left_r + i * bin_w,
                                               m_top_r + avail_h_r - bar_h,  # Flip on y-axis
                                               m_left_r + (i + 1) * bin_w,
                                               m_top_r + avail_h_r,
                                               fill="black", outline="black")
