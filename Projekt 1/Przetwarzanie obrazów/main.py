import tkinter as tk


# Podstrona X z dwoma przyciskami: Xa i Xb.
class SubpageX(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # Górny pasek podstrony X
        top_bar = tk.Frame(self)
        top_bar.pack(side=tk.TOP, fill=tk.X)
        btn_greyscale = tk.Button(top_bar, text="Szarość", command=self.show_greyscale)
        btn_greyscale.pack(side=tk.LEFT, padx=2, pady=2)
        btn_xb = tk.Button(top_bar, text="Jasność", command=self.show_xb)
        btn_xb.pack(side=tk.LEFT, padx=2, pady=2)
        btn_contrast = tk.Button(top_bar, text="Kontrast", command=self.show_contrast)
        btn_contrast.pack(side=tk.LEFT, padx=2, pady=2)

        # Obszar, w którym zmienia się zawartość zależnie od przycisku
        self.content_area = tk.Frame(self)
        self.content_area.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Ramki dla poszczególnych zawartości
        self.frame_greyscale = tk.Frame(self.content_area, bg="lightblue")
        self.frame_xb = tk.Frame(self.content_area, bg="lightgreen")
        self.frame_contrast = tk.Frame(self.content_area, bg="lightgreen")

        self.show_greyscale()  # domyślnie pokazujemy zawartość Xa

    def show_greyscale(self):
        self.frame_xb.pack_forget()
        self.frame_greyscale.pack(fill=tk.BOTH, expand=True)
        # Wyczyść ramkę i dodaj przykładową zawartość
        for widget in self.frame_greyscale.winfo_children():
            widget.destroy()
        tk.Label(self.frame_greyscale, text="Zawartość greyscale", bg="lightblue").pack(padx=10, pady=10)

    def show_xb(self):
        self.frame_greyscale.pack_forget()
        self.frame_xb.pack(fill=tk.BOTH, expand=True)
        # Wyczyść ramkę i dodaj przykładową zawartość
        for widget in self.frame_xb.winfo_children():
            widget.destroy()
        tk.Label(self.frame_xb, text="Zawartość Xb", bg="lightgreen").pack(padx=10, pady=10)


# Podstrona Y z trzema przyciskami: Ya, Yb i Yc.
class SubpageY(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # Górny pasek podstrony Y
        top_bar = tk.Frame(self)
        top_bar.pack(side=tk.TOP, fill=tk.X)
        btn_ya = tk.Button(top_bar, text="Ya", command=self.show_ya)
        btn_ya.pack(side=tk.LEFT, padx=2, pady=2)
        btn_yb = tk.Button(top_bar, text="Yb", command=self.show_yb)
        btn_yb.pack(side=tk.LEFT, padx=2, pady=2)
        btn_yc = tk.Button(top_bar, text="Yc", command=self.show_yc)
        btn_yc.pack(side=tk.LEFT, padx=2, pady=2)

        # Obszar zmiennej zawartości pod paskiem
        self.content_area = tk.Frame(self)
        self.content_area.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Ramki dla poszczególnych zawartości
        self.frame_ya = tk.Frame(self.content_area, bg="lightyellow")
        self.frame_yb = tk.Frame(self.content_area, bg="lightcoral")
        self.frame_yc = tk.Frame(self.content_area, bg="lightgrey")

        self.show_ya()  # domyślnie pokazujemy zawartość Ya

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


# Główna aplikacja
class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikacja Okienkowa")
        self.geometry("600x500")

        # Pasek górny z przyciskami do wyboru podstrony
        main_top_bar = tk.Frame(self, bd=2, relief=tk.RAISED)
        main_top_bar.pack(side=tk.TOP, fill=tk.X)
        btn_page_x = tk.Button(main_top_bar, text="Operacje na pikselach", command=self.show_page_x)
        btn_page_x.pack(side=tk.LEFT, padx=5, pady=5)
        btn_page_y = tk.Button(main_top_bar, text="Wczytaj / Zapisz", command=self.show_page_y)
        btn_page_y.pack(side=tk.LEFT, padx=5, pady=5)

        # Środkowy obszar z dwoma panelami (na przyszłe obrazy)
        central_area = tk.Frame(self, bd=2, relief=tk.SUNKEN)
        central_area.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.left_panel = tk.Label(central_area, text="Lewy Panel", bd=1, relief=tk.GROOVE)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.right_panel = tk.Label(central_area, text="Prawy Panel", bd=1, relief=tk.GROOVE)
        self.right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Obszar podstrony (zmieniana w zależności od wyboru)
        self.subpage_area = tk.Frame(self, bd=2, relief=tk.SUNKEN)
        self.subpage_area.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Inicjalizacja podstron
        self.page_x = SubpageX(self.subpage_area)
        self.page_y = SubpageY(self.subpage_area)

        # Domyślnie pokazujemy podstronę X
        self.page_x.pack(fill=tk.BOTH, expand=True)

    def show_page_x(self):
        self.page_y.pack_forget()
        self.page_x.pack(fill=tk.BOTH, expand=True)

    def show_page_y(self):
        self.page_x.pack_forget()
        self.page_y.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
