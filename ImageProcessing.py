import cv2
import numpy as np

#Grayscale image processing Class
class ProcessingGray(object):

    #Clahe - Grayscale
    @staticmethod
    def claheGray(img):
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        claGray = clahe.apply(img)
        return claGray

    #Equalize Histogram
    @staticmethod
    def equHist(img):
        equ = cv2.equalizeHist(img)
        return equ

    #Otsu Threshold
    @staticmethod
    def threshOtsu(img):
        ret, threshOtsu = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        return threshOtsu

    #Adaptive Mean Threshold
    @staticmethod
    def threshAdptMean(img):
        adptThreshMean = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
        return adptThreshMean   

    #Adaptive Gauss Threshold
    @staticmethod
    def threshAdptGauss(img):
        #adptThreshGauss = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        adptThreshGauss = cv2.adaptiveThreshold(img, 230, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13, 0)
        return adptThreshGauss        

    #Dilation
    @staticmethod
    def dilation(img):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(7,7)) #Rectangular Kernel
        dilation = cv2.dilate(img,kernel,iterations = 1)
        return dilation

    #Closing
    @staticmethod
    def closing(img):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(7,7)) #Rectangular Kernel
        closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        return closing
    
    #Canny filter
    @staticmethod
    def canny(img):
        #canny = cv2.Canny(img, 50, 200, 3)
        canny = cv2.Canny(img, 30, 90)
        return canny

#Color image processing Class
class ProcessingColor(object):

    #Grayscale
    @staticmethod
    def grayScale(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return gray

    #HSV colorscale
    @staticmethod
    def hsvScale(img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        return hsv

    #GaussianBlur
    @staticmethod
    def gaussBlur(img):
        blur = cv2.GaussianBlur(img, (3,3), 0, 0, cv2.BORDER_DEFAULT)
        return blur

    #Clahe - Color
    @staticmethod
    def claheColor(img):
        #LabColorSpace
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        labChannels = cv2.split(lab)
        #apply the CLAHE algorithm to the L channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)) #clahe->setClipLimit(4);
        claLab = clahe.apply(labChannels[0]);
        #Merge the the color planes back into an Lab image
        np.copyto(claLab,labChannels[0]);
        cla = cv2.merge(labChannels, lab);
        #convert back to RGB
        cla = cv2.cvtColor(cla, cv2.COLOR_Lab2BGR);
        return cla

    #MeanShift
    @staticmethod
    def meanShift(img):
        spatialRadius = 20
        colorRadius = 20
        maxPyrLevel = 3
        meanShift = cv2.pyrMeanShiftFiltering(img, spatialRadius, colorRadius, maxPyrLevel)
        return meanShift
