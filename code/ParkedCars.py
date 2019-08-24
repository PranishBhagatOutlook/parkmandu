"""
Determine the number of parking space using background subtraction
Algorithm:
    Subtract background from foreground
    filter for noise
    Binarize / Threshold
    Contour
    Filter out small contours
    Count bigger contours
"""

import cv2
import numpy as np
import MySQLdb

conn = MySQLdb.connect (host = "192.168.43.83",
                        user = "pratik",
                        passwd = "hello",
                        db = "parkmandu")

"""
def imageTransform(background, foreground):
    background = background[97:720, 480:1280]
    rows, cols= background.shape
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), -2, 1)
    background = cv2.warpAffine(background, M, (cols, rows))

    foreground = foreground[97:720, 480:1280]
    rows, cols= foreground.shape
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), -2, 1)
    foreground = cv2.warpAffine(foreground, M, (cols, rows))
"""


def emptyParkingSpaceCount(background, foreground, CAR_SIZE=0.01):
    """
    :param background:
    :param foreground:
    :return: no of empty parking space
    """
    emptyParkingSpace = 0

    # Gaussian smoothing for noise filter
    background = background[73:402, 133:598]
    cv2.imwrite("cropped.jpg", background)
    rows, cols = background.shape
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), -2, 1)
    background = cv2.warpAffine(background, M, (cols, rows))

    foreground = foreground[73:402, 133:598]
    rows, cols = foreground.shape
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), -2, 1)
    foreground = cv2.warpAffine(foreground, M, (cols, rows))

    background = cv2.GaussianBlur(background, (11, 11), 5)
    foreground = cv2.GaussianBlur(foreground, (11, 11), 5)
    cv2.imwrite("Gausback.jpg", background)
    cv2.imwrite("Gausfront.jpg", foreground)
    cv2.namedWindow('RES', cv2.WINDOW_NORMAL)
    cv2.namedWindow('CONTOURS', cv2.WINDOW_NORMAL)
    # background = cv2.erode(background,iterations=5)
    # foreground = cv2.erode(foreground, iterations=5)
    res = background - foreground

    # cv2.adaptiveThreshold(res, 255, cv2.THRESH_OTSU, cv2.THRESH_BINARY, (5,5),)
    res = cv2.inRange(res, 140, 230)
    res = cv2.dilate(res, None, iterations=10)

    # Res.copy() because cv2.findContours makes changes in the input image
    _, contours, _ = cv2.findContours(res.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #print "No of contours: ", len(contours)

    temp = res.copy()
    # cv2.drawContours(temp,contours, 0, (255,0,0),4,)
    for c in contours:
        normalizedArea = cv2.contourArea(c) / background.size
        if normalizedArea > CAR_SIZE:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(temp, (x,y), (x+w,y+h), (255,2,0), 5)
            emptyParkingSpace += 1

    cv2.imshow("RES", res)
    cv2.imshow("CONTOURS", temp)
    cv2.imwrite("contour.jpg", temp)
    cv2.waitKey(50)
    cv2.destroyAllWindows()
    return emptyParkingSpace


# def countParkingSpace(background):
#     cv2.threshold(background, 10,255, cv2.THRESH_BINARY, background)
#
#     # Res.copy() because cv2.findContours makes changes in the input image
#     contours, _ = cv2.findContours(background.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
#     for c in contours:
#         normalizedArea = cv2.contourArea(c)/background.size
#
#         # if normalizedArea > CAR_SIZE:
#         if 1:
#             # emptyParkingSpace += 1
#             print "Empty"
#
#     cv2.imshow("RES", background)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()


if __name__ == "__main__":
    file_index = 1
    # Camera 0 is the integrated web cam on my netbook
    camera_port = 2
 
    #Number of frames to throw away while the camera adjusts to light levels
    ramp_frames = 100

    camera = cv2.VideoCapture(camera_port)
 
    # Captures a single image from the camera and returns it in PIL format
    def get_image():
     # read is the easiest way to get a full image out of a VideoCapture object.
     retval, im = camera.read()
     return im

    try:
     while True: 
      # Ramp the camera - these frames will be discarded and are only used to allow v4l2
      # to adjust light levels, if necessary
      for i in xrange(ramp_frames):
       temp = get_image()
      print("Taking image...")
      # Take the actual image we want to keep
      camera_capture = get_image()
      file = "test_image_"+str(file_index)+".jpg"
      
      # A nice feature of the imwrite method is that it will automatically choose the
      # correct format based on the file extension you provide. Convenient!
      cv2.imwrite(file, camera_capture)
      background = cv2.imread("test_image_"+str(file_index)+".jpg", 0)
      foreground = cv2.imread("open_back.jpg", 0)
      file_index = file_index + 1
      TOTAL_PARKING_SPACE = 5
      #imageTransform(background = background, foreground = foreground)
      emptySpaceCount = emptyParkingSpaceCount(background=background, foreground=foreground)
      print "Occupied parking space : ", emptySpaceCount, " / ", TOTAL_PARKING_SPACE
      with conn:
          cursor = conn.cursor ()
          cursor.execute("UPDATE park SET Occupied = '"+str(emptySpaceCount)+"' WHERE mall = 'Kathmandu Mall'")
      cursor.close ()
      #conn.close ()
      
      #if file_index > 1:
          #break

    except KeyboardInterrupt:
     pass
 
    # You'll want to release the camera, otherwise you won't be able to create a new
    # capture object until your script exits
    del(camera)
 
   

    

