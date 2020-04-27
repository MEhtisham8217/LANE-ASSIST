import numpy as np
import cv2

img = cv2.imread('sample.jpeg',0)
cv2.imshow('image',img)
k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    cv2.imwrite('messigray.png',img)
    cv2.destroyAllWindows()

def gaussian_blur(img, kernel_size):
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
  
def canny(img, low_threshold, high_threshold):
    return cv2.Canny(img, low_threshold, high_threshold)


# apply gaussian blur
kernelSize = 5
gaussianBlur = gaussian_blur(img, kernelSize)

# canny
minThreshold = 100
maxThreshold = 200
edgeDetectedImage = canny(gaussianBlur, minThreshold, maxThreshold)

#display
cv2.imshow('image',edgeDetectedImage)
cv2.waitKey(0)
cv2.destroyAllWindows()
