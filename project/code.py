import numpy as np
import cv2
import time

def gaussian_blur(img, kernel_size):
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
  
def canny(img, low_threshold, high_threshold):
    return cv2.Canny(img, low_threshold, high_threshold)

def region_of_interest(img, vertices):
    #defining a blank mask to start with
    mask = np.zeros_like(img)   
    
    #defining a 3 channel or 1 channel color to fill the mask with 
    #depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def draw_lines(img, lines, color=[  0, 255, 255], thickness=5):
    imshape = img.shape
    
    # these variables represent the y-axis coordinates to which 
    # the line will be extrapolated to
    ymin_global = img.shape[0]
    ymax_global = img.shape[0]
    
    # left lane line variables
    all_left_grad = []
    all_left_y = []
    all_left_x = []
    
    # right lane line variables
    all_right_grad = []
    all_right_y = []
    all_right_x = []
    
    for line in lines:
        for x1,y1,x2,y2 in line:
            gradient, intercept = np.polyfit((x1,x2), (y1,y2), 1)
            ymin_global = min(min(y1, y2), ymin_global)
            
            if (gradient > 0):
                all_left_grad += [gradient]
                all_left_y += [y1, y2]
                all_left_x += [x1, x2]
            else:
                all_right_grad += [gradient]
                all_right_y += [y1, y2]
                all_right_x += [x1, x2]
    
    left_mean_grad = np.mean(all_left_grad)
    left_y_mean = np.mean(all_left_y)
    left_x_mean = np.mean(all_left_x)
    left_intercept = left_y_mean - (left_mean_grad * left_x_mean)
    
    right_mean_grad = np.mean(all_right_grad)
    right_y_mean = np.mean(all_right_y)
    right_x_mean = np.mean(all_right_x)
    right_intercept = right_y_mean - (right_mean_grad * right_x_mean)
    
    # Make sure we have some points in each lane line category
    if ((len(all_left_grad) > 0) and (len(all_right_grad) > 0)):
        upper_left_x = int((ymin_global - left_intercept) / left_mean_grad)
        lower_left_x = int((ymax_global - left_intercept) / left_mean_grad)
        upper_right_x = int((ymin_global - right_intercept) / right_mean_grad)
        lower_right_x = int((ymax_global - right_intercept) / right_mean_grad)

        cv2.line(img, (upper_left_x, ymin_global), 
                      (lower_left_x, ymax_global), color, thickness)
        cv2.line(img, (upper_right_x, ymin_global), 
                      (lower_right_x, ymax_global), color, thickness)
    
cap = cv2.VideoCapture("lane.mp4")
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # apply gaussian blur
    gaussianBlur = gaussian_blur(gray, 5)
    
    # canny
    edgeDetectedImage = canny(gaussianBlur, 50, 150)
    
    #apply mask
    lowerLeftPoint = [130, 540]
    upperLeftPoint = [410, 350]
    upperRightPoint = [570, 350]
    lowerRightPoint = [915, 540]
    pts = np.array([[lowerLeftPoint, upperLeftPoint, upperRightPoint,lowerRightPoint]], dtype=np.int32)
    masked_image = region_of_interest(edgeDetectedImage, pts)
    
    #hough lines
    lines = cv2.HoughLinesP(masked_image, 1, np.pi/180, 30, np.array([]),15, 15)
    draw_lines(frame, lines)
                              
    cv2.imshow("results", frame)
    
    if cv2.waitKey(1) == ord('q'):
       break
       

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()    
