import Tkinter as tk
import os
import tkFileDialog
from ParkingDetectionTemplateGUI import TemplateParkingDetection
from FrameCapture import FrameCapture


class GUI:
    def __init__(self, master):
        self.master = master
        master.title("GUI")
        master.resizable(False, False)

        self.labelImagePath = tk.Label(master, text="Image file:")
        self.labelImagePath.grid(row=0, column=0, sticky=tk.W)

        self.filePathImageVar = ""
        self.filePathImage = tk.StringVar()
        self.filePathImage.set(self.filePathImageVar)
        self.entryImagePath = tk.Entry(master, width=60, textvariable=self.filePathImage)
        self.entryImagePath.grid(row=1, column=0)

        self.browseButtonImage = tk.Button(master, text='Browse', width=6, command=lambda: self.browse_file("image"))
        self.browseButtonImage.grid(row=1, column=1)

        self.captureButton = tk.Button(master, text='Capture', width=6, command=lambda: self.capture())
        self.captureButton.grid(row=1, column=2)

        # template file browse
        self.labelTemplatePath = tk.Label(master, text="Template file:")
        self.labelTemplatePath.grid(row=2, column=0, sticky=tk.W)

        self.filePathTemplateVar = ""
        self.filePathTemplate = tk.StringVar()
        self.filePathTemplate.set(self.filePathTemplateVar)
        self.entryTemplatePath = tk.Entry(master, width=60, textvariable=self.filePathTemplate)
        self.entryTemplatePath.grid(row=3, column=0)

        self.browseButtonTemplate = tk.Button(master, text='Browse', width=6,
                                              command=lambda: self.browse_file("template"))
        self.browseButtonTemplate.grid(row=3, column=1)

        self.browseButtonTemplate = tk.Button(master, text='Process', width=12, command=lambda: self.start_processing())
        self.browseButtonTemplate.grid(row=4, column=0)

    def browse_file(self, selector):
        self.master.withdraw()
        file = tkFileDialog.askopenfilename(filetypes=[("Image file", ("*.jpg", "*.jpeg", "*.png", "*.bmp"))])
        if selector == "image":
            self.filePathImageVar = file
            self.filePathImage.set(self.filePathImageVar)
        elif selector == "template":
            self.filePathTemplateVar = file
            self.filePathTemplate.set(self.filePathTemplateVar)

        self.master.deiconify()
        return

    def getImagePath(self):
        return self.filePathImageVar

    def getTemplatePath(self):
        return self.filePathTemplateVar

    def capture(self):
        capture = FrameCapture(deviceID=0)
        capture.captureImage(fileName="frame.jpg")
        self.filePathImageVar = "frame.jpg"
        self.filePathImage.set(self.filePathImageVar)
        return

    def start_processing(self):
        tpd = TemplateParkingDetection()
        self.master.withdraw()
        tpd.detectParking(self.filePathImageVar, self.filePathTemplateVar)
        self.master.deiconify()
        return
