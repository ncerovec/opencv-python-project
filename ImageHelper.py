import cv2
import numpy as np

#Image helper Class
class ImageHelper(object):
        
    #Grayscale detection (gray/color type image) - returns true if the given 3 channel image is B=G=R
    #@classmethod   #has (access to) object properties (self, cls..) as first parameters
    @staticmethod
    def isGrayImage(img):
        dimNum = len(img.shape)
        if(dimNum > 2):
            bgr = cv2.split(img)

            dst = cv2.absdiff(bgr[0], bgr[1])
            if(cv2.countNonZero(dst)):  return False;

            dst = absdiff(bgr[0], bgr[2])
            return not cv2.countNonZero(dst)
        else:
            return True

    #Copy image array using NumPy library
    @staticmethod
    def copyImage(img):
        copy = np.copy(img)
        return copy
