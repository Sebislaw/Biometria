import tkinter as tk
import numpy as np
from PIL import Image
from application.pages.baseSubpage import BaseSubpage

# Page
class GraphicalFiltering(BaseSubpage):

    def __init__(self, master, main_app):
        # Subpage definition
        subpages = {
            "mean": {
                "label": "Uśredniający"
            },
            "gauss": {
                "label": "Gaussa"
            },
            "sharpening": {
                "label": "Wyostrzający"
            },
            "custom": {
                "label": "Dowolny filtr"
            }
        }
        # Default subpage
        default_subpage = "mean"
        self.slider_update_id = None
        super().__init__(master, main_app, subpages, default_subpage)

    ####################################################################################################################

    def build_subpage(self, page_key):
        if page_key == "mean":
            self.show_default_image()

            n = self.main_app.mean_size.get()
            center = self.main_app.mean_center.get()
            kernel = self.get_default_mean_kernel(n, center)

            self.show_matrix(kernel)
            right_frame = tk.Frame(self.content_area)
            right_frame.place(relx=0.75, rely=0.5, relwidth=0.5, relheight=1, anchor="center")

            # Right half: Functional controls
            controls_frame = tk.Frame(right_frame)
            controls_frame.pack(expand=True)
            tk.Label(controls_frame, text="Kernel Size:").grid(row=0, column=0, padx=5, pady=5)
            size_var = self.main_app.mean_size
            tk.Entry(controls_frame, textvariable=size_var, width=5).grid(row=0, column=1, padx=5, pady=5)

            tk.Label(controls_frame, text="Central Value:").grid(row=1, column=0, padx=5, pady=5)
            center_var = self.main_app.mean_center
            tk.Entry(controls_frame, textvariable=center_var, width=5).grid(row=1, column=1, padx=5, pady=5)

            # Two buttons: one to update kernel, one to apply it
            tk.Button(controls_frame, text="Update Kernel",
                      command=lambda: self.update_kernel("mean")
                      ).grid(row=2, column=0, columnspan=2, pady=10)
            tk.Button(controls_frame, text="Apply Filter",
                      command=lambda: self.apply_filter(kernel.astype(np.float32) / kernel.sum())
                      ).grid(row=4, column=0, columnspan=2, pady=10)

        elif page_key == "gauss":
            self.show_default_image()

            n = self.main_app.gaussian_size.get()
            sigma = self.main_app.gaussian_sigma.get()
            kernel = np.round(self.get_default_gaussian_kernel(n, sigma=sigma)).astype(np.int32)

            self.show_matrix(kernel)
            right_frame = tk.Frame(self.content_area)
            right_frame.place(relx=0.75, rely=0.5, relwidth=0.5, relheight=1, anchor="center")

            # Right half: Functional controls
            controls_frame = tk.Frame(right_frame)
            controls_frame.pack(expand=True)
            tk.Label(controls_frame, text="Kernel Size:").grid(row=0, column=0, padx=5, pady=5)
            size_var = self.main_app.gaussian_size
            tk.Entry(controls_frame, textvariable=size_var, width=5).grid(row=0, column=1, padx=5, pady=5)

            tk.Label(controls_frame, text="Parametr sigma:").grid(row=1, column=0, padx=5, pady=5)
            center_var = self.main_app.gaussian_sigma
            tk.Entry(controls_frame, textvariable=center_var, width=5).grid(row=1, column=1, padx=5, pady=5)

            # Two buttons: one to update kernel, one to apply it
            tk.Button(controls_frame, text="Update Kernel",
                      command=lambda: self.update_kernel("gauss")
                      ).grid(row=2, column=0, columnspan=2, pady=10)
            tk.Button(controls_frame, text="Apply Filter",
                      command=lambda: self.apply_filter(kernel.astype(np.float32) / kernel.sum())
                      ).grid(row=4, column=0, columnspan=2, pady=10)

        elif page_key == "sharpening":
            self.show_default_image()

            center_value = self.main_app.sharpening_center.get()
            kernel = self.get_default_sharpening_kernel(center_value)

            self.show_matrix(kernel)
            right_frame = tk.Frame(self.content_area)
            right_frame.place(relx=0.75, rely=0.5, relwidth=0.5, relheight=1, anchor="center")

            # Right half: Functional controls
            controls_frame = tk.Frame(right_frame)
            controls_frame.pack(expand=True)

            tk.Label(controls_frame, text="Central Value:").grid(row=1, column=0, padx=5, pady=5)
            center_var = self.main_app.sharpening_center
            tk.Entry(controls_frame, textvariable=center_var, width=5,).grid(row=1, column=1, padx=5, pady=5)

            # Two buttons: one to update kernel, one to apply it
            tk.Button(controls_frame, text="Update Kernel",
                      command=lambda: self.update_kernel("sharpening")
                      ).grid(row=2, column=0, columnspan=2, pady=10)
            tk.Button(controls_frame, text="Apply Filter",
                      command=lambda: self.apply_filter(kernel.astype(np.float32) / (center_value - 4)) if center_value >= 5 else None
                      ).grid(row=4, column=0, columnspan=2, pady=10)

        elif page_key == "custom":
            self.show_default_image()

            # Left half: Editable kernel matrix
            left_frame = tk.Frame(self.content_area)
            left_frame.place(relx=0.25, rely=0.5, relwidth=0.5, relheight=1, anchor="center")
            matrix_frame = tk.Frame(left_frame, borderwidth=2, relief="ridge")
            matrix_frame.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9, anchor="center")
            n = self.main_app.custom_kernel_size.get()  # IntVar
            kernel_entries = np.empty((n, n), dtype=object)
            for i in range(n):
                for j in range(n):
                    e = tk.Entry(matrix_frame, justify="center")
                    e.grid(row=i, column=j, padx=2, pady=2, sticky="nsew")
                    e.insert(0, "1")
                    kernel_entries[i, j] = e
                    matrix_frame.grid_columnconfigure(j, weight=1)
                matrix_frame.grid_rowconfigure(i, weight=1)
            if self.main_app.custom_kernel is None:
                self.main_app.custom_kernel = kernel_entries

            # Right half: Functional controls
            right_frame = tk.Frame(self.content_area)
            right_frame.place(relx=0.75, rely=0.5, relwidth=0.5, relheight=1, anchor="center")
            controls_frame = tk.Frame(right_frame)
            controls_frame.pack(expand=True)
            tk.Label(controls_frame, text="Kernel Size:").grid(row=0, column=0, padx=5, pady=5)
            tk.Entry(controls_frame, textvariable=self.main_app.custom_kernel_size, width=5).grid(row=0, column=1,
                                                                                                  padx=5, pady=5)
            tk.Button(controls_frame, text="Update Matrix",
                      command=lambda: self.update_kernel("custom")
                      ).grid(row=1, column=0, columnspan=2, pady=5)
            tk.Button(controls_frame, text="Apply Filter",
                      command=lambda: self.apply_filter(self.get_numeric_kernel(kernel_entries))
                      ).grid(row=2, column=0, columnspan=2, pady=5)



        else:
            tk.Label(self.content_area, text="Podstrona pusta").pack()

    ####################################################################################################################

    def show_matrix(self, kernel):
        # Divide content_area into two halves
        left_frame = tk.Frame(self.content_area)
        left_frame.place(relx=0.25, rely=0.5, relwidth=0.5, relheight=1, anchor="center")
        self.content_area.columnconfigure(0, weight=1)
        self.content_area.columnconfigure(1, weight=1)

        # Left half: Centered kernel matrix display (integer values)
        matrix_frame = tk.Frame(left_frame, borderwidth=2, relief="ridge")
        matrix_frame.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9, anchor="center")
        rows, cols = kernel.shape
        for i in range(rows):
            matrix_frame.grid_rowconfigure(i, weight=1)
            for j in range(cols):
                matrix_frame.grid_columnconfigure(j, weight=1)
                tk.Label(matrix_frame, text=f"{int(kernel[i, j])}", borderwidth=1,
                         relief="solid").grid(row=i, column=j, padx=2, pady=2, sticky="nsew")

    def update_kernel(self, type):
        try:
            self.build_subpage(type)
        except Exception:
            return

    ####################################################################################################################

    def get_default_mean_kernel(self, n, center=1.0):
        kernel = np.ones((n, n), dtype=np.float32)
        if n % 2 == 1:
            # Odd-sized: single center cell
            kernel[n // 2, n // 2] = center
        else:
            # Even-sized: set the four central cells
            c = n // 2
            kernel[c - 1, c - 1] = center
            kernel[c - 1, c] = center
            kernel[c, c - 1] = center
            kernel[c, c] = center
        return kernel

    ####################################################################################################################

    def get_default_gaussian_kernel(self, n, sigma=1.0):
        ax = np.linspace(-(n // 2), n // 2, n)
        xx, yy = np.meshgrid(ax, ax)
        kernel = np.exp(-(xx ** 2 + yy ** 2) / (2 * sigma ** 2))
        return kernel

    ####################################################################################################################

    def get_default_sharpening_kernel(self, center=5):
        kernel = np.array([[0, -1, -0],
                           [-1, center, -1],
                           [0, -1, -0]])
        return kernel

    ####################################################################################################################

    def get_numeric_kernel(self, kernel_entries):
        n = kernel_entries.shape[0]
        k = np.zeros((n, n), dtype=np.float32)
        for i in range(n):
            for j in range(n):
                try:
                    k[i, j] = float(kernel_entries[i, j].get())
                except:
                    k[i, j] = 0.0
        if k.sum() != 0:
            k /= k.sum()
        return k

    ####################################################################################################################

    def apply_filter(self, kernel):
        if self.main_app.original_image_array is None:
            print("No image loaded!")
            return
        filtered = self.convolve_image(self.main_app.original_image_array, kernel)
        self.update_right_panel(filtered)

    def convolve_image(self, img_array, kernel):
        H, W, C = img_array.shape
        kH, kW = kernel.shape
        pad_h, pad_w = kH // 2, kW // 2
        padded = np.pad(img_array, ((pad_h, pad_h), (pad_w, pad_w), (0, 0)), mode='constant')
        out = np.zeros((H, W, C), dtype=np.float32)
        for i in range(H):
            for j in range(W):
                for c in range(C):
                    out[i, j, c] = np.sum(padded[i:i + kH, j:j + kW, c] * kernel)
        return np.clip(out, 0, 255).astype(np.uint8)
