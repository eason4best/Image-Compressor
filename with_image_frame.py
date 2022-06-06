import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
import os


class WithImageFrame(tk.Frame):
    def __init__(self, master, initialQuality, imageZoneWidth):
        tk.Frame.__init__(self, master)
        self.imageZoneWidth = imageZoneWidth
        self.place(width=self.imageZoneWidth, height=self.imageZoneWidth/2)
        self.firstImageOriginal = None
        self.firstImageOriginalForDisplay = None
        self.firstImageCompressed = None
        self.firstImageCompressedForDisplay = None
        self.initialQuality = initialQuality
        self.createWidget()

    def createWidget(self):
        self.originalImageZone = tk.Frame(
            self, width=self.imageZoneWidth/2, height=self.imageZoneWidth/2, bg='white')
        self.originalImageZone.pack(side='left')
        self.compressedImageZone = tk.Frame(
            self, width=self.imageZoneWidth/2, height=self.imageZoneWidth/2, bg='white')
        self.compressedImageZone.pack(side='right')
        self.originalImageDisplay = tk.Label(
            self.originalImageZone, text='Original Image', image=self.firstImageOriginalForDisplay, bg='white')
        self.originalImageDisplay.place(
            relx=0.5, rely=0.5, relwidth=1.0, relheight=1.0, anchor='center')
        self.compressedImageDisplay = tk.Label(
            self.compressedImageZone, text='Compressed Image', image=self.firstImageCompressedForDisplay, bg='white')
        self.compressedImageDisplay.place(
            relx=0.5, rely=0.5, relwidth=1.0, relheight=1.0, anchor='center')
        self.divider = tk.Frame(
            self, width=1, height=self.imageZoneWidth/2, bg='grey')
        self.divider.place(relx=0.5, rely=0.5, anchor='center')
        self.originalImageLabel = tk.Label(
            self.originalImageZone, text='原圖', bg='white')
        self.originalImageLabel.place(relx=0.1, rely=0.95, anchor='center')
        self.compressedImageLabel = tk.Label(
            self.compressedImageZone, text='壓縮', bg='white')
        self.compressedImageLabel.place(relx=0.1, rely=0.95, anchor='center')

    def setFirstImageOriginal(self, imgPath):
        self.firstImageOriginal = self.cropImage(Image.open(imgPath))
        self.firstImageOriginalForDisplay = ImageTk.PhotoImage(
            self.firstImageOriginal)
        self.originalImageDisplay.configure(
            image=self.firstImageOriginalForDisplay)

    def cropImage(self, img):
        w, h = img.size
        if w < self.imageZoneWidth or h < self.imageZoneWidth:
            return img
        left = (w - self.imageZoneWidth)/2
        top = (h - self.imageZoneWidth)/2
        right = (w + self.imageZoneWidth)/2
        bottom = (h + self.imageZoneWidth)/2
        return img.crop((left, top, right, bottom))

    def convertToRGBChannel(self, img):
        return img.convert('RGB')

    def compressImageAndPreview(self, quality):
        buffer = BytesIO()
        self.convertToRGBChannel(self.firstImageOriginal).save(buffer, format='jpeg', quality=quality)
        buffer.seek(0)
        self.firstImageCompressed = Image.open(buffer)
        self.firstImageCompressedForDisplay = ImageTk.PhotoImage(
            self.firstImageCompressed)
        self.compressedImageDisplay.config(
            image=self.firstImageCompressedForDisplay)

    def compressAllImagesAndSave(self, images, quality, onCompressing):
        imagesCount = len(images)
        currentImage = 1
        for img in images:
            targetDirectory = os.path.join(
                os.path.dirname(img), '{}-已壓縮'.format(os.path.dirname(img).replace('\\','/').split('/')[-1]))
            if not os.path.isdir(targetDirectory):
                os.mkdir(targetDirectory)
            originalImg = Image.open(img)
            self.convertToRGBChannel(originalImg).save(os.path.join(
                targetDirectory, os.path.basename(img)), quality=quality, optimize=True)
            onCompressing((currentImage / imagesCount)*100)
            currentImage += 1
