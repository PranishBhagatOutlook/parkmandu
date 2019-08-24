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


def emptyParkingSpaceCount(background, foreground, CAR_SIZE=0.001):
    """
    :param background:
    :param foreground:
    :return: no of empty parking space
    """
    emptyParkingSpace = 0

    # Gaussian smoothing for noise filter
    background = cv2.GaussianBlur(background, (11, 11), 5)
    foreground = cv2.GaussianBlur(foreground, (11, 11), 5)

    # background = cv2.erode(background,iterations=5)
    # foreground = cv2.erode(foreground, iterations=5)
    res = background - foreground

    # cv2.adaptiveThreshold(res, 255, cv2.THRESH_OTSU, cv2.THRESH_BINARY, (5,5),)
    res = cv2.inRange(res, 140,230)
    res = cv2.dilate(res,None, iterations=10)

    # Res.copy() because cv2.findContours makes changes in the input image
    contours, _ = cv2.findContours(res.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    print "No of contours: ", len(contours)

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
    cv2.waitKey(0)
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
    background = cv2.imread("G:/Filters/Occupied.jpg", 0)
    foreground = cv2.imread("G:/Filters/Open.jpg", 0)
    TOTAL_PARKING_SPACE = 4
    emptySpaceCount = emptyParkingSpaceCount(background=background, foreground=foreground)
    print "Empty parking space : ", emptySpaceCount, " / ", TOTAL_PARKING_SPACE
