import os
import random
import re
from collections import Counter

import math
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import cv2
from PIL import Image, ImageTk

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def draw_pupil_and_iris_boundaries(images, centers, pupil_radii, iris_radii,
                                   pupil_color=(255,255,0), iris_color=(0,255,255),
                                   thickness=2):
    n = len(images)
    cols = min(5, n)
    rows = math.ceil(n / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 3, rows * 3), facecolor='none')
    fig.patch.set_alpha(0)

    if not isinstance(axes, np.ndarray):
        axes = [axes]
    else:
        axes = axes.flatten()

    for ax, img, (cx, cy), rp, ri in zip(axes, images, centers, pupil_radii, iris_radii):
        disp = img.copy()
        if disp.ndim == 2:
            disp = cv2.cvtColor(disp, cv2.COLOR_GRAY2BGR)
        cv2.circle(disp, (int(cx), int(cy)), int(rp), pupil_color, thickness)
        cv2.circle(disp, (int(cx), int(cy)), int(ri), iris_color, thickness)
        ax.imshow(cv2.cvtColor(disp, cv2.COLOR_BGR2RGB))
        ax.axis('off')

    for ax in axes[n:]:
        ax.axis('off')

    plt.subplots_adjust(wspace=0.05, hspace=0.05, left=0.01, right=0.99, top=0.99, bottom=0.01)
    return fig


def plot_bitstring(bitstring, num_strips=8, num_coeffs=128):
    bits = np.fromiter((int(c) for c in bitstring), dtype=int, count=len(bitstring))
    bit_image = bits.reshape(num_strips, num_coeffs * 2).astype(np.uint8) * 255
    fig, ax = plt.subplots(figsize=(8, 2.5))
    fig.patch.set_alpha(0)
    ax.imshow(bit_image, cmap='gray', aspect='equal', interpolation='nearest')
    ax.set_xlabel('Bit index')
    ax.set_ylabel('Strip index')
    ax.set_title('Binary Iris Code')
    ax.set_xticks(np.arange(0, num_coeffs * 2, 16))
    ax.grid(False)
    plt.subplots_adjust(left=0.05, right=0.95, top=0.85, bottom=0.15)
    return fig

# ----------------------------------------------------------------------------------------------------------------------
# Application class
# ----------------------------------------------------------------------------------------------------------------------

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Iris Biometry Application")
        self.geometry("1280x720")

        # Dark theme via custom ttk style
        style = ttk.Style(self)
        style.theme_use('clam')
        bg = '#2e2e2e'
        fg = '#ffffff'
        style.configure('.', background=bg, foreground=fg)
        style.configure('TButton', background='#444444', foreground=fg, relief='raised', padding=5)
        style.map('TButton',
                  background=[('active', '#555555'), ('pressed', '#666666')],
                  relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
        self.configure(bg=bg)

        # Toolbar
        toolbar = ttk.Frame(self)
        toolbar.grid(row=0, column=0, sticky='ew')
        toolbar.columnconfigure((0, 1, 2), weight=1)

        # Buttons
        self.btn_load = ttk.Button(toolbar, text="Load Images", command=self.load_images, cursor='hand2')
        self.btn_find = ttk.Button(toolbar, text="Find Iris Code", command=self.find_iris_code, cursor='hand2')
        self.btn_params = ttk.Button(toolbar, text="Change Parameters", command=self.change_params, cursor='hand2')
        self.btn_load.grid(row=0, column=0, padx=5, pady=5)
        self.btn_find.grid(row=0, column=1, padx=5, pady=5)
        self.btn_params.grid(row=0, column=2, padx=5, pady=5)

        # Main panes
        main_frame = ttk.Frame(self)
        main_frame.grid(row=1, column=0, sticky='nsew')
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        for c in range(3):
            main_frame.columnconfigure(c, weight=1)

        self.panels = []
        for col in range(3):
            panel = ImagePanel(main_frame, bg, relief='groove', bd=2)
            panel.grid(row=0, column=col, sticky='nsew', padx=2, pady=2)
            self.panels.append(panel)

        self.images = []

        self.max_image_size_for_processing = 256
        self.white_ratio_threshold_for_pupils = 0.975
        self.closing_kernel_size_for_pupils = 10
        self.openening_kernel_size_for_pupils = 10
        self.crop_x_axis_for_pupils = 0.75
        self.crop_y_axis_for_pupils = 0.75
        self.crop_x_axis_for_irises = 1.0
        self.crop_y_axis_for_irises = 0.75
        self.white_ratio_threshold_for_irises = 0.75
        self.closing_kernel_size_for_irises = 20
        self.openening_kernel_size_for_irises = 10
        self.number_of_stripes_measure_iris_brightness = 16
        self.start_index_of_stripe_measure_iris_brightness = 2
        self.gabor_frequency = math.pi * 0.47

# Loading images -------------------------------------------------------------------------------------------------------

    def load_images(self):
        # Clear previously loaded images and plots
        self.images.clear()

        # Clear panels 1 and 2 (where plots are shown)
        for panel in self.panels[0:]:
            for widget in panel.inner.winfo_children():
                widget.destroy()

        # File dialog to select images
        filetypes = [("Image files", "*.png *.jpg *.bmp *.jpeg"), ("All files", "*")]
        paths = filedialog.askopenfilenames(title="Select images", filetypes=filetypes)
        if not paths:
            return

        pil_list = []
        for p in paths:
            try:
                with open(p, 'rb') as f:
                    data = f.read()
                arr = np.frombuffer(data, np.uint8)
                img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                if img is None:
                    messagebox.showwarning("Load Image", f"Could not decode image: {p}")
                    continue
            except Exception as e:
                messagebox.showwarning("Load Image", f"Error reading {p}: {e}")
                continue

            self.images.append(img)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pil = Image.fromarray(img_rgb)
            pil_list.append(pil)

        if pil_list:
            self.panels[0].display_images(pil_list)



# Changing parameters --------------------------------------------------------------------------------------------------

    def change_params(self):
        param_names = [
            'max_image_size_for_processing',
            'white_ratio_threshold_for_pupils',
            'closing_kernel_size_for_pupils',
            'openening_kernel_size_for_pupils',
            'crop_x_axis_for_pupils',
            'crop_y_axis_for_pupils',
            'crop_x_axis_for_irises',
            'crop_y_axis_for_irises',
            'white_ratio_threshold_for_irises',
            'closing_kernel_size_for_irises',
            'openening_kernel_size_for_irises',
            'number_of_stripes_measure_iris_brightness',
            'start_index_of_stripe_measure_iris_brightness',
            'gabor_frequency'
        ]

        dlg = tk.Toplevel(self)
        dlg.title("Change Parameters")

        style = ttk.Style(dlg)
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        fieldbackground="white")
        style.configure("Treeview.Heading",
                        background="lightgray",
                        foreground="black")

        tree = ttk.Treeview(dlg, columns=('Parameter', 'Value'), show='headings')
        tree.heading('Parameter', text='Parameter')
        tree.heading('Value', text='Value')
        tree.column('Parameter', width=250)
        tree.column('Value', width=150)

        entries = {}
        param_types = {}

        for name in param_names:
            value = getattr(self, name)
            param_types[name] = type(value)  # Store the type of the parameter
            tree.insert('', 'end', iid=name, values=(name, value))
        tree.grid(row=0, column=0, padx=10, pady=10)

        def edit_value(event):
            selected = tree.focus()
            if not selected:
                return
            column = tree.identify_column(event.x)
            if column != '#2':
                return

            x, y, width, height = tree.bbox(selected, '#2')
            entry = tk.Entry(dlg)
            entry.place(x=x + 10, y=y + 10, width=width)
            entry.insert(0, tree.set(selected, column))
            entry.focus()

            def save_edit(event):
                try:
                    # Retrieve the original type of the parameter
                    name = tree.focus()
                    original_type = param_types[name]

                    # Try to convert the value to the original type
                    val = entry.get()
                    if original_type == int:
                        val = int(val)
                    elif original_type == float:
                        val = float(val)
                    elif original_type == bool:
                        val = val.lower() in ('true', '1', 't', 'y', 'yes')
                    # Add more type conversions as needed (e.g., str, etc.)

                    tree.set(selected, column, val)
                    setattr(self, name, val)  # Update the parameter with the new value
                except ValueError:
                    pass  # Handle invalid inputs gracefully
                entry.destroy()

            entry.bind('<Return>', save_edit)
            entry.bind('<FocusOut>', lambda e: entry.destroy())

        tree.bind('<Double-1>', edit_value)

        def on_ok():
            for name in param_names:
                val = tree.set(name, 'Value')
                original_type = param_types[name]
                try:
                    # Convert the value to the original type before saving
                    if original_type == int:
                        val = int(val)
                    elif original_type == float:
                        val = float(val)
                    elif original_type == bool:
                        val = val.lower() in ('true', '1', 't', 'y', 'yes')
                    setattr(self, name, val)
                except ValueError:
                    pass  # Handle invalid inputs gracefully
            dlg.destroy()

        ttk.Button(dlg, text="OK", command=on_ok).grid(row=1, column=0, pady=10)

# Processing images ----------------------------------------------------------------------------------------------------

    def find_iris_code(self):

        ######################################################################
        # Fucntions ##########################################################
        ######################################################################

        # Resizing -----------------------------------------------------------

        def resize_images(images, max_size=256):
            resized = []
            for img in images:
                h, w = img.shape[:2]
                scale = max_size / max(h, w)
                new_size = (int(w * scale), int(h * scale))  # (width, height)
                resized_img = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)
                resized.append(resized_img)
            return resized

        # Correcting poor quality image --------------------------------------

        def remove_tophat_glints(gray):
            r = max(3, int(min(gray.shape) * 0.02) // 2 * 2 + 1)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (r, r))
            tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel)
            return cv2.subtract(gray, tophat)

        def inpaint_highlights(gray):
            _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            mask = cv2.dilate(mask, kernel, iterations=2)
            inpainted = cv2.inpaint(gray, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
            return inpainted

        def preprocess_remove_glares(gray):
            gray = remove_tophat_glints(gray)
            gray = cv2.GaussianBlur(gray, (7, 7), sigmaX=1.5)
            gray = inpaint_highlights(gray)
            return gray

        # Greyscale ----------------------------------------------------------

        def convert_images_to_greyscale(images):
            grey_images = []
            for img in images:
                if len(img.shape) == 3:
                    grey_img = np.mean(img, axis=2).astype(img.dtype)
                else:
                    grey_img = img.copy()
                grey_images.append(grey_img)
            return grey_images

        # Binarization -------------------------------------------------------

        def adaptive_binarize(
                grey_images,
                initial_factor,
                white_ratio_thresh=0.9,
                min_factor=1.0,
                factor_step=0.5,
                verbose=False
        ):
            binaries = []

            for idx, grey in enumerate(grey_images):
                X = initial_factor
                while True:

                    # ------------------------------------------
                    # Image sizes
                    h, w = grey.shape
                    # Treshold based on mean
                    P = np.sum(grey) / (h * w)
                    # Modified treshold
                    P = P / X
                    # Binarization
                    bin_image = np.zeros_like(grey, dtype=np.uint8)
                    bin_image[grey >= P] = 255
                    # ------------------------------------------

                    white_ratio = np.mean(bin_image == 255)
                    if white_ratio > white_ratio_thresh and (X - factor_step) >= min_factor:
                        new_X = round(X - factor_step, 2)
                        if verbose:
                            print(
                                f"Image {idx}: white ratio {white_ratio:.3f} > {white_ratio_thresh}, "
                                f"lowering factor {X:.2f} → {new_X:.2f} and retrying"
                            )
                        X = new_X
                        continue
                    break

                # Print final threshold if not verbose
                if not verbose:
                    print(
                        f"Image {idx}: final threshold P/X = {P / X:.2f} (factor X = {X:.2f}), "
                        f"white ratio = {white_ratio:.3f}"
                    )

                binaries.append(bin_image)

            return binaries

        # Morphologial operations --------------------------------------------

        def get_structuring_element(shape, ksize, anchor=None):
            rows, cols = ksize
            if anchor is None:
                anchor = (rows // 2, cols // 2)
            if shape.lower() == "rect":
                kernel = np.ones((rows, cols), dtype=np.uint8)
            elif shape.lower() == "ellipse":
                kernel = np.zeros((rows, cols), dtype=np.uint8)
                # Use the center of the kernel for ellipse definition.
                cy, cx = rows // 2, cols // 2
                a = rows / 2.0
                b = cols / 2.0
                for i in range(rows):
                    for j in range(cols):
                        # Equation of ellipse centered at (cy, cx)
                        if ((i - cy) / a) ** 2 + ((j - cx) / b) ** 2 <= 1:
                            kernel[i, j] = 1
            elif shape.lower() == "cross":
                kernel = np.zeros((rows, cols), dtype=np.uint8)
                # Place ones in the row and column corresponding to anchor
                ay, ax = anchor
                if 0 <= ay < rows:
                    kernel[ay, :] = 1
                if 0 <= ax < cols:
                    kernel[:, ax] = 1
            else:
                raise ValueError("Unsupported kernel shape. Choose 'rect', 'ellipse', or 'cross'.")
            return kernel, anchor

        def erosion(image, kernel, anchor):
            krows, kcols = kernel.shape
            ay, ax = anchor
            pad_top = ay
            pad_bottom = krows - ay - 1
            pad_left = ax
            pad_right = kcols - ax - 1
            padded = np.pad(image, ((pad_top, pad_bottom), (pad_left, pad_right)), mode='constant',
                            constant_values=image.min())
            out = np.zeros_like(image)
            rows, cols = image.shape
            for i in range(rows):
                for j in range(cols):
                    region = padded[i:i + krows, j:j + kcols]
                    out[i, j] = np.max(region[kernel == 1])
            return out

        def dilation(image, kernel, anchor):
            krows, kcols = kernel.shape
            ay, ax = anchor
            pad_top = ay
            pad_bottom = krows - ay - 1
            pad_left = ax
            pad_right = kcols - ax - 1
            padded = np.pad(image, ((pad_top, pad_bottom), (pad_left, pad_right)), mode='constant',
                            constant_values=image.max())
            out = np.zeros_like(image)
            rows, cols = image.shape
            for i in range(rows):
                for j in range(cols):
                    region = padded[i:i + krows, j:j + kcols]
                    out[i, j] = np.min(region[kernel == 1])
            return out

        def opening(image, kernel, anchor):
            eroded = erosion(image, kernel, anchor)
            opened = dilation(eroded, kernel, anchor)
            return opened

        def closing(image, kernel, anchor):
            dilated = dilation(image, kernel, anchor)
            closed = erosion(dilated, kernel, anchor)
            return closed

        # Remove artifacts away from center ----------------------------------

        def mask_outside_boundary(images, x_thresh=0.9, y_thresh=0.9):
            masked = []
            for img in images:
                h, w = img.shape[:2]
                cx, cy = w / 2.0, h / 2.0
                dx, dy = x_thresh * (w / 2.0), y_thresh * (h / 2.0)
                left, right = cx - dx, cx + dx
                top, bottom = cy - dy, cy + dy

                # Create a boolean mask of pixels to white‑out:
                ys, xs = np.ogrid[:h, :w]
                outside = (xs < left) | (xs > right) | (ys < top) | (ys > bottom)

                out = img.copy()
                if img.ndim == 2:
                    out[outside] = 255
                else:
                    out[outside] = (255, 255, 255)
                masked.append(out)
            return masked

        # Projections and find center ----------------------------------------

        def compute_projections(image):
            h, w = image.shape
            # horizontal & vertical
            h_proj = np.sum(image == 0, axis=1)
            v_proj = np.sum(image == 0, axis=0)

            # main diagonal offsets d = j - i
            d_off = np.arange(-h + 1, w)
            d_proj = np.array([
                sum(image[i, i + d] == 0
                    for i in range(max(0, -d), min(h, w - d)))
                for d in d_off
            ])

            # anti-diagonal offsets s = i + j
            ad_off = np.arange(0, h + w - 1)
            ad_proj = np.array([
                sum(image[i, s - i] == 0
                    for i in range(max(0, s - (w - 1)), min(h, s + 1)))
                for s in ad_off
            ])

            return h_proj, v_proj, d_proj, ad_proj, d_off, ad_off

        def get_pupil_centers_from_projections(pupil_projections):
            centers = []

            for (h_proj, v_proj, d_proj, ad_proj, d_off, ad_off) in pupil_projections:
                h = h_proj.shape[0]
                w = v_proj.shape[0]

                # 1) indices of max in each projection
                h_maxs = np.flatnonzero(h_proj == h_proj.max())  # y‑coords
                v_maxs = np.flatnonzero(v_proj == v_proj.max())  # x‑coords
                d_idxs = np.flatnonzero(d_proj == d_proj.max())
                ad_idxs = np.flatnonzero(ad_proj == ad_proj.max())
                d_maxs = d_off[d_idxs]  # j - i = d
                ad_maxs = ad_off[ad_idxs]  # i + j = s

                pts = []
                # H and V
                for y in h_maxs:
                    for x in v_maxs:
                        pts.append((x, y))

                # H and D:  j = i + d  → x = y + d
                for y in h_maxs:
                    for d in d_maxs:
                        pts.append((y + d, y))

                # H and A:  i + j = s → x = s - y
                for y in h_maxs:
                    for s in ad_maxs:
                        pts.append((s - y, y))

                # V and D:  x = x, y = x - d
                for x in v_maxs:
                    for d in d_maxs:
                        pts.append((x, x - d))

                # V and A:  x = x, y = s - x
                for x in v_maxs:
                    for s in ad_maxs:
                        pts.append((x, s - x))

                # D and A:  j = i + d  and  i + j = s
                # -> i = (s - d)/2,  j = i + d
                for d in d_maxs:
                    for s in ad_maxs:
                        i = (s - d) / 2.0
                        j = i + d
                        pts.append((j, i))

                # filter to valid image coords
                valid = [(x, y) for x, y in pts if 0 <= x < w and 0 <= y < h]
                if not valid:
                    centers.append((None, None))
                else:
                    xs, ys = zip(*valid)
                    centers.append((float(np.mean(xs)), float(np.mean(ys))))

            return centers

        # Find pupil radious -------------------------------------------------

        def find_radius_from_projection_edges(projections, centers):
            radii = []

            for (h_proj, v_proj, d_proj, ad_proj, d_off, ad_off), _ in zip(projections, centers):
                # Horizontal (rows) → y direction
                h_indices = np.where(h_proj > 0)[0]
                h_radius = (h_indices[-1] - h_indices[0] + 1) / 2.0 if len(h_indices) > 0 else 0

                # Vertical (columns) → x direction
                v_indices = np.where(v_proj > 0)[0]
                v_radius = (v_indices[-1] - v_indices[0] + 1) / 2.0 if len(v_indices) > 0 else 0

                # Diagonal
                d_indices = np.where(d_proj > 0)[0]
                d_radius = (d_indices[-1] - d_indices[0] + 1) / 2.0 / math.sqrt(2) if len(d_indices) > 0 else 0

                # Anti-diagonal
                ad_indices = np.where(ad_proj > 0)[0]
                ad_radius = (ad_indices[-1] - ad_indices[0] + 1) / 2.0 / math.sqrt(2) if len(ad_indices) > 0 else 0

                radius = np.mean([v_radius, h_radius, d_radius, ad_radius])
                radii.append(radius)

            return radii

        # Find iris radious --------------------------------------------------

        def find_iris_boundaries(
                grey_images, centers, radii, iris_masks,
                num_strips=10, max_frac=2.0, start_index=1
        ):
            iris_radii = []

            for img, (cx_f, cy_f), rp, mask in zip(grey_images, centers, radii, iris_masks):
                cx, cy = cx_f, cy_f
                # build ring edges
                edges = np.linspace(rp, rp * max_frac, num_strips + 1)
                h, w = img.shape
                Y, X = np.ogrid[:h, :w]
                D = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)

                # compute mean brightness per ring
                means = []
                for k in range(1, num_strips + 1):
                    inner, outer = edges[k - 1], edges[k]
                    ring_mask = (D >= inner) & (D < outer) & (mask == 0)
                    vals = img[ring_mask]
                    means.append(vals.mean() if vals.size else 0)

                # derivative between adjacent means
                deriv = np.diff(means)
                if deriv.size == 0:
                    iris_radii.append(None)
                    continue

                # pick the largest jump
                idx = int(np.argmax(deriv[start_index:]) + 1)
                # boundary is at edges[idx+1]
                iris_radii.append(float(edges[idx + 1]))

            return iris_radii

        # Transfer centers to different size ---------------------------------

        def map_center_to_different_image(center, target_shape, source_shape):
            src_h, src_w = source_shape
            tgt_h, tgt_w = target_shape

            x, y = center

            # Compute scaling factors regardless of direction
            scale_x = tgt_w / src_w
            scale_y = tgt_h / src_h

            # Scale and round to integer pixel location
            x_new = int(round(x * scale_x))
            y_new = int(round(y * scale_y))

            return (x_new, y_new)

        def map_radius_to_different_image(radius, new_shape, base_shape):
            base_h, base_w = base_shape
            new_h, new_w = new_shape

            # Scale based on average scaling factor from both dimensions
            scale_h = new_h / base_h
            scale_w = new_w / base_w
            scale = (scale_h + scale_w) / 2.0

            return radius * scale

        # Get iris code ------------------------------------------------------

        def get_raw_strips(
                images,
                binarized_iris_images,
                centers,
                pupil_radii,
                iris_radii,
                num_stripes=8,
                angular_res=360
        ):

            all_strips = []
            for img, mask, (cx, cy), rp, ri in zip(
                    images, binarized_iris_images, centers, pupil_radii, iris_radii
            ):

                h, w = img.shape[:2]
                Y, X = np.ogrid[:h, :w]
                D = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
                A = (np.degrees(np.arctan2(Y - cy, X - cx)) + 360) % 360
                A = (A - 270) % 360
                edges = np.linspace(rp, ri, num_stripes + 1)

                strips = []
                polar_size = (angular_res, int(ri))  # (width, max radius)
                origin = (int(cx), int(cy))
                maxR = float(ri)
                for i in range(num_stripes):
                    inner, outer = edges[i], edges[i + 1]
                    radial_mask = (D >= inner) & (D < outer) & (mask == 0)

                    # define angular mask per stripe
                    if i < 4:
                        ang_mask = ((A >= 15) & (A <= 360 - 15))
                    elif i < 6:
                        ang_mask = (A >= 90 - 56.5) & (A <= 90 + 56.5) | (A >= 270 - 56.5) & (A <= 270 + 56.5)
                    else:
                        ang_mask = (A >= 90 - 45) & (A <= 90 + 45) | (A >= 270 - 45) & (A <= 270 + 45)
                    strip_mask = radial_mask & ang_mask

                    # --- manual unwarp to rectangular strip ---
                    radial_steps = int(np.ceil(outer - inner))
                    angles = np.linspace(0, 2 * np.pi, angular_res, endpoint=False)
                    angles = (angles + 3 * np.pi / 2) % (2 * np.pi)
                    radii = inner + np.linspace(0, outer - inner, radial_steps, endpoint=False)

                    R, Theta = np.meshgrid(radii, angles, indexing='ij')
                    Xs = np.clip((cx + R * np.cos(Theta)).astype(int), 0, w - 1)
                    Ys = np.clip((cy + R * np.sin(Theta)).astype(int), 0, h - 1)

                    strip_vals = img[Ys, Xs]
                    mask_vals = strip_mask[Ys, Xs]

                    strip_vals[~mask_vals] = 0

                    valid_cols = mask_vals.any(axis=0)
                    strip_rect = strip_vals[:, valid_cols]

                    strips.append(strip_rect)

                all_strips.append(strips)

            return all_strips

        def collapse_strips(raw_strips, sigma=None):
            collapsed = []
            for strip in raw_strips:
                H, W = strip.shape[:2]
                C = strip.shape[2] if strip.ndim == 3 else 1

                # 1) Konwersja do szarości
                gray = strip[..., 0]

                # 2) budujemy okno Gaussa dla wysokości H
                if sigma is None:
                    sigma = H / 6.0
                coords = np.arange(H)
                center = (H - 1) / 2.0
                gauss = np.exp(-0.5 * ((coords - center) / sigma) ** 2)
                gauss /= gauss.sum()  # znormalizuj tak, żeby suma wag = 1

                # 3) ważone uśrednienie każdej kolumny
                #    wynik to wektor [0..W-1]
                col_avg = gauss @ gray  # shape: (W,)
                collapsed.append(col_avg)

            return collapsed

        def gabor_decompose(strips, f, num_coeffs=128):
            """
            strips       : list of 1D numpy arrays, waried length
            f            : frequency of wave (in pixel cycles)
            num_coeffs   : number of coefficients

            Schema:
              - sigma = 0.5 * pi * f
              - center of waves: x_k = k * (1/f)
              - for every wave g_k(n) = exp( - (n−x_k)^2 / (2 sigma^2) ) * exp( 1j·2pif·(n−x_k) )
              - coefficients: c_k = sum_n strip[n] · g_k(n)
            """
            sigma = 0.5 * np.pi * f
            coeffs = np.zeros((len(strips), num_coeffs), dtype=np.complex128)

            for i, strip in enumerate(strips):
                W = strip.shape[0]
                n = np.arange(W)
                step = 1.0 / f
                x_k = np.arange(num_coeffs) * step

                delta = n[None, :] - x_k[:, None]
                gauss = np.exp(-0.5 * (delta / sigma) ** 2)
                osc = np.exp(1j * 2 * np.pi * f * delta)

                G = gauss * osc
                coeffs[i, :] = G.dot(strip)

            return coeffs

        def encode_phases(coeffs):
            """
            coeffs : numpy array of complex numbers, shape (num_strips, num_coeffs)

            Returns a tuple:
              - codes     : numpy array of dtype 'U1', shape (num_strips, num_coeffs, 2)
                            each entry is ['b0', 'b1'] corresponding to the phase quadrant
              - bitstring : str of length num_strips * num_coeffs * 2,
                            bits in order: strip0_coeff0_b0, strip0_coeff0_b1, strip0_coeff1_b0, strip0_coeff1_b1, ...

            Phase encoding:
              Quadrant I   (Re ≥ 0, Im ≥ 0) -> "00"
              Quadrant II  (Re <  0, Im ≥ 0) -> "01"
              Quadrant III (Re <  0, Im <  0) -> "11"
              Quadrant IV  (Re ≥ 0, Im <  0) -> "10"
            """
            re = coeffs.real
            im = coeffs.imag
            num_strips, num_coeffs = coeffs.shape

            codes = np.empty((num_strips, num_coeffs, 2), dtype='U1')

            # I Quadrant
            mask = (re >= 0) & (im >= 0)
            codes[mask, 0] = '0'
            codes[mask, 1] = '0'

            # II Quadrant
            mask = (re < 0) & (im >= 0)
            codes[mask, 0] = '0'
            codes[mask, 1] = '1'

            # III Quadrant
            mask = (re < 0) & (im < 0)
            codes[mask, 0] = '1'
            codes[mask, 1] = '1'

            # IV Quadrant
            mask = (re >= 0) & (im < 0)
            codes[mask, 0] = '1'
            codes[mask, 1] = '0'

            flat = codes.reshape(-1, 2)
            bitstring = ''.join(flat.flatten())

            return codes, bitstring

        def hamming_distance(bitstring1, bitstring2):
            return sum(b1 != b2 for b1, b2 in zip(bitstring1, bitstring2))

        ######################################################################
        # Pipeline ##########################################################
        ######################################################################

        # Parameters
        max_image_size_for_processing = 256
        white_ratio_threshold_for_pupils = 0.975
        closing_kernel_size_for_pupils = 10
        openening_kernel_size_for_pupils = 10
        crop_x_axis_for_pupils = 0.75
        crop_y_axis_for_pupils = 0.75
        crop_x_axis_for_irises = 1.0
        crop_y_axis_for_irises = 0.75
        white_ratio_threshold_for_irises = 0.75
        closing_kernel_size_for_irises = 20
        openening_kernel_size_for_irises = 10
        number_of_stripes_measure_iris_brightness = 16
        start_index_of_stripe_measure_iris_brightness = 2
        gabor_frequency = math.pi * 0.47

        # Loading
        images = self.images
        print(f"Loaded {len(images)} images.")

        # Resizing
        if images[0].shape[1] > self.max_image_size_for_processing:
            resized_images = resize_images(images, max_size=self.max_image_size_for_processing)
            print("Images resized.")
        else:
            resized_images = images.copy()
            print("Image resizing not needed.")

        # Greyscale
        grey_images = convert_images_to_greyscale(resized_images)
        print("Converted images to greyscale.")

        # Remove glares
        processed_grey_images = [preprocess_remove_glares(img) for img in grey_images]
        print("Removed glares from images.")

        # For pupil ------------------------------------------------
        print("Starting pupil detection...")

        # Binarization
        binarized_pupil_images = adaptive_binarize(
            processed_grey_images,
            initial_factor=15,
            white_ratio_thresh=self.white_ratio_threshold_for_pupils,
            min_factor=1.0,
            factor_step=0.05,
            verbose=False
        )
        print("Binarized pupil images.")

        # Closing
        kernel_size = math.floor(np.mean(binarized_pupil_images[0].shape) * (self.closing_kernel_size_for_pupils / 100))
        structuring_element, anchor = get_structuring_element(shape="ellipse", ksize=(kernel_size, kernel_size),
                                                              anchor=None)
        closed_pupil_images = [closing(img, structuring_element, anchor) for img in binarized_pupil_images]
        print("Applied morphological closing to pupil images.")

        # Opening
        kernel_size = math.floor(np.mean(binarized_pupil_images[0].shape) * (self.openening_kernel_size_for_pupils / 100))
        structuring_element, anchor = get_structuring_element(shape="ellipse", ksize=(kernel_size, kernel_size),
                                                              anchor=None)
        opened_pupil_images = [opening(img, structuring_element, anchor) for img in closed_pupil_images]
        print("Applied morphological opening to pupil images.")

        # Removing artifacts near border
        cleaned_pupil_images = mask_outside_boundary(opened_pupil_images, x_thresh=self.crop_x_axis_for_pupils,
                                                     y_thresh=self.crop_y_axis_for_pupils)
        print("Computed pupil centers and radii.")

        # Calculating projections, finding pupil centers and radii for pupil
        pupil_projections = [compute_projections(img) for img in cleaned_pupil_images]
        pupil_centers = get_pupil_centers_from_projections(pupil_projections)
        pupil_radii = find_radius_from_projection_edges(pupil_projections, pupil_centers)

        # For iris -------------------------------------------------
        print("Starting iris detection...")

        # Removing artifacts near border
        cleaned_iris_images = mask_outside_boundary(processed_grey_images, x_thresh=self.crop_x_axis_for_irises,
                                                    y_thresh=self.crop_y_axis_for_irises)
        print("Masked iris boundary areas.")

        # Binarization
        binarized_iris_images = adaptive_binarize(
            cleaned_iris_images,
            initial_factor=15,
            white_ratio_thresh=self.white_ratio_threshold_for_irises,
            min_factor=1.0,
            factor_step=0.05,
            verbose=False
        )
        print("Binarized iris images.")

        # Closing
        kernel_size = math.floor(np.mean(binarized_iris_images[0].shape) * (self.closing_kernel_size_for_irises / 100))
        structuring_element, anchor = get_structuring_element(shape="ellipse", ksize=(kernel_size, kernel_size),
                                                              anchor=None)
        closed_iris_images = [closing(img, structuring_element, anchor) for img in binarized_iris_images]
        print("Applied morphological closing to iris images.")

        # Opening
        kernel_size = math.floor(np.mean(closed_iris_images[0].shape) * (self.openening_kernel_size_for_irises / 100))
        structuring_element, anchor = get_structuring_element(shape="ellipse", ksize=(kernel_size, kernel_size),
                                                              anchor=None)
        opened_iris_images = [opening(img, structuring_element, anchor) for img in closed_iris_images]
        print("Applied morphological opening to iris images.")

        # Finding iris radious
        iris_radii = find_iris_boundaries(
            grey_images,
            pupil_centers,
            pupil_radii,
            opened_iris_images,
            num_strips=self.number_of_stripes_measure_iris_brightness,
            max_frac=3.5,
            start_index=self.start_index_of_stripe_measure_iris_brightness
        )
        print("Computed iris radii.")

        # Rebase elements-------------------------------------------
        print("Rebasing centers and radii to original image dimensions...")

        new_pupil_radii = [
            map_radius_to_different_image(radius, img_to_transfer_to.shape[:2], base_img.shape[:2])
            for radius, img_to_transfer_to, base_img
            in zip(pupil_radii, images, cleaned_pupil_images)]
        new_pupil_centers = [
            map_center_to_different_image(center, img_to_transfer_to.shape[:2], base_img.shape[:2])
            for center, img_to_transfer_to, base_img
            in zip(pupil_centers, images, cleaned_pupil_images)]
        new_iris_radii = [
            map_radius_to_different_image(radius, img_to_transfer_to.shape[:2], base_img.shape[:2])
            for radius, img_to_transfer_to, base_img
            in zip(iris_radii, images, opened_iris_images)]
        print("Done rebasing.")

        # Iris code ------------------------------------------------
        print("Generating iris codes...")

        # Create mask (default no mask)
        masks = [np.zeros_like(img[..., 0]) for img in images]

        # Get raw stripes
        raw_strips = get_raw_strips(
            images,
            masks,
            new_pupil_centers,
            new_pupil_radii,
            new_iris_radii,
            num_stripes=8,
            angular_res=360
        )

        # Collapse stripes into 1D
        one_dimensional_strips = [collapse_strips(raw_strip) for raw_strip in raw_strips]

        # Get Gabor coefficients
        gabor_coefficients = [gabor_decompose(one_dimensional_strip, f=self.gabor_frequency) for one_dimensional_strip in
                              one_dimensional_strips]

        # Obtain iris code
        iris_codes, bitstrings = zip(*[encode_phases(gabor_coefficient) for gabor_coefficient in gabor_coefficients])
        print("Iris codes and bitstrings generated.")

        # Showcase -------------------------------------------------
        print("Displaying results...")
        # 2nd panel: show each bitstring side‑by‑side (or just the first one)
        figs = [draw_pupil_and_iris_boundaries([image], [new_pupil_center],
                                               [new_pupil_radius], [new_iris_radius],
                                               thickness=max(2, int(images[0].shape[0]/200)))
                for image, new_pupil_center, new_pupil_radius, new_iris_radius
                in zip(images, new_pupil_centers, new_pupil_radii, new_iris_radii)]
        # clear & display them all in panel 2:
        for w in self.panels[1].inner.winfo_children():
            w.destroy()
        for fig in figs:
            canvas = FigureCanvasTkAgg(fig, master=self.panels[1].inner)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True, pady=5)
        print('Pupil and iris boundary plots drawn.')

        # 3rd panel: show each bitstring side‑by‑side (or just the first one)
        figs = [plot_bitstring(bs) for bs in bitstrings]
        # clear & display them all in panel 3:
        for w in self.panels[2].inner.winfo_children():
            w.destroy()
        for fig in figs:
            # canvas = FigureCanvasTkAgg(fig, master=self.panels[2].inner)
            canvas = FigureCanvasTkAgg(fig, master=self.panels[2].inner)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True, pady=5)
        print('Iris code drawn.')


# ----------------------------------------------------------------------------------------------------------------------
# ImagePanel class
# ----------------------------------------------------------------------------------------------------------------------

class ImagePanel(tk.Frame):
    def __init__(self, parent, bg, **kwargs):
        super().__init__(parent, bg=bg, **kwargs)
        self.bg = bg

        # Canvas + scrollbar
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0)
        self.vscroll = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vscroll.set)

        self.vscroll.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both', expand=True)

        # Inner frame inside canvas
        self.inner = tk.Frame(self.canvas, bg=bg)
        self.inner_id = self.canvas.create_window((0, 0), window=self.inner, anchor='nw')

        # Update scroll region when inner frame changes
        self.inner.bind('<Configure>', lambda e:
            self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        )

        # Resize images when canvas size changes
        self.canvas.bind('<Configure>', lambda e: (
            self.canvas.itemconfigure(self.inner_id, width=e.width),
            self._resize_all()
        ))

        # Bind mouse wheel to the canvas only
        self.canvas.bind('<Enter>', lambda e: self.canvas.focus_set())
        self.canvas.bind('<MouseWheel>', self._on_mousewheel)
        self.canvas.bind('<Button-4>', self._on_mousewheel)
        self.canvas.bind('<Button-5>', self._on_mousewheel)

        self._labels = []
        self._pil_images = []

    def _on_mousewheel(self, event):
        if hasattr(event, 'delta'):
            # Windows / macOS
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')
        else:
            # Linux scroll
            if event.num == 4:
                self.canvas.yview_scroll(-1, 'units')
            elif event.num == 5:
                self.canvas.yview_scroll(1, 'units')

    def display_images(self, pil_images):
        # Clear existing
        for widget in self.inner.winfo_children():
            widget.destroy()
        self._pil_images = pil_images.copy()
        self._labels.clear()
        # Create labels
        for img in self._pil_images:
            lbl = tk.Label(self.inner, bg=self.bg, bd=1, relief='solid')
            lbl.pack(fill='x', padx=5, pady=5)
            self._labels.append(lbl)
        self._resize_all()

    def _resize_all(self):
        # Available width minus padding
        width = self.canvas.winfo_width() - 10
        if width <= 0:
            return
        for pil, lbl in zip(self._pil_images, self._labels):
            w, h = pil.size
            new_h = int(h * (width / w))
            resized = pil.resize((width, new_h), Image.Resampling.LANCZOS)
            tk_img = ImageTk.PhotoImage(resized)
            lbl.configure(image=tk_img)
            lbl.image = tk_img

    def display_figure(self, fig):
        # clear any previous content
        for w in self.inner.winfo_children():
            w.destroy()
        # embed new figure
        canvas = FigureCanvasTkAgg(fig, master=self.inner)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill='both', expand=True)


if __name__ == '__main__':
    app = Application()
    app.mainloop()
