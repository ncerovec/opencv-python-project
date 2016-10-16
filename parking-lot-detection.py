import cv2
import numpy as np
import matplotlib.pyplot as plt    #from matplotlib import pyplot as plt

imgName = 'parking-simplified-1.jpg'
dataFolder = './DATA/parking-sample/'

#Load an image modes: #1/cv2.IMREAD_COLOR #0/cv2.IMREAD_GRAYSCALE #-1/cv2.IMREAD_UNCHANGED
img = cv2.imread(dataFolder+imgName,1)

#-> Image processing
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#Otsu Threshold
ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

#Dilation - size of foreground object increases
    #kernel = np.ones((5,5),np.uint8)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(7,7)) #Rectangular Kernel
dilation = cv2.dilate(thresh,kernel,iterations = 1)
closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

#Canny filter
minLineLength = 10
maxLineGap = 5
edges = cv2.Canny(thresh, 30, 90)
#dst = cv2.Canny(thresh, 50, 200, 3)

#Probabilistic Hough Lines
lines = cv2.HoughLinesP(thresh, 1, np.pi/180 ,50,minLineLength,maxLineGap)

#Contoures
_, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

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
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
'''

#Images arrays
titles = ['Original','Gray','Otsu','Dilation', 'Closing', 'Canny']
images = [img, gray, thresh, dilation, closing, edges]
img_num = len(images)

#Advanced Image preview
plt.axis("off")
for i in xrange(img_num):
    plt.subplot(int(img_num/4)+1,4,i+1),plt.imshow(images[i],cmap = 'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()

final = img

#Simple Image preview
cv2.imshow('image',final)

k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    cv2.imwrite(dataFolder+'parking-detect.png',final)
    cv2.destroyAllWindows()
