import cv2

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened():
	rval, frame = vc.read()
else
	rval = False

while rval:
	cv2.imshow("preview", frame)
	rval, frame = vc.read()

cv2.destroyAllWindows()
