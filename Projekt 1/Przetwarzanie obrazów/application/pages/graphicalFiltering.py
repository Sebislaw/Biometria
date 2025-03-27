import tkinter as tk
import numpy as np
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
            "robert": {
                "label": "Krzyż Robertsa"
            },
            "prewitt": {
                "label": "Operatory Prewitta"
            },
            "sobel": {
                "label": "Operatory Sobela"
            },
            "laplace": {
                "label": "Operatory Laplace'a"
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
        self.show_default_image()
        if page_key in {"mean", "gauss", "sharpening"}:
            self.show_matrix(self.get_filter_kernel(page_key))
            controls = {
                "mean": [("Rozmiar filtra:", self.main_app.mean_size),
                         ("Wartość centralna:", self.main_app.mean_center)],
                "gauss": [("Rozmiar filtra:", self.main_app.gaussian_size),
                          ("Parametr sigma:", self.main_app.gaussian_sigma)],
                "sharpening": [("Wartość centralna:", self.main_app.sharpening_center)]
            }
            self.create_right_panel(controls[page_key], page_key)

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
            tk.Label(controls_frame, text="Rozmiar filtra:").grid(row=0, column=0, padx=5, pady=5)
            tk.Entry(controls_frame, textvariable=self.main_app.custom_kernel_size, width=5).grid(row=0, column=1,
                                                                                                  padx=5, pady=5)
            tk.Button(controls_frame, text="Zaktualizuj rozmiar",
                      command=lambda: self.update_kernel("custom")
                      ).grid(row=1, column=0, columnspan=2, pady=5)
            tk.Button(controls_frame, text="Zastosuj filtr",
                      command=lambda: self.apply_filter(self.get_numeric_kernel(kernel_entries))
                      ).grid(row=2, column=0, columnspan=2, pady=5)

        elif page_key == "robert":
            left_frame = tk.Frame(self.content_area)
            left_frame.place(relx=0.25, rely=0.5, relwidth=0.5, relheight=1, anchor="center")
            right_frame = tk.Frame(self.content_area)
            right_frame.place(relx=0.75, rely=0.5, relwidth=0.5, relheight=1, anchor="center")
            controls_frame = tk.Frame(right_frame)
            controls_frame.pack(expand=True)

            # Dropdown to pick variant
            variant_var = tk.StringVar(value="Wariant 1")
            variants = list(self.roberts_options.keys())
            tk.OptionMenu(controls_frame, variant_var, *variants,
                          command=lambda _: self.show_roberts_matrices(variant_var.get(), left_frame)
                          ).grid(row=2, column=0, columnspan=2, pady=10)

            # Button to apply
            tk.Button(controls_frame, text="Zastosuj filtry",
                      command=lambda: self.apply_roberts(variant_var.get())
                      ).grid(row=4, column=0, columnspan=2, pady=10)

            # Show default matrices
            self.show_roberts_matrices(variant_var.get(), left_frame)

        elif page_key == "prewitt":
            self.create_filter_with_dropdown("Zastosuj filtr", self.prewitt_options)

        elif page_key == "sobel":
            self.create_filter_with_dropdown("Zastosuj filtr", self.sobel_options)

        elif page_key == "laplace":
            self.create_filter_with_dropdown("Zastosuj filtr", self.laplace_options)

    def show_roberts_matrices(self, variant, parent_frame):
        # Clear previous widgets
        for widget in parent_frame.winfo_children():
            widget.destroy()

        kernels = self.roberts_options[variant]

        # Left kernel matrix display
        left_matrix_frame = tk.Frame(parent_frame, borderwidth=2, relief="ridge")
        left_matrix_frame.place(relx=0.25, rely=0.5, relwidth=0.4, relheight=0.9, anchor="center")
        self.display_matrix(left_matrix_frame, kernels[0])

        # Right kernel matrix display
        right_matrix_frame = tk.Frame(parent_frame, borderwidth=2, relief="ridge")
        right_matrix_frame.place(relx=0.75, rely=0.5, relwidth=0.4, relheight=0.9, anchor="center")
        self.display_matrix(right_matrix_frame, kernels[1])

    def display_matrix(self, frame, kernel):
        rows, cols = kernel.shape
        for i in range(rows):
            frame.grid_rowconfigure(i, weight=1)
            for j in range(cols):
                frame.grid_columnconfigure(j, weight=1)
                tk.Label(frame, text=f"{kernel[i, j]:.0f}" if kernel[i, j].is_integer() else f"{kernel[i, j]:.2f}",
                         borderwidth=1, relief="solid").grid(row=i, column=j, padx=2, pady=2, sticky="nsew")

    def create_right_panel(self, controls, page_key):
        right_frame = tk.Frame(self.content_area)
        right_frame.place(relx=0.75, rely=0.5, relwidth=0.5, relheight=1, anchor="center")

        controls_frame = tk.Frame(right_frame)
        controls_frame.pack(expand=True)

        for row, (label, var) in enumerate(controls):
            tk.Label(controls_frame, text=label).grid(row=row, column=0, padx=5, pady=5)
            tk.Entry(controls_frame, textvariable=var, width=5).grid(row=row, column=1, padx=5, pady=5)

        tk.Button(controls_frame, text="Zaktualizuj rozmiar", command=lambda: self.update_kernel(page_key)).grid(
            row=len(controls), column=0, columnspan=2, pady=10)
        tk.Button(controls_frame, text="Zastosuj filtr",
                  command=lambda: self.apply_filter(self.get_filter_kernel(page_key))).grid(row=len(controls) + 2,
                                                                                            column=0, columnspan=2,
                                                                                            pady=10)
    def get_filter_kernel(self, page_key):
        if page_key == "mean":
            return self.get_default_mean_kernel(self.main_app.mean_size.get(), self.main_app.mean_center.get())
        elif page_key == "gauss":
            return np.round(
                self.get_default_gaussian_kernel(self.main_app.gaussian_size.get(), self.main_app.gaussian_sigma.get()),
                2).astype(np.float32)
        elif page_key == "sharpening":
            center_value = self.main_app.sharpening_center.get()
            return self.get_default_sharpening_kernel(center_value).astype(np.float32) / (
                        center_value - 4) if center_value >= 5 else None
        elif page_key == "custom":
            return self.get_numeric_kernel(self.main_app.custom_kernel)
        return None

    def create_filter_with_dropdown(self, button_text, options):
        left_frame = tk.Frame(self.content_area)
        left_frame.place(relx=0.25, rely=0.5, relwidth=0.5, relheight=1, anchor="center")
        right_frame = tk.Frame(self.content_area)
        right_frame.place(relx=0.75, rely=0.5, relwidth=0.5, relheight=1, anchor="center")
        controls_frame = tk.Frame(right_frame)
        controls_frame.pack(expand=True)

        option_var = tk.StringVar(value=list(options.keys())[0])
        tk.OptionMenu(controls_frame, option_var, *options.keys(),
                      command=lambda _: self.show_matrix(options[option_var.get()])).grid(row=2, column=0, columnspan=2,
                                                                                          pady=10)
        tk.Button(controls_frame, text=button_text, command=lambda: self.apply_filter(options[option_var.get()])).grid(row=4,
                                                                                                           column=0,
                                                                                                           columnspan=2,
                                                                                              pady=10)
        self.show_matrix(options[option_var.get()])

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
                tk.Label(matrix_frame, text=f"{kernel[i, j]:.0f}" if kernel[i, j].is_integer() else f"{kernel[i, j]:.2f}", borderwidth=1,
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

    def apply_roberts(self, variant_key):
        # Convolve with each 2×2 kernel, combine results (e.g., sqrt of sum of squares)
        if self.main_app.original_image_array is None:
            return

        kernels = self.roberts_options[variant_key]

        # Convert to float for convolution
        img = self.main_app.original_image_array.astype(np.float32)
        # Convolve with the two kernels
        res1 = self.convolve_image(img, kernels[0])
        res2 = self.convolve_image(img, kernels[1])
        # Combine (magnitude)
        combined = np.abs(res1) + np.abs(res2)
        combined = np.clip(combined, 0, 255).astype(np.uint8)
        self.update_right_panel(combined)

    ####################################################################################################################

    def apply_filter(self, kernel):
        if self.main_app.original_image_array is None:
            print("No image loaded!")
            return
        filtered = self.convolve_image(self.main_app.original_image_array, kernel)
        self.update_right_panel(filtered)

    def convolve_image(self, img_array, kernel):
        if kernel.sum() > 1:
            kernel = kernel / kernel.sum()
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

    # Roberts Cross variants:
    roberts_options = {
        "Wariant 1": [
            np.array([[1, -1],
                      [0, 0]]),
            np.array([[1, 0],
                      [-1, 0]])
        ],
        "Wariant 2": [
            np.array([[1, 0],
                      [0, -1]]),
            np.array([[0, 1],
                      [-1, 0]])
        ]
    }

    # Prewitt 8 rotations (3×3 each). Example subset:
    prewitt_options = {
        "0 stopni": np.array([[-1, -1, -1],
                              [0, 0, 0],
                              [1, 1, 1]]),

        "45 stopni": np.array([[0, -1, -1],
                               [1, 0, -1],
                               [1, 1, 0]]),

        "90 stopni": np.array([[1, 0, -1],
                               [1, 0, -1],
                               [1, 0, -1]]),

        "135 stopni": np.array([[1, 1, 0],
                                [1, 0, -1],
                                [0, -1, -1]]),

        "180 stopni": np.array([[1, 1, 1],
                                [0, 0, 0],
                                [-1, -1, -1]]),

        "225 stopni": np.array([[0, 1, 1],
                                [-1, 0, 1],
                                [-1, -1, 0]]),

        "270 stopni": np.array([[-1, 0, 1],
                                [-1, 0, 1],
                                [-1, 0, 1]]),

        "315 stopni": np.array([[-1, -1, 0],
                                [-1, 0, 1],
                                [0, 1, 1]])
    }

    # Sobel 8 rotations (3×3 each). Example subset:
    sobel_options = {
        "0 stopni": np.array([[-1, -2, -1],
                              [0, 0, 0],
                              [1, 2, 1]]),

        "45 stopni": np.array([[0, -1, -2],
                               [1, 0, -1],
                               [2, 1, 0]]),

        "90 stopni": np.array([[1, 0, -1],
                               [2, 0, -2],
                               [1, 0, -1]]),

        "135 stopni": np.array([[2, 1, 0],
                                [1, 0, -1],
                                [0, -1, -2]]),

        "180 stopni": np.array([[1, 2, 1],
                                [0, 0, 0],
                                [-1, -2, -1]]),

        "225 stopni": np.array([[0, 1, 2],
                                [-1, 0, 1],
                                [-2, -1, 0]]),

        "270 stopni": np.array([[-1, 0, 1],
                                [-2, 0, 2],
                                [-1, 0, 1]]),

        "315 stopni": np.array([[-2, -1, 0],
                                [-1, 0, 1],
                                [0, 1, 2]])
    }

    laplace_options = {
        "Poziomy": np.array([[0, 0, 0],
                              [-1, 2, -1],
                              [0, 0, 0]]),

        "Diagonalny": np.array([[-1, 0, 0],
                               [0, 2, 0],
                               [0, 0, -1]]),

        "Pionwy": np.array([[0, -1, 0],
                               [0, 2, 0],
                               [0, -1, 0]]),

        "Antydiagonaly": np.array([[0, 0, -1],
                                [0, 2, 0],
                                [-1, 0, 0]]),

        "Standardowy laplacjan": np.array([[-1, -1, -1],
                                [-1, 8, -1],
                                [-1, -1, -1]]),

        "Mocniejsze centrum": np.array([[1, -2, 1],
                                [-2, 4, -2],
                                [1, -2, 1]]),

        "Uproszczony laplacjan": np.array([[0, 1, 0],
                                [1, -4, 1],
                                [0, 1, 0]]),

        "Alternatywna wersja": np.array([[2, -1, 2],
                                [-1, -4, -1],
                                [2, -1, 2]])

    }

