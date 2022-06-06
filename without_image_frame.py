import tkinter as tk
from tkinter import filedialog
import os

class WithOutImageFrame(tk.Frame):
    def __init__(self, master, onSelectImages, imageZoneWidth):
        tk.Frame.__init__(self, master)
        self.config(bg='white')
        self.imageZoneWidth = imageZoneWidth
        self.place(width=self.imageZoneWidth, height=self.imageZoneWidth/2)
        self.images = []
        self.createWidget(onSelectImages)
    def createWidget(self, onSelectImages):
        self.selectFileButton = tk.Button(self, text='選擇圖片', command=lambda: self.selectImages(onSelectImages))
        self.selectFileButton.place(relx=0.5, rely=0.5, anchor='center')
    def selectImages(self, onSelectImages):
        dirSelected = filedialog.askdirectory()
        if dirSelected != '':
            selectedImages = []
            for dirPaths, dirNames, fileNames in os.walk(dirSelected):
                for f in fileNames:
                    if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                        selectedImages.append(os.path.join(dirPaths, f))
            if len(selectedImages) > 0:
                onSelectImages(selectedImages)
                
    
    