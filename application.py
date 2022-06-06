import tkinter as tk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("圖片壓縮")
        self.resizable(False, False)