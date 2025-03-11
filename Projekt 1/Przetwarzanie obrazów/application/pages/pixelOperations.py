import tkinter as tk

# Strona
class PixelOperations(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        # Górny pasek strony z przyciskami podstron --------------------------------------------------------------------

        # Górny pasek strony
        top_bar = tk.Frame(self)
        top_bar.pack(side=tk.TOP, fill=tk.X)

        # Przycisk podstron na górnym pasku strony
        pages_config = [
            ("greyscale", "Konwersja do odcieni szarości"),
            ("brightness", "Korekta jasności"),
            ("contrast", "Korekta kontrastu"),
            ("negative", "Negatyw"),
            ("binarization", "Binaryzacja")
        ]
        for key, btn_text in pages_config:
            btn = tk.Button(top_bar, text=btn_text, command=lambda k=key: self.show_page(k))
            btn.pack(side=tk.LEFT, padx=2, pady=2)

        # Zawartośći podstron ------------------------------------------------------------------------------------------

        # Obszar podstrony
        self.content_area = tk.Frame(self)
        self.content_area.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Zawartość podstrony
        self.pages = {
            "greyscale": {
                "frame": tk.Frame(self.content_area, bg="lightblue"),
                "content": {"text": "Coś z szarością", "bg": "lightblue"}
            },
            "brightness": {
                "frame": tk.Frame(self.content_area, bg="lightgreen"),
                "content": {"text": "Tutaj będzie coś z jasnością", "bg": "lightgreen"}
            },
            "contrast": {
                "frame": tk.Frame(self.content_area, bg="lightblue"),
                "content": {"text": "Kontrast", "bg": "lightgreen"}
            },
            "negative": {
                "frame": tk.Frame(self.content_area, bg="lightgreen"),
                "content": {"text": "Negatyw", "bg": "lightgreen"}
            },
            "binarization": {
                "frame": tk.Frame(self.content_area, bg="lightblue"),
                "content": {"text": "Binaryzacja", "bg": "lightgreen"}
            }
        }

        # Domyślna podstrona
        self.show_page("greyscale")

    def show_page(self, page_key):
        """Wyświetla stronę odpowiadającą page_key i ukrywa pozostałe."""
        for key, data in self.pages.items():
            frame = data["frame"]
            if key == page_key:
                frame.pack(fill=tk.BOTH, expand=True)
                for widget in frame.winfo_children():
                    widget.destroy()
                tk.Label(frame, **data["content"]).pack(padx=10, pady=10)
            else:
                frame.pack_forget()