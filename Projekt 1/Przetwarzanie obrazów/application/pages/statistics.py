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
        default_subpage = "greyscale"
        self.slider_update_id = None
        super().__init__(master, main_app, subpages, default_subpage)

    ####################################################################################################################

    def build_subpage(self, page_key):

        if page_key == "histogram":
            if self.main_app.original_image_array is None:
                tk.Label(self.content_area, text="No image loaded!").pack()
                return
            import numpy as np
            # Use original image for color histograms; create full greyscale from right-panel image
            orig = self.main_app.original_image_array
            grey = np.mean(orig, axis=2).astype(np.uint8)
            hist_brightness, _ = np.histogram(grey, bins=256, range=(0, 255))
            hist_red, _ = np.histogram(orig[:, :, 0], bins=256, range=(0, 255))
            hist_green, _ = np.histogram(orig[:, :, 1], bins=256, range=(0, 255))
            hist_blue, _ = np.histogram(orig[:, :, 2], bins=256, range=(0, 255))
            canvas = tk.Canvas(self.content_area, bg="white")
            canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
            # Assume fixed canvas height; draw four histograms in one row with no gap.
            ch = 200
            canvas.config(height=ch)
            max_val = max(hist_brightness.max(), hist_red.max(), hist_green.max(), hist_blue.max())

            def draw_hist(x, w, hist, col):
                binw = w / 256.0
                for i, count in enumerate(hist):
                    bh = (count / max_val) * ch
                    canvas.create_rectangle(x + i * binw, ch - bh, x + (i + 1) * binw, ch, fill=col, outline=col)

            total_w = 800  # adjust as needed
            draw_hist(0, total_w / 4, hist_brightness, "black")
            draw_hist(total_w / 4, total_w / 4, hist_red, "red")
            draw_hist(total_w / 2, total_w / 4, hist_green, "green")
            draw_hist(3 * total_w / 4, total_w / 4, hist_blue, "blue")
        elif page_key == "projections":
            if self.main_app.modified_image_array is None:
                tk.Label(self.content_area, text="No image loaded!").pack()
                return
            import numpy as np
            # Binarize right panel image at threshold 128.
            grey = np.mean(self.main_app.modified_image_array, axis=2).astype(np.uint8)
            binary = np.where(grey < 128, 0, 255).astype(np.uint8)
            proj_col = (binary == 0).sum(axis=0)
            proj_row = (binary == 0).sum(axis=1)
            left_canvas = tk.Canvas(self.content_area, bg="white")
            right_canvas = tk.Canvas(self.content_area, bg="white")
            left_canvas.place(relx=0, rely=0, relwidth=0.5, relheight=1)
            right_canvas.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)
            cw = 400;
            ch = 200
            max_col = proj_col.max() or 1
            max_row = proj_row.max() or 1
            binw = cw / len(proj_col)
            for i, count in enumerate(proj_col):
                bh = (count / max_col) * ch
                left_canvas.create_rectangle(i * binw, ch - bh, (i + 1) * binw, ch, fill="black", outline="black")
            binh = ch / len(proj_row)
            for i, count in enumerate(proj_row):
                bw = (count / max_row) * cw
                right_canvas.create_rectangle(0, i * binh, bw, (i + 1) * binh, fill="black", outline="black")
        elif page_key == "colours":
            if self.main_app.original_image_array is None:
                tk.Label(self.content_area, text="No image loaded!").pack()
                return
            from PIL import Image, ImageTk
            import numpy as np
            orig = self.main_app.original_image_array.copy()
            red = orig.copy();
            red[:, :, 1] = 0;
            red[:, :, 2] = 0
            green = orig.copy();
            green[:, :, 0] = 0;
            green[:, :, 2] = 0
            blue = orig.copy();
            blue[:, :, 0] = 0;
            blue[:, :, 1] = 0
            red_img = ImageTk.PhotoImage(Image.fromarray(red))
            green_img = ImageTk.PhotoImage(Image.fromarray(green))
            blue_img = ImageTk.PhotoImage(Image.fromarray(blue))
            # Place three images in one row, no gap.
            tk.Label(self.content_area, image=red_img).place(relx=0.17, rely=0.5, anchor="center")
            tk.Label(self.content_area, image=green_img).place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(self.content_area, image=blue_img).place(relx=0.83, rely=0.5, anchor="center")
            # Save references
            self.red_img, self.green_img, self.blue_img = red_img, green_img, blue_img
        else:
            tk.Label(self.content_area, text="Podstrona pusta").pack()


    ####################################################################################################################


    ####################################################################################################################



    ####################################################################################################################



    ####################################################################################################################



    ####################################################################################################################

