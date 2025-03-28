import tkinter as tk
import numpy as np
from PIL import Image
from application.pages.baseSubpage import BaseSubpage

# Page
class MorphologicalOperations(BaseSubpage):

    def __init__(self, master, main_app):
        # Subpage definition
        subpages = {
            "dilation": {
                "label": "Dylacja"
            },
            "erosion": {
                "label": "Erozja"
            },
            "open": {
                "label": "Otwarcie"
            },
            "close": {
                "label": "Zamknięcie"
            }

        }
        # Default subpage
        default_subpage = "dilation"
        super().__init__(master, main_app, subpages, default_subpage)

    ####################################################################################################################

    def _build_morph_subpage(self, op_type):
        # Common binary image check
        self.show_default_image()
        if self.main_app.original_image_array is None:
            return
        uniq = np.unique(self.main_app.original_image_array)
        if not set(uniq).issubset({0, 255}):
            return
        # Left half: Structural element grid (default provided if not present)
        if not hasattr(self.main_app, "custom_struct_elem"):
            self.create_default_struct_elem()
        self.show_default_image()
        # Right half: Controls for element size and operation
        right_frame = tk.Frame(self.content_area)
        right_frame.place(relx=0.75, rely=0.5, relwidth=0.45, relheight=1, anchor="center")
        controls_frame = tk.Frame(right_frame)
        controls_frame.pack(expand=True, fill="x", padx=10, pady=10)

        tk.Label(controls_frame, text="Rozmiar (wiersze):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        size_var = tk.StringVar(value="3")
        tk.Entry(controls_frame, textvariable=size_var, width=5).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tk.Label(controls_frame, text="Rozmiar (kolumny):").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        col_var = tk.StringVar(value="3")
        tk.Entry(controls_frame, textvariable=col_var, width=5).grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # Determine operation-specific button(s)
        if op_type == "dilation":
            btn_text = "Zastosuj dylację"
            cmd = self.apply_dilation
        elif op_type == "erosion":
            btn_text = "Zastosuj erozję"
            cmd = self.apply_erosion
        elif op_type == "open":
            btn_text = "Operacja otwarcia"
            cmd = self.apply_opening
        elif op_type == "close":
            btn_text = "Operacja zamknięcia)"
            cmd = self.apply_closing
        else:
            btn_text = ""
            cmd = None

        tk.Button(controls_frame, text="Zmień rozmiar elementu",
                  command=lambda: self.update_struct_elem(size_var.get(), col_var.get())
                  ).grid(row=1, column=0, columnspan=4, pady=5)

        if cmd:
            tk.Button(controls_frame, text=btn_text, command=cmd
                      ).grid(row=2, column=0, columnspan=4, pady=5)

        self.update_struct_elem(size_var.get(), col_var.get())
        self.create_default_struct_elem()

    def build_subpage(self, page_key):
        if page_key in {"dilation", "erosion", "open", "close"}:
            self._build_morph_subpage(page_key)
        else:
            tk.Label(self.content_area, text="Podstrona pusta").pack()

    ####################################################################################################################

    def create_default_struct_elem(self):
        n = 3
        default = np.empty((n, n), dtype=object)
        left_frame = tk.Frame(self.content_area)
        left_frame.place(relx=0.25, rely=0.5, relwidth=0.45, relheight=1, anchor="center")
        self.struct_elem_frame = tk.Frame(left_frame)
        self.struct_elem_frame.pack(expand=True, fill="both")
        for i in range(n):
            for j in range(n):
                color = "black" if (i == n // 2 and j == n // 2) else "white"
                btn = tk.Button(self.struct_elem_frame, bg=color, relief="raised", borderwidth=1,
                                command=lambda i=i, j=j: self.toggle_cell(i, j))
                btn.grid(row=i, column=j, padx=2, pady=2, sticky="nsew")
                default[i, j] = btn
                self.struct_elem_frame.grid_columnconfigure(j, weight=1)
            self.struct_elem_frame.grid_rowconfigure(i, weight=1)
        self.main_app.custom_struct_elem = default

    def toggle_cell(self, i, j):
        btn = self.main_app.custom_struct_elem[i, j]
        current = btn.cget("bg")
        btn.config(bg="black" if current == "white" else "white")

    def update_struct_elem(self, size_str, col_str):
        try:
            m = int(size_str)
            n = int(col_str)
        except Exception:
            return
        if hasattr(self, 'struct_elem_frame'):
            self.struct_elem_frame.destroy()
        left_frame = tk.Frame(self.content_area)
        left_frame.place(relx=0.25, rely=0.5, relwidth=0.45, relheight=1, anchor="center")
        self.struct_elem_frame = tk.Frame(left_frame)
        self.struct_elem_frame.pack(expand=True, fill="both")
        new_elem = np.empty((n, m), dtype=object)
        for i in range(n):
            for j in range(m):
                color = "black" if (i == n // 2 and j == m // 2) else "white"
                btn = tk.Button(self.struct_elem_frame, bg=color, relief="raised", borderwidth=1,
                                command=lambda i=i, j=j: self.toggle_cell(i, j))
                btn.grid(row=i, column=j, padx=2, pady=2, sticky="nsew")
                new_elem[i, j] = btn
                self.struct_elem_frame.grid_columnconfigure(j, weight=1)
            self.struct_elem_frame.grid_rowconfigure(i, weight=1)
        self.main_app.custom_struct_elem = new_elem

    def apply_dilation(self):
        if self.main_app.original_image_array is None:
            return
        if not hasattr(self.main_app, "custom_struct_elem"):
            return

        n, m = self.main_app.custom_struct_elem.shape
        se = np.zeros((n, m), dtype=np.uint8)
        for i in range(n):
            for j in range(m):
                btn = self.main_app.custom_struct_elem[i, j]
                se[i, j] = 1 if btn.cget("bg") == "black" else 0

        orig = self.main_app.original_image_array.astype(np.uint8)
        pad_r = n // 2
        pad_c = m // 2
        padded = np.pad(orig, ((pad_r, pad_r), (pad_c, pad_c), (0, 0)), mode='constant', constant_values=255)
        out = np.copy(orig)
        H, W, _ = orig.shape
        for i in range(H):
            for j in range(W):
                neighborhood = padded[i:i + n, j:j + m, 0]
                if np.any(neighborhood[se == 1] == 0):
                    out[i, j] = [0, 0, 0]
                else:
                    out[i, j] = [255, 255, 255]
        self.main_app.modified_image = Image.fromarray(out)
        self.main_app.modified_image_array = out
        self.update_right_panel(out)

    def apply_dilation_on_array(self, image_array, se):
        orig = image_array.astype(np.uint8)
        n, m = se.shape
        pad_r = n // 2
        pad_c = m // 2
        padded = np.pad(orig, ((pad_r, pad_r), (pad_c, pad_c), (0, 0)), mode='constant', constant_values=255)
        out = np.copy(orig)
        H, W, _ = orig.shape
        for i in range(H):
            for j in range(W):
                neighborhood = padded[i:i + n, j:j + m, 0]
                if np.any(neighborhood[se == 1] == 0):
                    out[i, j] = [0, 0, 0]
                else:
                    out[i, j] = [255, 255, 255]
        return out

    ####################################################################################################################

    def apply_erosion(self):
        if self.main_app.original_image_array is None:
            return
        if not hasattr(self.main_app, "custom_struct_elem"):
            return

        n, m = self.main_app.custom_struct_elem.shape
        se = np.zeros((n, m), dtype=np.uint8)
        for i in range(n):
            for j in range(m):
                btn = self.main_app.custom_struct_elem[i, j]
                se[i, j] = 1 if btn.cget("bg") == "black" else 0

        eroded = self.apply_erosion_on_array(self.main_app.original_image_array, se)
        self.main_app.modified_image = Image.fromarray(eroded)
        self.main_app.modified_image_array = eroded
        self.update_right_panel(eroded)

    def apply_erosion_on_array(self, image_array, se):
        orig = image_array.astype(np.uint8)
        n, m = se.shape
        pad_r = n // 2
        pad_c = m // 2
        padded = np.pad(orig, ((pad_r, pad_r), (pad_c, pad_c), (0, 0)), mode='constant', constant_values=255)
        out = np.copy(orig)
        H, W, _ = orig.shape
        for i in range(H):
            for j in range(W):
                neighborhood = padded[i:i + n, j:j + m, 0]
                if np.all(neighborhood[se == 1] == 0):
                    out[i, j] = [0, 0, 0]
                else:
                    out[i, j] = [255, 255, 255]
        return out

    ####################################################################################################################

    def apply_opening(self):
        if self.main_app.original_image_array is None:
            return
        n, m = self.main_app.custom_struct_elem.shape
        se = np.zeros((n, m), dtype=np.uint8)
        for i in range(n):
            for j in range(m):
                btn = self.main_app.custom_struct_elem[i, j]
                se[i, j] = 1 if btn.cget("bg") == "black" else 0
        eroded = self.apply_erosion_on_array(self.main_app.original_image_array, se)
        opened = self.apply_dilation_on_array(eroded, se)
        self.main_app.modified_image = Image.fromarray(opened)
        self.main_app.modified_image_array = opened
        self.update_right_panel(opened)

    ####################################################################################################################

    def apply_closing(self):
        if self.main_app.original_image_array is None:
            return
        n, m = self.main_app.custom_struct_elem.shape
        se = np.zeros((n, m), dtype=np.uint8)
        for i in range(n):
            for j in range(m):
                btn = self.main_app.custom_struct_elem[i, j]
                se[i, j] = 1 if btn.cget("bg") == "black" else 0
        dilated = self.apply_dilation_on_array(self.main_app.original_image_array, se)
        closed = self.apply_erosion_on_array(dilated, se)
        self.main_app.modified_image = Image.fromarray(closed)
        self.main_app.modified_image_array = closed
        self.update_right_panel(closed)