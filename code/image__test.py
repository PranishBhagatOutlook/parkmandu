import numpy as np
import cv2

im = cv2.imread("test_image.jpg", 0)
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
print im.size
#im = cv2.GaussianBlur(im, (11, 11), 5)
im = cv2.inRange(im, 200, 255)
cv2.imshow("Image", im)
im = cv2.dilate(im, None, iterations=10)
cv2.imshow("Dilate", im)
cv2.waitKey(0)
cv2.destroyAllWindows()