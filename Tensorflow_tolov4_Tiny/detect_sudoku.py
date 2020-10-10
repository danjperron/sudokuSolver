#================================================================
#
#   File name   : detect_mnist.py
#   Author      : PyLessons
#   Created date: 2020-08-12
#   Website     : https://pylessons.com/
#   GitHub      : https://github.com/pythonlessons/TensorFlow-2.x-YOLOv3
#   Description : mnist object detection example
#
#================================================================
import os
import copy
import glob
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import cv2
import numpy as np
import time
import tensorflow as tf
from yolov3.yolov4 import Create_Yolo
from yolov3.utils import detect_img
from yolov3.configs import *

from sudokuGridSorter import sudokuGridSorter
from sudokuSolver import sudokuSolver
from Statistic import Statistic
solver = sudokuSolver()

# ---------  camera size ----------
camWidth=640
camHeight=480

# --------   haugh Transform
import cv2
import numpy as np
import math


def haughTransform(img):
    gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)

    lines = cv2.HoughLines(edges,1,np.pi/180,200)
    if lines is None:
        return None
    statAngle = Statistic()
    angleTable = []
    for i in range(lines.shape[0]):
        rho, theta = lines[i][0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        dy = y2 - y1
        dx = x2 - x1
        A = 0
        if abs(dx) > abs(dy):
            if x1 < x2:
                A = 1
                angle = math.atan2(-dy,dx)
            else:
                A = 2
                angle = math.atan2(dy,dx)
        else:
            if y1 < y2:
                A = 3
                angle = math.atan2(dx,dy)
            else:
                A = 4
                angle = math.atan2(-dx,-dy)
        angleTable.append(angle)
        statAngle.add(angle)
#        print( dx, dy , angle * 180.0 / math.pi , A)
    # reject any angle higher than  5 degree  from target
    targetAngle=statAngle.mean()
    maxDegree = 5 * math.pi / 180
    statAngle.clear()
    for angle in angleTable:
        if (abs(angle -targetAngle)) <   maxDegree:
            statAngle.add(angle)
    if statAngle.count > 0:
        targetAngle = statAngle.mean()

    print("Best angle :", 180.0 * targetAngle / math.pi)
    return targetAngle


# ---------   main start ------

refID =[]
try:
    file = open("sudoku/sudoku.names","rt")
    lines= file.readlines()
    file.close()
    print(lines)

    for line in lines:
        line = line.strip()
        if  not line=='':
            refID.append(line)
except FileNotFoundError:
   print("Reference ID not found!")
   quit()

yolo = Create_Yolo(input_size=YOLO_INPUT_SIZE, CLASSES=TRAIN_CLASSES)

fname = f"./checkpoints/{TRAIN_MODEL_NAME}"
print("weight = {}".format(fname))
yolo.load_weights(fname) # use keras weights
print("weights loaded")


webcam=cv2.VideoCapture("/dev/video0")
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, camWidth)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, camHeight)

cv2.namedWindow("img",cv2.WINDOW_NORMAL)
cv2.resizeWindow("img",camWidth*2,camHeight)


imS =  np.zeros((camHeight, camWidth, 3), np.uint8)
imS[::]=(255,255,255)

# --------  main loop -------

webcamBuffer=5
while True:
    #decrease lag by clearing 5 images buffer
    for i in range(webcamBuffer):
        _, imI = webcam.read()
    #flip image

    imI = cv2.flip(imI,-1)
    sudokuAngle = haughTransform(imI)
    webcamBuffer = 2
    if sudokuAngle is not None:
        webcamBuffer=5
        #rotate image according to haug
        image_center = tuple(np.array(imI.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, -sudokuAngle * 180.0 / math.pi, 1.0)
        result  = cv2.warpAffine(imI, rot_mat, imI.shape[1::-1],
                         flags=cv2.INTER_LINEAR)
        imI = copy.deepcopy(result)
        im =  copy.deepcopy(imI)

        frame = np.hstack(( im,imS))
        cv2.imshow("img",frame)
        cv2.moveWindow("img",0,0)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

        imr, boxes = detect_img(yolo, im, "", input_size=YOLO_INPUT_SIZE, show=False, CLASSES=TRAIN_CLASSES, rectangle_colors=(255,0,0))
 #       print(boxes)
        frame = np.hstack(( imr,imS))
        cv2.imshow("img",frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

        imT= copy.deepcopy(imI)
        sudokuAngle=0
        gridSorter = sudokuGridSorter(boxes,refID,imT,sudokuAngle)
        gridSorter.printGrid()

        if gridSorter.sortGrid():
            solver.grid = copy.deepcopy(gridSorter.grid)
            solver.printGrid()
            solver.fillGrid()
            if solver.isDone():
                solver.printGrid()
                gridSorter.show(imT,solver.grid)
                imS=copy.deepcopy(imT)
                frame = np.hstack(( imr,imS))
                cv2.imshow("img",frame)
                print("Solve")
            else:
                solver.printGrid()
                print("no sort")
        #        imS = copy.deepcopy(gridSorter.img)
        #        frame = np.hstack(( imr,imS))
        #        cv2.imshow("img",frame)
        else:
            imS[::]=(255,255,255)
    else:
        imS[::]=(255,255,255)
        frame = np.hstack(( imI,imS))
        cv2.imshow("img",frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break


cv2.destroyAllWindows()
quit()

