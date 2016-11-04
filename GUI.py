import Tkinter as tk
import tkFileDialog
from ParkingDetectionTemplateGUI import TemplateParkingDetection
from ParkingDetectionFilteringGUI import FilteringParkingDetection
from ParkingDetectionSubtractionGUI import SubtractionParkingDetection
from ParkingDetectionBgSubModelGUI import BgSubModelParkingDetection
from FrameCapture import FrameCapture


class uiTemplate:
    def __init__(self, master):
        self.master = master
        master.title("Template matching")
        master.resizable(False, False)

        labelImagePath = tk.Label(master, text="Image file:")
        labelImagePath.grid(row=0, column=0, sticky=tk.W)

        self.filePathImageVar = ""
        self.filePathImage = tk.StringVar()
        self.filePathImage.set(self.filePathImageVar)
        self.entryImagePath = tk.Entry(master, width=60, textvariable=self.filePathImage)
        self.entryImagePath.grid(row=1, column=0)

        browseButtonImage = tk.Button(master, text='Browse', width=6, command=lambda: self.browse_file("image"))
        browseButtonImage.grid(row=1, column=1)

        captureButton = tk.Button(master, text='Capture', width=6, command=lambda: self.capture())
        captureButton.grid(row=1, column=2)

        # template file browse
        labelTemplatePath = tk.Label(master, text="Template file:")
        labelTemplatePath.grid(row=2, column=0, sticky=tk.W)

        self.filePathTemplateVar = ""
        self.filePathTemplate = tk.StringVar()
        self.filePathTemplate.set(self.filePathTemplateVar)
        self.entryTemplatePath = tk.Entry(master, width=60, textvariable=self.filePathTemplate)
        self.entryTemplatePath.grid(row=3, column=0)

        browseButtonTemplate = tk.Button(master, text='Browse', width=6, command=lambda: self.browse_file("template"))
        browseButtonTemplate.grid(row=3, column=1)

        processButton = tk.Button(master, text='Process', width=12, command=lambda: self.start_processing())
        processButton.grid(row=4, column=0)

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

    def getImagePath(self):
        return self.filePathImageVar

    def getTemplatePath(self):
        return self.filePathTemplateVar

    def capture(self):
        capture = FrameCapture(deviceID=0)
        if (capture.captureImage(fileName="frame.jpg") == 1):
            self.filePathImageVar = "frame.jpg"
            self.filePathImage.set(self.filePathImageVar)

    def start_processing(self):
        tpd = TemplateParkingDetection()
        self.master.withdraw()
        tpd.detectParking(self.filePathImageVar, self.filePathTemplateVar)
        self.master.deiconify()


class uiFiltering:
    def __init__(self, master):
        self.master = master
        master.title("Filtering image")
        master.resizable(False, False)

        self.labelImagePath = tk.Label(master, text="Image file:")
        self.labelImagePath.grid(row=0, column=0, sticky=tk.W)

        self.filePathImageVar = ""
        self.filePathImage = tk.StringVar()
        self.filePathImage.set(self.filePathImageVar)
        self.entryImagePath = tk.Entry(master, width=60, textvariable=self.filePathImage)
        self.entryImagePath.grid(row=1, column=0)

        browseButtonImage = tk.Button(master, text='Browse', width=6, command=lambda: self.browse_file())
        browseButtonImage.grid(row=1, column=1)

        captureButton = tk.Button(master, text='Capture', width=6, command=lambda: self.capture())
        captureButton.grid(row=1, column=2)

        processButton = tk.Button(master, text='Process', width=12, command=lambda: self.start_processing())
        processButton.grid(row=4, column=0)

    def browse_file(self):
        self.master.withdraw()

        file = tkFileDialog.askopenfilename(filetypes=[("Image file", ("*.jpg", "*.jpeg", "*.png", "*.bmp"))])
        self.filePathImageVar = file
        self.filePathImage.set(self.filePathImageVar)

        self.master.deiconify()

    def getImagePath(self):
        return self.filePathImageVar

    def capture(self):
        capture = FrameCapture(deviceID=0)
        if (capture.captureImage(fileName="frame.jpg") == 1):
            self.filePathImageVar = "frame.jpg"
            self.filePathImage.set(self.filePathImageVar)

    def start_processing(self):
        fpd = FilteringParkingDetection()
        self.master.withdraw()
        fpd.detectParking(self.filePathImageVar)
        self.master.deiconify()


class uiBasicSub:
    def __init__(self, master):
        self.master = master
        master.title("Simple background subtraction")
        master.resizable(False, False)

        labelImagePath = tk.Label(master, text="Image file:")
        labelImagePath.grid(row=0, column=0, sticky=tk.W)

        self.filePathImageVar = ""
        self.filePathImage = tk.StringVar()
        self.filePathImage.set(self.filePathImageVar)
        self.entryImagePath = tk.Entry(master, width=60, textvariable=self.filePathImage)
        self.entryImagePath.grid(row=1, column=0)

        browseButtonImage = tk.Button(master, text='Browse', width=6, command=lambda: self.browse_file("image"))
        browseButtonImage.grid(row=1, column=1)

        captureButton = tk.Button(master, text='Capture', width=6, command=lambda: self.capture())
        captureButton.grid(row=1, column=2)

        # template file browse
        labelBackground = tk.Label(master, text="Background image:")
        labelBackground.grid(row=2, column=0, sticky=tk.W)

        self.fileBackgroundPathVar = ""
        self.fileBackgroundPath = tk.StringVar()
        self.fileBackgroundPath.set(self.fileBackgroundPathVar)
        self.entryBackgroundPath = tk.Entry(master, width=60, textvariable=self.fileBackgroundPath)
        self.entryBackgroundPath.grid(row=3, column=0)

        browseButtonBackground = tk.Button(master, text='Browse', width=6,
                                           command=lambda: self.browse_file("background"))
        browseButtonBackground.grid(row=3, column=1)

        processButton = tk.Button(master, text='Process', width=12, command=lambda: self.start_processing())
        processButton.grid(row=4, column=0)

    def browse_file(self, selector):
        self.master.withdraw()
        file = tkFileDialog.askopenfilename(filetypes=[("Image file", ("*.jpg", "*.jpeg", "*.png", "*.bmp"))])
        if selector == "image":
            self.filePathImageVar = file
            self.filePathImage.set(self.filePathImageVar)
        elif selector == "background":
            self.fileBackgroundPathVar = file
            self.fileBackgroundPath.set(self.fileBackgroundPathVar)

        self.master.deiconify()

    def getImagePath(self):
        return self.filePathImageVar

    def getBackgroundPath(self):
        return self.fileBackgroundPathVar

    def capture(self):
        capture = FrameCapture(deviceID=0)
        if (capture.captureImage(fileName="frame.jpg") == 1):
            self.filePathImageVar = "frame.jpg"
            self.filePathImage.set(self.filePathImageVar)

    def start_processing(self):
        spd = SubtractionParkingDetection()
        self.master.withdraw()
        spd.detectParking(self.filePathImageVar, self.fileBackgroundPathVar)
        self.master.deiconify()


class uiBgndModel:
    def __init__(self, master):
        self.master = master
        master.title("Background modeling")
        master.resizable(False, False)

        labelImagePath = tk.Label(master, text="Image file:")
        labelImagePath.grid(row=0, column=0, sticky=tk.W)

        self.filePathImageVar = ""
        self.filePathImage = tk.StringVar()
        self.filePathImage.set(self.filePathImageVar)
        self.entryImagePath = tk.Entry(master, width=60, textvariable=self.filePathImage)
        self.entryImagePath.grid(row=1, column=0)

        browseButtonImage = tk.Button(master, text='Browse', width=6, command=lambda: self.browse_file())
        browseButtonImage.grid(row=1, column=1)

        captureButton = tk.Button(master, text='Capture', width=6, command=lambda: self.capture())
        captureButton.grid(row=1, column=2)

        # template file browse
        labelEmptyPath = tk.Label(master, text="Empty pictures folder:")
        labelEmptyPath.grid(row=2, column=0, sticky=tk.W)

        self.folderEmptyPathVar = ""
        self.folderEmptyPath = tk.StringVar()
        self.folderEmptyPath.set(self.folderEmptyPathVar)
        self.entryEmptyFolder = tk.Entry(master, width=60, textvariable=self.folderEmptyPath)
        self.entryEmptyFolder.grid(row=3, column=0)

        browseButtonEmptyFolder = tk.Button(master, text='Browse', width=6, command=lambda: self.browse_folder())
        browseButtonEmptyFolder.grid(row=3, column=1)

        processButton = tk.Button(master, text='Process', width=12, command=lambda: self.start_processing())
        processButton.grid(row=4, column=0)

    def browse_file(self):
        self.master.withdraw()
        file = tkFileDialog.askopenfilename(filetypes=[("Image file", ("*.jpg", "*.jpeg", "*.png", "*.bmp"))])
        self.filePathImageVar = file
        self.filePathImage.set(self.filePathImageVar)
        self.master.deiconify()

    def browse_folder(self):
        self.master.withdraw()
        folder = tkFileDialog.askdirectory()
        self.folderEmptyPathVar = folder
        self.folderEmptyPath.set(self.folderEmptyPathVar)
        self.master.deiconify()

    def getImagePath(self):
        return self.filePathImageVar

    def getEmptyFolderPath(self):
        return self.folderEmptyPathVar

    def capture(self):
        capture = FrameCapture(deviceID=0)
        if (capture.captureImage(fileName="frame.jpg") == 1):
            self.filePathImageVar = "frame.jpg"
            self.filePathImage.set(self.filePathImageVar)

    def start_processing(self):
        bpd = BgSubModelParkingDetection()
        self.master.withdraw()
        bpd.detectParking(self.filePathImageVar, self.folderEmptyPathVar)
        self.master.deiconify()
