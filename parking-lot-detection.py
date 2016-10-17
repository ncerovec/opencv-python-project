import cv2
import numpy as np
import matplotlib.pyplot as plt    #from matplotlib import pyplot as plt

imgName = 'parking-full-top.jpg'
dataFolder = './DATA/parking-sample/'

# --> FUNCTIONS START <--

#Grayscale detection (gray/color type image) - returns true if the given 3 channel image is B=G=R
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
            
# --> FUNCTIONS END <--

#Load an image modes: #1/cv2.IMREAD_COLOR #0/cv2.IMREAD_GRAYSCALE #-1/cv2.IMREAD_UNCHANGED
img = cv2.imread(dataFolder+imgName,1)


#-> Image processing
ftrImg = img

#Clahe - LabColorSpace
lab = cv2.cvtColor(ftrImg, cv2.COLOR_BGR2Lab)
labChannels = cv2.split(lab)
#apply the CLAHE algorithm to the L channel
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)) #clahe->setClipLimit(4);
claLab = clahe.apply(labChannels[0]);
#Merge the the color planes back into an Lab image
np.copyto(claLab,labChannels[0]);
cla = cv2.merge(labChannels, lab);
#convert back to RGB
cla = cv2.cvtColor(cla, cv2.COLOR_Lab2BGR);

#MeanShift
spatialRadius = 20
colorRadius = 10
maxPyrLevel = 1
meanShift = cv2.pyrMeanShiftFiltering(ftrImg, spatialRadius, colorRadius, maxPyrLevel)

#Grayscale
gray = cv2.cvtColor(ftrImg, cv2.COLOR_BGR2GRAY)

#Equalize Histogram
equ = cv2.equalizeHist(gray)

#Clahe - Grayscale
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
claGray = clahe.apply(gray)

#Threshold (Adaptive)
ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)   #Otsu 
adptThreshMean = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2) #Adaptive Mean 
adptThreshGauss = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)    #Adaptive Gauss 

#Dilation - size of foreground object increases
    #kernel = np.ones((5,5),np.uint8)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(7,7)) #Rectangular Kernel
dilation = cv2.dilate(thresh,kernel,iterations = 1)
closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

#Canny filter
minLineLength = 50
maxLineGap = 50
edges = cv2.Canny(thresh, 30, 90)
#dst = cv2.Canny(thresh, 50, 200, 3)


#-> Image feature detection
dtcImg = dilation

#Contoures
_, contours, hierarchy = cv2.findContours(dtcImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#Probabilistic Hough Lines
lines = cv2.HoughLinesP(dtcImg, 1, np.pi/180 ,10,minLineLength,maxLineGap)

#Draw only biggest contour
'''
areas = [cv2.contourArea(c) for c in contours]
max_index = np.argmax(areas)
cnt=contours[max_index]
x,y,w,h = cv2.boundingRect(cnt)
cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
'''

#Draw all found contoures
for contour in contours:
    x,y,w,h = cv2.boundingRect(contour)
    #if(cv2.contourArea(rect) >= 2000 & (h/w) > 1.0):
    if(h*w >= 10000 and h*w <= 14000):
        #print h*w  #print contour sizes
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),1)

#Draw all found lines
'''
for x1,y1,x2,y2 in lines[0]:
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),1)
'''


#-> Image result preview

#Images arrays
titles = ['Original', 'EquHist', 'Clahe', 'Mean Shift', 'Gray', 'Clahe Gray', 'Otsu', 'Adaptive Mean', 'Adaptive Gauss', 'Dilation', 'Closing', 'Canny']
images = [img, equ, cla, meanShift, gray, claGray, thresh, adptThreshMean, adptThreshGauss, dilation, closing, edges]
img_num = len(images)

#Advanced Image preview
plt.axis("off")
for i in xrange(img_num):
    image = images[i]
    if(isGrayImage(image)):
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
    plt.subplot(int(img_num/4)+1,4,i+1),plt.imshow(image)
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()

#Simple Image preview
img1 = img
img2 = claGray
img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2RGB) if isGrayImage(img1) else img1
img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2RGB) if isGrayImage(img2) else img2
cmpResult = np.hstack((img1,img2)) #stacking images side-by-side
cv2.imshow('result',cmpResult)


#-> Image save & end program

k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    cv2.imwrite(dataFolder+'parking-detect.png',final)
    cv2.destroyAllWindows()
