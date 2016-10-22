import cv2
import numpy as np

#Image feature detection Class
class FeatureDetection(object):
        
    #Probabilistic Hough Lines
    @staticmethod
    def detectLines(img):
        minLineLength = 50
        maxLineGap = 50
        lines = cv2.HoughLinesP(img, 1, np.pi/180 ,10,minLineLength,maxLineGap)
        return lines

    #Contours
    @staticmethod
    def detectSqrContours(img):
        _, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    #Draw lines in array
    @staticmethod
    def drawLines(img, lines):
        for x1,y1,x2,y2 in lines[0]:
            cv2.line(img,(x1,y1),(x2,y2),(0,255,0),1)
        return img

    #Draw contours in array
    @staticmethod
    def drawContours(img, contours):
        for contour in contours:
            x,y,w,h = cv2.boundingRect(contour)
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),1)
        return img

    #Draw certain size contours in array (deviation = %/100)
    @staticmethod
    def drawSizedContours(img, contours, width, height, deviation):
        devWidth = width*deviation
        devHeight = height*deviation
        minWidth = width-devWidth
        maxWidth = width+devWidth
        minHeight = height-devHeight
        maxHeight = height+devHeight
        
        for contour in contours:
            x,y,w,h = cv2.boundingRect(contour)
            if(w > minWidth and w < 100 and h > 100 and h < 150):
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),1)
        return img

    #Draw certain aspect ratio contours in array (ratio=height:width) (deviation = ratio-part)
    def drawRatioContours(img, contours, ratio, deviation):
        minRatio = ratio - deviation
        maxRatio = ratio + deviation
        
        for contour in contours:
            x,y,w,h = cv2.boundingRect(contour)
            contRatio = float(h)/float(w)
            #print contRatio
            
            #filtering contours by width and height ratio
            if(contRatio > 1.8 and contRatio < 2.3):
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),1)
        return img
        
    #Draw only biggest contour in array
    @staticmethod
    def drawBiggestContour(img, contours):
        areas = [cv2.contourArea(c) for c in contours]
        max_index = np.argmax(areas)
        cnt=contours[max_index]
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        return img
