import cv2
import Tkinter
import tkFileDialog

#File operations Class
class FileOperations(object):
    fileTypes = None
    openFolder = None
    saveFolder = None
    openFile = None
    saveFile = None
    
    def __init__(self, fileTypes, openFolder, saveFolder, openFile, saveFile):
        self.fileTypes = fileTypes
        self.openFolder = openFolder
        self.saveFolder = saveFolder
        self.openFile = openFile
        self.saveFile = saveFile
        #print self.fileTypes, self.openFolder, self.saveFolder, self.openFile, self.saveFile

    def openFileDialog(self):
        Tkinter.Tk().withdraw() # Close the root window
        #defaultextension=self.fileTypes[0], 
        filePath = tkFileDialog.askopenfilename(filetypes=self.fileTypes, initialdir=self.openFolder, initialfile=self.openFile)
        return filePath
    
    def saveFileDialog(self, img):
        Tkinter.Tk().withdraw() # Close the root window
        filePath = tkFileDialog.asksaveasfilename(filetypes=self.fileTypes, initialdir=self.saveFolder, initialfile=self.saveFile)
        cv2.imwrite(filePath,img)
    
