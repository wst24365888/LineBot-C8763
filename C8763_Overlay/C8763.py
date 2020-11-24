import os
import math

import cv2
import dlib
import numpy as np

from scipy import ndimage
from matplotlib import pyplot as plt

def get_X_Y_WIDTH(begin, end, landmarks, scale):
    x, y = 0, 0
    x_min, x_max = 99999, -1
    x_min_y, x_max_y = 99999, -1

    for n in range(begin, end):
        x += landmarks.part(n).x
        y += landmarks.part(n).y

        if landmarks.part(n).x < x_min:
            x_min = landmarks.part(n).x
            x_min_y = landmarks.part(n).y
        if landmarks.part(n).x > x_max:
            x_max = landmarks.part(n).x
            x_max_y = landmarks.part(n).y

    angle = -math.atan2((x_max_y-x_min_y), ((x_max-x_min)))/math.pi*180

    return int(x/(end-begin)), int(y/(end-begin)), int((x_max-x_min)*scale)*math.sqrt(math.sqrt(math.sqrt(abs(angle)))), angle

def getEven(value):
    return int(value) if int(value) % 2 == 0 else int(value) + 1

def overlay(x, y, w, h, xOffset, yOffset, toReplace, img):
    print("toReplace.shape: ({}, {})".format(w, h))

    # if w <= 0:
    #     w = getEven(1)

    # if h <= 0:
    #     h = getEven(1)

    lil = cv2.resize(toReplace, (w, h))    
    areaToReplace = img[y - int(h/2) - yOffset:y + int(h/2) - yOffset, x - int(w/2) - xOffset : x + int(w/2) - xOffset]
    
    for row in range(h):
        for column in range(w):
            if(lil[row][column][3] >= 100):
                areaToReplace[row][column] = lil[row][column]

    img[y - int(h/2) - yOffset:y + int(h/2) - yOffset, x - int(w/2) - xOffset : x + int(w/2) - xOffset] = areaToReplace

    return img

def getC8763Overlay(IMG_RGB):
    # Load Assets
    SCALE = 1.2

    C8763_LEFT_EYE = cv2.imread('/app/C8763_Overlay/C8763_left_eye_rotate.png', cv2.IMREAD_UNCHANGED)
    C8763_LEFT_EYE_RATIO = C8763_LEFT_EYE.shape[1] / C8763_LEFT_EYE.shape[0]
    C8763_LEFT_EYE_SCALE = 2.3*SCALE

    C8763_RIGHT_EYE = cv2.imread('/app/C8763_Overlay/C8763_right_eye.png', cv2.IMREAD_UNCHANGED)
    C8763_RIGHT_EYE_RATIO = C8763_RIGHT_EYE.shape[1] / C8763_RIGHT_EYE.shape[0]
    C8763_RIGHT_EYE_SCALE = 2.1*SCALE

    C8763_MOUTH = cv2.imread('/app/C8763_Overlay/C8763_mouth.png', cv2.IMREAD_UNCHANGED)
    C8763_MOUTH_RATIO = C8763_MOUTH.shape[1] / C8763_MOUTH.shape[0]
    C8763_MOUTH_SCALE = 1.25*SCALE

    # Load the detector
    detector = dlib.get_frontal_face_detector()

    # Load the predictor
    predictor = dlib.shape_predictor("/app/C8763_Overlay/shape_predictor_68_face_landmarks.dat")

    # read the image
    # IMG = cv2.imread("test12.jpg")

    # Convert image into grayscale
    gray = cv2.cvtColor(src=np.copy(IMG_RGB), code=cv2.COLOR_RGB2GRAY)

    # Convert to PNG
    # b,g,r = cv2.split(IMG)
    # IMG_RGB = cv2.merge([r,g,b])
    IMG_RGB = np.lib.pad(IMG_RGB, ((0,0),(0,0),(0,1)), 'constant', constant_values=(255))

    # return IMG_RGB

    # Use detector to find landmarks
    faces = detector(gray)
    
    LAST_WIDTH = 30

    for face in faces:
        x1 = face.left() # left point
        y1 = face.top() # top point
        x2 = face.right() # right point
        y2 = face.bottom() # bottom point

        # Create landmark object
        landmarks = predictor(image=gray, box=face)

        """
        Jaw Points = 0–16
        Right Brow Points = 17–21
        Left Brow Points = 22–26
        Nose Points = 27–35
        Right Eye Points = 36–41  #LEFT_EYE
        Left Eye Points = 42–47 #RIGHT_EYE
        Mouth Points = 48–60
        Lips Points = 61–67
        """

        LEFT_EYE_X, LEFT_EYE_Y, LEFT_EYE_WIDTH, LEFT_EYE_ANGLE = get_X_Y_WIDTH(36, 42, landmarks, C8763_LEFT_EYE_SCALE)
        RIGHT_EYE_X, RIGHT_EYE_Y, RIGHT_EYE_WIDTH, RIGHT_EYE_ANGLE = get_X_Y_WIDTH(42, 48, landmarks, C8763_RIGHT_EYE_SCALE)
        MOUTH_X, MOUTH_Y, MOUTH_WIDTH, MOUTH_ANGLE = get_X_Y_WIDTH(48, 61, landmarks, C8763_MOUTH_SCALE)

        # if width made some mistake (eg. <= 0), then use last width

        if LEFT_EYE_WIDTH <= 0:
            LEFT_EYE_WIDTH = LAST_WIDTH
        else:
            LAST_WIDTH = LEFT_EYE_WIDTH

        if RIGHT_EYE_WIDTH <= 0:
            RIGHT_EYE_WIDTH = LAST_WIDTH
        else:
            LAST_WIDTH = RIGHT_EYE_WIDTH

        if MOUTH_WIDTH <= 0:
            MOUTH_WIDTH = LAST_WIDTH
        else:
            LAST_WIDTH = MOUTH_WIDTH

        # Draw Point

        cv2.circle(img=IMG_RGB, center=(LEFT_EYE_X, LEFT_EYE_Y), radius=3, color=(0, 0, 255), thickness=-1)
        cv2.circle(img=IMG_RGB, center=(RIGHT_EYE_X, RIGHT_EYE_Y), radius=3, color=(0, 0, 255), thickness=-1)
        cv2.circle(img=IMG_RGB, center=(MOUTH_X, MOUTH_Y), radius=3, color=(0, 0, 255), thickness=-1)

        # Overlay C8763 LEFT EYE
        LEFT_EYE_HEIGHT = int(LEFT_EYE_WIDTH/C8763_LEFT_EYE_RATIO)

        LEFT_EYE_WIDTH = getEven(LEFT_EYE_WIDTH)
        LEFT_EYE_HEIGHT = getEven(LEFT_EYE_HEIGHT)

        LEFT_EYE_X_OFFSET = getEven(LEFT_EYE_WIDTH/(8 - (0 if LEFT_EYE_ANGLE < 5 else LEFT_EYE_ANGLE/4)))
        LEFT_EYE_Y_OFFSET = getEven(LEFT_EYE_HEIGHT/(6 + (0 if LEFT_EYE_ANGLE < 5 else LEFT_EYE_ANGLE/6)))

        IMG_RGB = overlay(LEFT_EYE_X, LEFT_EYE_Y, LEFT_EYE_WIDTH, LEFT_EYE_HEIGHT, LEFT_EYE_X_OFFSET, LEFT_EYE_Y_OFFSET, ndimage.rotate(C8763_LEFT_EYE, LEFT_EYE_ANGLE + (10 if LEFT_EYE_ANGLE < 5 else 20)), IMG_RGB)

        # Overlay C8763 RIGHT EYE
        RIGHT_EYE_HEIGHT = int(RIGHT_EYE_WIDTH/C8763_RIGHT_EYE_RATIO)

        RIGHT_EYE_WIDTH = getEven(RIGHT_EYE_WIDTH)
        RIGHT_EYE_HEIGHT = getEven(RIGHT_EYE_HEIGHT)

        RIGHT_EYE_X_OFFSET = getEven(0 if RIGHT_EYE_ANGLE < 5 else RIGHT_EYE_WIDTH/6)
        RIGHT_EYE_Y_OFFSET = getEven(RIGHT_EYE_HEIGHT/4.5 if RIGHT_EYE_ANGLE < 5 else RIGHT_EYE_HEIGHT/6)

        IMG_RGB = overlay(RIGHT_EYE_X, RIGHT_EYE_Y, RIGHT_EYE_WIDTH, RIGHT_EYE_HEIGHT, RIGHT_EYE_X_OFFSET, RIGHT_EYE_Y_OFFSET, ndimage.rotate(C8763_RIGHT_EYE, LEFT_EYE_ANGLE+5), IMG_RGB)

        # Overlay C8763 MOUTH
        MOUTH_HEIGHT = int(MOUTH_WIDTH/C8763_MOUTH_RATIO*math.sqrt(math.sqrt(math.sqrt(abs(MOUTH_ANGLE)))))

        MOUTH_WIDTH = getEven(MOUTH_WIDTH)
        MOUTH_HEIGHT = getEven(MOUTH_HEIGHT)

        IMG_RGB = overlay(MOUTH_X, MOUTH_Y, MOUTH_WIDTH, MOUTH_HEIGHT, 0, 0, ndimage.rotate(C8763_MOUTH, MOUTH_ANGLE+5), IMG_RGB)

        # Loop through all the points
        # for n in range(0, 68):
        #     x = landmarks.part(n).x
        #     y = landmarks.part(n).y

        #     # Draw a circle
        #     cv2.circle(img=IMG_RGB, center=(x, y), radius=1, color=(0, 255, 0), thickness=-1)

    # plt.figure(figsize=(20, 20))
    # plt.imshow(IMG_RGB)

    print("Overlay Complete.")

    return IMG_RGB
