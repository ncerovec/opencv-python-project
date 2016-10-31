import Tkinter as tk
import os
import tkFileDialog


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

        # template file browse
        self.labelTemplatePath = tk.Label(master, text="Template file:")
        self.labelTemplatePath.grid(row=2, column=0, sticky=tk.W)

        self.filePathTemplateVar = ""
        self.filePathTemplate = tk.StringVar()
        self.filePathTemplate.set(self.filePathTemplateVar)
        self.entryTemplatePath = tk.Entry(master, width=60, textvariable=self.filePathTemplate)
        self.entryTemplatePath.grid(row=3, column=0)

        self.browseButtonTemplate = tk.Button(master, text='Browse', width=6, command=lambda: self.browse_file("template"))
        self.browseButtonTemplate.grid(row=3, column=1)

        self.browseButtonTemplate = tk.Button(master, text='Process', width=12, command= lambda : self.start_processing)
        self.browseButtonTemplate.grid(row=4, column=0)

    def browse_file(self, selector):
        self.master.withdraw()
        file = tkFileDialog.askopenfilename(filetypes=[("Image file", ("*.jpg", "*.jpeg", "*.png", "*.bmp"))])
        if selector=="image":
            self.filePathImageVar = file
            self.filePathImage.set(self.filePathImageVar)
        elif selector=="template":
            self.filePathTemplateVar = file
            self.filePathTemplate.set(self.filePathTemplateVar)

        self.master.deiconify()

    def getImagePath(self):
        return self.filePathImageVar

    def getTemplatePath(self):
        return self.filePathTemplateVar





'''
if __name__ == "__main__":

    global filePathImage
    global filePathTemplate

    mainWindow = tk.Tk()

    mainWindow.title('Parking analyse')
    mainWindow.resizable(False, False)

    #Image file browse
    labelImagePath = tk.Label(mainWindow, text="Image file:")
    labelImagePath.grid(row=0, column=0, sticky = tk.W)

    filePathImage = ""
    entryImagePath = tk.Entry(mainWindow, width=60, textvariable=filePathImage)
    entryImagePath.grid(row=1, column=0)

    browseButtonImage = tk.Button(master=mainWindow, text='Browse', width=6)
    browseButtonImage.grid(row=1, column=1)


    #template file browse
    labelTemplatePath = tk.Label(mainWindow, text="Template file:")
    labelTemplatePath.grid(row=2, column=0, sticky=tk.W)

    filePathTemplate = ""
    entryTemplatePath = tk.Entry(mainWindow, width=60, textvariable=filePathTemplate)
    entryTemplatePath.grid(row=3, column=0)

    browseButtonTemplate = tk.Button(master=mainWindow, text='Browse', width=6, command=browse_file)
    browseButtonTemplate.grid(row=3, column=1)

    mainWindow.mainloop()

'''