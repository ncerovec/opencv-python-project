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
        img_median_val = np.median(img)
        #adptThreshGauss = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        adptThreshGauss = cv2.adaptiveThreshold(img, img_median_val, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13, -1)
        return adptThreshGauss
    
    #Canny filter
    @staticmethod
    def canny(img):
        sigma = 0.33
        img_median_val = np.median(img)
        lower_thresh = int(max(0, (1.0 - sigma) * img_median_val))
        upper_thresh = int(min(255, (1.0 + sigma) * img_median_val))
        canny = cv2.Canny(img, lower_thresh, upper_thresh)
        return canny

    #Erosion (opposite of dilation) - size of foreground object decreases
        #detach two connected objects (removing small white noises)
    @staticmethod
    def erosion(img):
        kernel = np.ones((3,3),np.uint8)
        erosion = cv2.erode(img,kernel,iterations = 1)
        return erosion

    #Dilation (opposite of erosion) - size of foreground object increases
        #joining broken parts of object
    @staticmethod
    def dilation(img):
        kernel = np.ones((3,3),np.uint8)
        dilation = cv2.dilate(img,kernel,iterations = 1)
        return dilation

    #Opening - Erosion followed by dilation
        #removing noise from and around object
    @staticmethod
    def opening(img):
        kernel = np.ones((3,3),np.uint8)
        opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        return opening

    #Closing - Dilation followed by Erosion
        #filling holes of object
    @staticmethod
    def closing(img):
        kernel = np.ones((3,3),np.uint8)
        closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        return closing

    #Morphological Gradient - Difference between dilation and erosion
        #outline of the object
    @staticmethod
    def gradient(img):
        kernel = np.ones((3,3),np.uint8)
        gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
        return gradient

    #Top Hat - Substraction of Opening from Original
        #remove minorities of object
    @staticmethod
    def tophat(img):
        kernel = np.ones((3,3),np.uint8)
        tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
        return tophat

    #Black Hat - Substraction of Original from Closing
        #highlight minorities of object
    @staticmethod
    def blackhat(img):
        kernel = np.ones((3,3),np.uint8)
        blackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)
        return blackhat

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

    #BilateralBlur
    @staticmethod
    def bilateralBlur(img):
        blur = cv2.bilateralFilter(img,9,75,75)
        return blur

    #GaussianBlur
    @staticmethod
    def gaussBlur(img):
        blur = cv2.GaussianBlur(img, (3,3), 0, 0, cv2.BORDER_DEFAULT)
        return blur

    #MedianBlur
    @staticmethod
    def medianBlur(img):
        blur = cv2.medianBlur(img, 3)
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
        spatialRadius = 30
        colorRadius = 20
        maxPyrLevel = 3
        meanShift = cv2.pyrMeanShiftFiltering(img, spatialRadius, colorRadius, maxPyrLevel)
        return meanShift

    #Color-Range filtering HSV
    @staticmethod
    def colorRange(img):
        #img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img_hsv = ProcessingColor.hsvScale(img)

        lower_black = np.array([0,0,0])
        upper_black = np.array([180,255,50])

        lower_white = np.array([0,0,200])
        upper_white = np.array([180,255,255])

        #lower_red0 = np.array([0,100,100])
        #upper_red0 = np.array([10,255,255])

        #lower_red1 = np.array([160,100,100])
        #upper_red1 = np.array([179,255,255])

        #lower_blue = np.array([100,150,0])
        #upper_blue = np.array([140,255,255])

        #lower_green = np.array([75,100,100])
        #upper_green = np.array([75,255,255])

        #lower_yellow = np.array([20,100,100])
        #upper_yellow = np.array([30,255,255])

        #lower_orange = np.array([14,0,0])
        #upper_orange = np.array([16,255,255])

        #mask_red0 = cv2.inRange(img_hsv, lower_red0, upper_red0)
        #mask_red1 = cv2.inRange(img_hsv, lower_red1, upper_red1)

        #mask_red = cv2.addWeighted(mask_red0, 1, mask_red1, 1, 1)

        mask_black = cv2.inRange(img_hsv, lower_black, upper_black)
        mask_white = cv2.inRange(img_hsv, lower_white, upper_white)

        mask = cv2.addWeighted(mask_black, 1, mask_white, 1, 0)
        #res = cv2.bitwise_or(mask_black,mask_white)
        return mask
