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


previousFrame = None

tfFrame =  np.zeros((camHeight, camWidth, 3), np.uint8)
tfFrame[::]=(255,255,255)

rotatedFrame = copy.deepcopy(tfFrame)
sudokuFrame= copy.deepcopy(tfFrame)

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
cv2.resizeWindow("img",camWidth*3,camHeight)



# --------  main loop -------

webcamBuffer=5

# --------  timing for motion detection
start = time.time()
previousFrame = None
motion=False

while True:
    #decrease lag by clearing 5 images buffer

    for i in range(webcamBuffer):
        _, frame = webcam.read()
    #flip image
    frame = cv2.flip(frame,-1)

    # motion detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21),0)
    if previousFrame is None:
        previousFrame = gray
        continue
    diff_frame = cv2.absdiff(previousFrame,gray)
    previousFrame=gray
    thresh_frame = cv2.threshold(diff_frame,30,255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
    cnts,_ = cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL,
                              cv2.CHAIN_APPROX_SIMPLE)
    for contour in cnts:
        if cv2.contourArea(contour) < 10:
            continue
        start=time.time()

    frames = np.hstack(( frame,tfFrame,sudokuFrame))
    cv2.imshow("img",frames)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

    # is the image steady?
    # if not  skip the detection
    if time.time()-start < 0.1:
        webcamBuffer=1
        continue
    webcamBuffer=5

    sudokuAngle = haughTransform(frame)
    if sudokuAngle is not None:
        #rotate image according to haug
        image_center = tuple(np.array(frame.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, -sudokuAngle * 180.0 / math.pi, 1.0)
        rotatedFrame  = cv2.warpAffine(frame, rot_mat, frame.shape[1::-1],
                         flags=cv2.INTER_LINEAR)
        _tFrame=copy.deepcopy(rotatedFrame)
        tfFrame, boxes = detect_img(yolo, _tFrame, "", input_size=YOLO_INPUT_SIZE, show=False, CLASSES=TRAIN_CLASSES, rectangle_colors=(255,0,0))

        sudokuAngle=0
        gridSorter = sudokuGridSorter(boxes,refID,sudokuFrame,sudokuAngle)
        gridSorter.printGrid()

        if gridSorter.sortGrid():
            solver.grid = copy.deepcopy(gridSorter.grid)
            solver.printGrid()
            solver.fillGrid()
            if solver.isDone():
                solver.printGrid()
                sudokuFrame= copy.deepcopy(rotatedFrame)
                gridSorter.show(sudokuFrame,solver.grid)
                print("Solve")
            else:
                solver.printGrid()
                print("no sort")
        else:
            sudokuFrame[::]=(255,255,255)
    else:
        sudokuFrame[::]=(255,255,255)

cv2.destroyAllWindows()
quit()

