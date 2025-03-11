import tkinter as tk

# Strona
class ReadSavePicture(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        # Górny pasek strony
        top_bar = tk.Frame(self)
        top_bar.pack(side=tk.TOP, fill=tk.X)

        # Obszar podstrony
        self.content_area = tk.Frame(self)
        self.content_area.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Zawartość podstrony
        self.pages = {
            "readsave": {
                "label": "Wczytaj/zapisz obraz",
                "frame": tk.Frame(self.content_area, bg="pink"),
                "content": {"text": "Zapisz wczyt", "bg": "lightblue"}
            }
        }

        # Przyciski podstron na górnym pasku strony
        for key, page in self.pages.items():
            btn = tk.Button(top_bar, text=page["label"], command=lambda k=key: self.show_page(k))
            btn.pack(side=tk.LEFT, padx=2, pady=2)

        # Domyślna podstrona
        self.show_page("readsave")

    def show_page(self, page_key):
        for key, data in self.pages.items():
            frame = data["frame"]
            if key == page_key:
                frame.pack(fill=tk.BOTH, expand=True)
                for widget in frame.winfo_children():
                    widget.destroy()
                tk.Label(frame, **data["content"]).pack(padx=10, pady=10)
            else:
                # Ukryj pozostałe elementy
                frame.pack_forget()