import cv2
import numpy as np
import matplotlib.pyplot as plt    #from matplotlib import pyplot as plt

from ImageHelper import ImageHelper as ih
from ImageProcessing import ProcessingGray as pg
from ImageProcessing import ProcessingColor as pc
from ImageFeaturing import FeatureDetection as fd
from ImagePreview import ImagePreview as ip
from RectSizeSelection import RectSelection
#from FileOperations import FileOperations

#TODO:
    #Order image processing and filtering for best results
    #Implement parking spot size detection (average of most of contures with size ratio 2:3)
    #Detect cars and parking spots - print the number of empty and full parking spots

fileTypes = [('JPG', '.jpg'), ('PNG', '.png')]
imgOpen = './parking-full-top-small.jpg'
imgSave = './parking-detect.png'
sampleFolder = './parking-sample/'
dataFolder = './DATA/'

filePath = dataFolder+sampleFolder+imgOpen

#Open file select dialog
#fo = FileOperations(fileTypes, str(dataFolder+sampleFolder), dataFolder, imgOpen, imgSave)
#filePath = fo.openFileDialog()

#Load an image modes: #1/cv2.IMREAD_COLOR #0/cv2.IMREAD_GRAYSCALE #-1/cv2.IMREAD_UNCHANGED
img = cv2.imread(filePath,1)

#-> Parking spot size marking
#print "Select parking spot size and press Enter:"
#rs = RectSelection(ih.copyImage(img))
#rectWidth, rectHeight = rs.getRectSize()
rectWidth, rectHeight = 60,110
print "Parking spot size: " + str(rectWidth) + "x" + str(rectHeight)

#-> Image processing
ftrImg = ih.copyImage(img)

'''
claColor = pc.claheColor(ftrImg)
meanShift = pc.meanShift(ftrImg)
gray = pc.grayScale(ftrImg)
equ = pg.equHist(gray)
claGray = pg.claheGray(gray)
thresh = pg.threshOtsu(gray)
adptThreshMean = pg.threshAdptMean(gray)
adptThreshGauss = pg.threshAdptGauss(gray)
dilation = pg.dilation(thresh)
closing = pg.closing(thresh)
canny = pg.canny(gray)
result = canny
'''

blur = pc.medianBlur(ftrImg)
mean = pc.meanShift(blur)
colRange = pc.colorRange(mean)

gray = cv2.cvtColor(mean, cv2.COLOR_BGR2GRAY)
adpThresh = pg.threshAdptGauss(gray)

res = cv2.bitwise_and(colRange,adpThresh)
gradient = pg.gradient(colRange)
closing = pg.closing(gradient)
result = closing

'''
blur = pc.bilateralBlur(ftrImg)
mean = pc.meanShift(blur)
gray = pc.grayScale(mean)

sobelx8u = cv2.Sobel(gray,cv2.CV_8U,1,0,ksize=5)
canny = pg.canny(sobelx8u)

adpThresh = pg.threshAdptGauss(gray)

res = np.bitwise_or(canny,adpThresh)
opening = pg.opening(res)
result = sobelx8u
'''

#-> Image feature detection
dtcImg = ih.copyImage(result)

#img = fd.drawLines(img, fd.detectLines(dtcImg))

contours = fd.detectSqrContours(dtcImg)
#img = fd.drawBiggestContour(img, contours)
#img = fd.drawContours(img, contours)
img = fd.drawSizedContours(img, contours, rectWidth, rectHeight, 0.2)
#img = fd.drawRatioContours(img, contours, 2, 0.2)


#-> Image result preview

#Images arrays
#titles = ['Original', 'EquHist', 'Clahe', 'Mean Shift', 'Gray', 'Clahe Gray', 'Otsu', 'Adaptive Mean', 'Adaptive Gauss', 'Dilation', 'Closing', 'Canny']
#images = [img, equ, claColor, meanShift, gray, claGray, thresh, adptThreshMean, adptThreshGauss, dilation, closing, canny]
#titles = ['Original', 'HSV', 'V-channel', 'Blur', 'Mean', 'Gray', 'Adp Thresh Gauss']
#images = [img, hsv, v, blur, mean, gray, adpThresh]
titles = ['Original', 'Blur', 'Mean', 'Color-Range', 'Gray', 'Thresh', 'Gradient', 'Closing']
images = [img, blur, mean, colRange, gray, adpThresh, gradient, closing]
#titles = ['Original', 'Blur', 'Mean', 'Gray', 'Canny', 'Thresh', 'Canny+Thresh', 'Opening']
#images = [img, blur, mean, gray, canny, adpThresh, res, opening]

ip.showAdvanced(images, titles)
#ip.showSimple(images, titles)

img1 = img
img2 = result
cv2.imshow('comparison',ip.stackImages(img1, img2))

cv2.imshow('result',img)


#-> Image save & end program

k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    #fo.saveFileDialog(img)
    cv2.imwrite(dataFolder+imgSave,img)
    cv2.destroyAllWindows()
