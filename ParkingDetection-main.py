import cv2
import numpy as np
import matplotlib.pyplot as plt    #from matplotlib import pyplot as plt

from ParkingDetectionFiltering import FilteringParkingDetection
from ParkingDetectionSubstraction import SubstractionParkingDetection

#TODO:
    #Order image processing and filtering for best results
    #Implement parking spot size detection (average of most of contures with size ratio 2:3)
    #Detect cars and parking spots - print the number of empty and full parking spots

fileTypes = [('JPG', '.jpg'), ('PNG', '.png')]
dataFolder = './DATA/'

sampleFolder = './parking-sample/'
imgOpen = './parking-full-top-small.jpg'
imgSave = './parking-detect.png'

filePath = dataFolder+sampleFolder+imgOpen

pklotFolder = './parking-pkLot/'
imgSubOpen = './parking-2.jpg'
imgSubOpenBG = './parking-bg.jpg'

filePathSub = dataFolder+pklotFolder+imgSubOpen
filePathSubBG = dataFolder+pklotFolder+imgSubOpenBG

#Open file select dialog
#fo = FileOperations(fileTypes, str(dataFolder+sampleFolder), dataFolder, imgOpen, imgSave)
#filePath = fo.openFileDialog()

#Load an image modes: #1/cv2.IMREAD_COLOR #0/cv2.IMREAD_GRAYSCALE #-1/cv2.IMREAD_UNCHANGED
img = cv2.imread(filePath,1)
imgSub = cv2.imread(filePathSub,1)
imgBG = cv2.imread(filePathSubBG,1)

#Defining parking detection techniques - Class detection
fpd = FilteringParkingDetection()
spd = SubstractionParkingDetection()

print '1. Parking detection using image filtering'
print '2. Parking detection using background substraction'
teqNo = raw_input('Choose detection technique: ')

if(teqNo == '1'):    
    #Parking detection using image filtering
    img = fpd.detectParking(img, False)
elif(teqNo == '2'):
    #Parking detection using background substraction
    img = spd.detectParking(imgSub, imgBG, True)
else:
    print 'Wrong input!'

cv2.imshow('detection',img)

#-> Image save & end program

k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    #fo.saveFileDialog(img)
    cv2.imwrite(dataFolder+imgSave,img)
    cv2.destroyAllWindows()
