import cv2
import numpy as np

from ImageHelper import ImageHelper as ih

#Rectangle selection Class
class RectSelection(object):
    ix,iy = -1,-1
    jx,jy = -1,-1
    selecting = False # true if mouse is pressed

    def __init__(self, img):
        self.img = img
        self.showSelectImage()

    def selectParkSize(self, event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.selecting = True
            self.ix,self.iy = x,y

        #elif event == cv2.EVENT_MOUSEMOVE:
        #    if self.selecting == True:
        #        cv2.rectangle(self.img,(self.ix,self.iy),(x,y),(0,0,255),2)

        elif event == cv2.EVENT_LBUTTONUP:
            self.selecting = False
            self.jx,self.jy = x,y
            cv2.rectangle(self.img,(self.ix,self.iy),(x,y),(0,0,255),2)

    def showSelectImage(self):
        cv2.namedWindow('image-select')    #necessary naming window for event environment
        cv2.setMouseCallback('image-select', self.selectParkSize)   #window of event, callback function

        while(True):
            cv2.imshow('image-select',self.img)

            k = cv2.waitKey(1) & 0xFF
            if k == 13:
                cv2.destroyWindow('image-select') #close image-select window on Enter/Return press
                break

    def getRectSize(self):
        rectWidth = abs(self.ix - self.jx)
        rectHeight = abs(self.iy - self.jy)
        return rectWidth, rectHeight
