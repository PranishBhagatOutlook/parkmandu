import cv2
import numpy as np

im = cv2.imread("to_crop.jpg", 1)
crop_im = im[97:720, 480:1250]
rows,cols, _ = crop_im.shape
M = cv2.getRotationMatrix2D((cols/2,rows/2),-2,1)
dst = cv2.warpAffine(crop_im,M,(cols,rows))
cv2.namedWindow("Cropped", cv2.WINDOW_NORMAL)
cv2.imshow("Cropped", dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
