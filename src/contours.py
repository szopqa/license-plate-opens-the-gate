import numpy as np
import cv2
import  imutils
import os

from Reader import Reader

images_dir = './out_image_frames'

for each_frame in os.listdir(images_dir):
    image = cv2.imread(f'{images_dir}/{each_frame}')
    image = imutils.resize(image, width=600)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    th3 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)

    edged = cv2.Canny(th3, 170, 200)

    (new, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts=sorted(cnts, key = cv2.contourArea, reverse = True)[:10] #sort contours based on their area keeping minimum required area as '30' (anything smaller than this will not be considered)
    NumberPlateCnt = None #we currently have no Number plate contour

    # loop over our contours to find the best possible approximate contour of number plate
    count = 0
    for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:  # Select the contour with 4 corners
                NumberPlateCnt = approx #This is our approx Number Plate Contour
                cv2.drawContours(image, [NumberPlateCnt], -1, (0,255,0), 3)
                cv2.imshow("Final Image With Number Plate Detected", image)
                cv2.waitKey(0) #Wait for user input before closing the images displayed


