import tkinter as tk

# Strona
class GraphicalFiltering(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        # Górny pasek strony z przyciskami podstron --------------------------------------------------------------------

        # Górny pasek strony
        top_bar = tk.Frame(self)
        top_bar.pack(side=tk.TOP, fill=tk.X)

        # Przycisk podstron na górnym pasku strony
        btn_ya = tk.Button(top_bar, text="Ya", command=self.show_ya)
        btn_ya.pack(side=tk.LEFT, padx=2, pady=2)
        btn_yb = tk.Button(top_bar, text="Yb", command=self.show_yb)
        btn_yb.pack(side=tk.LEFT, padx=2, pady=2)
        btn_yc = tk.Button(top_bar, text="Yc", command=self.show_yc)
        btn_yc.pack(side=tk.LEFT, padx=2, pady=2)

        # Zawartośći podstron ------------------------------------------------------------------------------------------

        # Obszar podstrony
        self.content_area = tk.Frame(self)
        self.content_area.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Zawartość podstrony
        self.frame_ya = tk.Frame(self.content_area, bg="lightyellow")
        self.frame_yb = tk.Frame(self.content_area, bg="lightcoral")
        self.frame_yc = tk.Frame(self.content_area, bg="lightgrey")

        # Domyślna podstrona
        self.show_ya()

    def show_ya(self):
        self.frame_yb.pack_forget()
        self.frame_yc.pack_forget()
        self.frame_ya.pack(fill=tk.BOTH, expand=True)
        for widget in self.frame_ya.winfo_children():
            widget.destroy()
        tk.Label(self.frame_ya, text="Zawartość Ya", bg="lightyellow").pack(padx=10, pady=10)

    def show_yb(self):
        self.frame_ya.pack_forget()
        self.frame_yc.pack_forget()
        self.frame_yb.pack(fill=tk.BOTH, expand=True)
        for widget in self.frame_yb.winfo_children():
            widget.destroy()
        tk.Label(self.frame_yb, text="Zawartość Yb", bg="lightcoral").pack(padx=10, pady=10)

    def show_yc(self):
        self.frame_ya.pack_forget()
        self.frame_yb.pack_forget()
        self.frame_yc.pack(fill=tk.BOTH, expand=True)
        for widget in self.frame_yc.winfo_children():
            widget.destroy()
        tk.Label(self.frame_yc, text="Zawartość Yc", bg="lightgrey").pack(padx=10, pady=10)