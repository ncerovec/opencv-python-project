import cv2
import numpy as np
import matplotlib.pyplot as plt    #from matplotlib import pyplot as plt

from ParkingDetection import ParkingDetection

from ImageProcessing import ProcessingGray as pg
from ImageProcessing import ProcessingColor as pc
from ImageFeaturing import FeatureDetection as fd
from ImagePreview import ImagePreview as ip

class SubstractionParkingDetection(ParkingDetection):

    def detectParking(self, img, imgBG, showProcess):
        #-> Image processing
        blurImg = pc.medianBlur(img)
        meanImg = pc.meanShift(blurImg)
        grayImg = cv2.cvtColor(meanImg, cv2.COLOR_BGR2GRAY)
        adpThreshImg = pg.threshAdptGauss(grayImg)

        blurBG = pc.medianBlur(imgBG)
        meanBG = pc.meanShift(blurBG)
        grayBG = cv2.cvtColor(meanBG, cv2.COLOR_BGR2GRAY)
        adpThreshBG = pg.threshAdptGauss(grayBG)

        diffImage = cv2.absdiff(adpThreshBG, adpThreshImg)

        #-> Image feature detection
        contours = fd.detectSqrContours(diffImage)
        img = fd.drawRatioContours(img, contours, 2, 0.2)

        #-> Image result preview
        if(showProcess):
            #Images arrays
            titles = ['Img', 'BG', 'Substraction']
            images = [adpThreshImg, adpThreshBG, diffImage]

            ip.showAdvanced(images, titles)
            #ip.showSimple(images, titles)

            img1 = adpThreshImg
            img2 = diffImage
            cv2.imshow('comparison',ip.stackImages(img1, img2))

        return img
