import tkinter as tk
from application.pages.pixelOperations import PixelOperations
from application.pages.graphicalFiltering import GraphicalFiltering
from application.pages.readSavePicture import ReadSavePicture

# Aplikacja
class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Przetwarzanie obrazów")
        self.geometry("600x500")

        # Górny pasek aplikacji z przyciskami stron --------------------------------------------------------------------

        # Górny pasek aplikacji
        main_top_bar = tk.Frame(self, bd=2, relief=tk.RAISED)
        main_top_bar.pack(side=tk.TOP, fill=tk.X)

        # Przyciski stron na górnym pasku aplikacji
        btn_page_ReadSavePicture = tk.Button(main_top_bar, text="Wczytaj / Zapisz", command=self.show_page_ReadSavePicture)
        btn_page_ReadSavePicture.pack(side=tk.LEFT, padx=5, pady=5)
        btn_page_PixelOperations = tk.Button(main_top_bar, text="Operacje na pikselach", command=self.show_page_PixelOperations)
        btn_page_PixelOperations.pack(side=tk.LEFT, padx=5, pady=5)
        btn_page_GraphicalFiltering = tk.Button(main_top_bar, text="Filtry Graficzne", command=self.show_page_GraphicalFiltering)
        btn_page_GraphicalFiltering.pack(side=tk.LEFT, padx=5, pady=5)

        # Środkowy obszar z dwoma panelami na obrazy -------------------------------------------------------------------

        # Środkowy obszar
        central_area = tk.Frame(self, bd=2, relief=tk.SUNKEN)
        central_area.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Panel lewy
        self.left_panel = tk.Label(central_area, text="Lewy Panel", bd=1, relief=tk.GROOVE)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        # Panel prawy
        self.right_panel = tk.Label(central_area, text="Prawy Panel", bd=1, relief=tk.GROOVE)
        self.right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Zawartośći stron ---------------------------------------------------------------------------------------------

        # Obszar strony
        self.subpage_area = tk.Frame(self, bd=2, relief=tk.SUNKEN)
        self.subpage_area.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Inicjalizacja stron
        self.page_ReadSavePicture = ReadSavePicture(self.subpage_area)
        self.page_PixelOperations = PixelOperations(self.subpage_area)
        self.page_GraphicalFiltering = GraphicalFiltering(self.subpage_area)

        # Domyślna strona
        self.page_ReadSavePicture.pack(fill=tk.BOTH, expand=True)

    def show_page_ReadSavePicture(self):
        self.page_PixelOperations.pack_forget()
        self.page_GraphicalFiltering.pack_forget()
        self.page_ReadSavePicture.pack(fill=tk.BOTH, expand=True)

    def show_page_PixelOperations(self):
        self.page_ReadSavePicture.pack_forget()
        self.page_GraphicalFiltering.pack_forget()
        self.page_PixelOperations.pack(fill=tk.BOTH, expand=True)

    def show_page_GraphicalFiltering(self):
        self.page_ReadSavePicture.pack_forget()
        self.page_PixelOperations.pack_forget()
        self.page_GraphicalFiltering.pack(fill=tk.BOTH, expand=True)