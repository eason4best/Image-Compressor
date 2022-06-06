import tkinter as tk
from tkinter import Label, ttk
from with_image_frame import WithImageFrame
from without_image_frame import WithOutImageFrame
import threading


class MainFrame(tk.Frame):
    def __init__(self, master, imageZoneWidth):
        tk.Frame.__init__(self, master)
        self.images = []
        self.initialQuality = 80
        self.imageZoneWidth = imageZoneWidth
        self.imageZone = tk.Frame(
            self, width=self.imageZoneWidth, height=self.imageZoneWidth/2)
        self.imageZone.pack(side='left')
        self.sliderZone = tk.Frame(
            self, width=self.imageZoneWidth/3, height=self.imageZoneWidth/2)
        self.sliderZone.pack(side='right')
        self.imageFrames = [WithImageFrame(self.imageZone, self.initialQuality, self.imageZoneWidth), WithOutImageFrame(
            self.imageZone, self.onSelectImages, self.imageZoneWidth)]
        self.pack()
        self.createWidget()

    def createWidget(self):
        self.compressButton = tk.Button(
            self.sliderZone, text='開始壓縮', command=self.onPressed)
        self.compressButton.config(state='disabled')
        self.compressButton.place(relx=0.5, rely=0.95, anchor='s')
        self.qualitySlider = tk.Scale(
            self.sliderZone, label='品質', from_=100, to=0, command=lambda v: self.onChangeSlider(int(v)))
        self.qualitySlider.config(state='disabled')
        self.qualitySlider.place(relx=0.5, rely=0.8, relheight=0.7, anchor='s')

    def onSelectImages(self, images):
        self.images = images
        self.imageFrames[0].tkraise()
        self.imageFrames[0].setFirstImageOriginal(self.images[0])
        self.compressButton.config(state='active')
        self.qualitySlider.config(state='active')
        self.qualitySlider.set(self.initialQuality)

    def onChangeSlider(self, value):
        self.imageFrames[0].compressImageAndPreview(value)

    def compress(self):
        self.compressButton.place_forget()
        self.progressIndicator = ttk.Progressbar(
            self.sliderZone, orient='horizontal', mode='determinate')
        self.progressIndicator.place(relx=0.5, rely=0.95, anchor='s')
        self.progressText = Label(self.sliderZone, text='0%')
        self.progressText.place(relx=0.85, rely=0.95, anchor='s')
        self.imageFrames[0].compressAllImagesAndSave(
            self.images, int(self.qualitySlider.get()), self.onCompressing)

    def onPressed(self):
        global compressThread
        compressThread = threading.Thread(target=self.compress, daemon=True)
        compressThread.start()
        self.after(10, self.checkCompressThread)

    def checkCompressThread(self):
        if compressThread.is_alive():
            self.after(10, self.checkCompressThread)
        else:
            self.progressIndicator.destroy()
            self.progressText.destroy()
            self.compressButton.place(relx=0.5, rely=0.95, anchor='s')
            self.compressButton.config(state='disabled')
            self.qualitySlider.set(0)
            self.qualitySlider.config(state='disabled')
            self.imageFrames[1].tkraise()

    def onCompressing(self, progress):
        self.progressIndicator.configure(value=progress)
        self.progressText.configure(text='{}%'.format(round(progress)))
