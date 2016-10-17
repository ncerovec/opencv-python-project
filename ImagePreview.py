import cv2
import numpy as np
import matplotlib.pyplot as plt    #from matplotlib import pyplot as plt

from ImageHelper import ImageHelper as ih

#Image preview Class
class ImagePreview(object):
        
    #PyPlot - Advanced Image preview
    @staticmethod
    def showAdvanced(images, titles):
        img_num = len(images)
        plt.axis("off")
        for i in xrange(img_num):
            image = images[i]
            if(ih.isGrayImage(image)):
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            else:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
            plt.subplot(int(img_num/4)+1,4,i+1),plt.imshow(image)
            plt.title(titles[i])
            plt.xticks([]),plt.yticks([])
        plt.show()

    #Stack images for comparison
    @staticmethod
    def stackImages(img1, img2):
        global showSimple
        img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2RGB) if ih.isGrayImage(img1) else img1
        img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2RGB) if ih.isGrayImage(img2) else img2
        cmpResult = np.hstack((img1,img2)) #stacking images side-by-side
        return cmpResult
