import math
import cv2
import numpy as np
from Statistic import Statistic


class sudokuGridSorter:

    def __init__(self, boxes,referenceIdx,img=None,sudokuAngle=0):
        self.boxes= boxes
        self.referenceIdx = referenceIdx
        self.allDigitsCenter=[]
        self.img = img
        self.angleFactor = 180 / math.pi
        self.digitsSpacing= 0
        self.initAngle=sudokuAngle
        self.sudokuBox = None
        self.sudokuBoxSize = 0
        self.sudokuBoxCenter = 0
    # radian2Degree
    # return degree fro radian
    def radian2Degree(self, value):
        return value * self.angleFactor


    # degree2Radian
    # return radian from degree
    def degree2Radian(self, value):
        return value /self.angleFactor


    # cross
    # put a '+'  at the point on self.img
    def cross(self,point,color):
        x = point[0]
        y = point[1]
        cv2.line(self.img,(x-1,y),(x+1,y),color,1)
        cv2.line(self.img,(x,y-1),(x,y+1),color,1)


    # rotateImage
    # rotate image using  degree
    def rotateImage(self,image, angle):
       image_center = tuple(np.array(image.shape[1::-1]) / 2)
       rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
       result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
       return result


    # printGrid
    # print the A.I. boxes
    def printGrid(self):
        return
        for box in self.boxes:
            print(box)


    # isInsideBox
    # check of Point is inside the box
    def isInsideBox(self,Point,box):
        if Point[0] < box[0]:
            return False
        if Point[0] > box[2]:
            return False
        if Point[1] < box[1]:
            return False
        if Point[1] > box[3]:
            return False
        return True


    # rotatePoint
    # return  Point retotated from  self.sudokuBoxCenter
    def rotatePoint(self,angle,Point):
        cx = Point[0] - self.sudokuBoxCenter[0]
        cy = Point[1] - self.sudokuBoxCenter[1]
        vx = math.cos(angle)
        vy = math.sin(angle)
        x  = cx*vx - cy*vy
        y  = cx*vy + cy*vx
        x = x + self.sudokuBoxCenter[0]
        y = y + self.sudokuBoxCenter[1]
        return (x,y)


    # getAngle
    # return Angle between 2 points
    # return angle between -PI/2 to PI/2
    def getAngle(self, Point1,Point2):
        px = Point2[0] - Point1[0]
        py = Point1[1] - Point2[1]
        dist =math.sqrt(px*px + py*py)
        px = px / dist
        py = py / dist
        if py == 0:
            return 0
        #which is the greatest
        # use always  from left to right 
        if Point2[0] > Point1[0]:
                angle = math.atan2(py/dist,px/dist)
        else:
                angle = math.atan2(-py/dist,-px/dist)
        if angle > (math.pi/4):
           angle = angle - (math.pi/2)
        if angle < (-math.pi/4):
           angle = -(math.pi/2) - angle
        return angle


    # getallDigitsCenter
    # get center of the grid and all objects center inside the grid
    def getallDigitsCenter(self):
        if self.boxes is None:
            return False
        self.allDigitsCenter=[]
        self.sudokuBoxCenter=(0,0)
        #find  sudoku box first
        self.sudokuBox = None
        for box in self.boxes:
            ID = self.referenceIdx[int(box[5])]
            if ID == "Sudoku":
                self.sudokuBox = [box[0],box[1],box[2],box[3]]
                self.sudokuBoxSize = (abs(box[2]-box[0])+
                                      abs(box[3]-box[1])) /2
                gap = 10
                sudokuBoxInflated = [box[0]-gap,box[1]-gap,
                                     box[2]+gap,box[3]+gap]
        # do we have Sudoku  box
        if self.sudokuBox is None:
            return False
        # ok get center of everything
        for box in self.boxes:
            cx = int(box[0] + box[2]) //2
            cy = int(box[1] + box[3]) //2
            if not self.isInsideBox((cx,cy),sudokuBoxInflated):
                  continue
            ID = self.referenceIdx[int(box[5])]
            if ID == "Sudoku":
                self.sudokuBoxCenter=(cx,cy)
                #print("Grid center at ({},{})".format(cx,cy))
#                if self.img is not None:
#                    self.cross((cx,cy),(0,255,255))
            else:
                self.allDigitsCenter.append({"center":(cx , cy) ,
                                         "id": ID,
                                         "valid": True,
                                         "x":0,"y":0})
#                self.cross((cx,cy),(0,0,255))

        return True


    # findNearest
    # return the nearest digit from pointXY and the distance in pixel
    def findNearest(self, pointXY, error=0.0):
        bestDist = 99999.9
        bestBox = None
        for  centerBox in self.allDigitsCenter:
            dx = pointXY[0] - centerBox["center"][0]
            dy = pointXY[1] - centerBox["center"][1]
            dist = math.sqrt(dx*dx+dy*dy)
            if dist < bestDist:
                bestDist = dist
                bestBox = centerBox
                if dist < error:
                    return bestBox
        return bestBox, dist


    # getdigitsSpacing
    # return minimum spacing from center point of all digits
    # invalidate the second digit if it is too near
    # we assume that the grid is  aligned 
    def getdigitsSpacing(self, cBoxes, minSpacing):
        self.digitsSpacing = 0
        deltaX=[]
        deltaY=[]

        centerX = Statistic()
        centerY = Statistic()
        cx, cy = self.sudokuBoxCenter

        for digit in cBoxes:
            if abs(digit["center"][0] - cx) < minSpacing/2:
                centerX.add(digit["center"][0])
            if abs(digit["center"][1] - cy) < minSpacing/2:
                centerY.add(digit["center"][0])

        if centerX.count > 1:
            cx = centerX.mean()

        if centerY.count > 1:
            cx = centerY.mean()

        self.sudokuBoxCenter = (cx, cy)

        #get spacing between all objects
        for idx1 in range(len(cBoxes)-1):
            obj1 = cBoxes[idx1]
            if obj1["valid"] is False:
                continue
            for idx2 in range(idx1+1,len(self.allDigitsCenter)):
                obj2 = cBoxes[idx2]
                if obj2["valid"] is False:
                    continue
                dx = abs(obj1["center"][0] - obj2["center"][0])
                if dx >= minSpacing/2:
                    deltaX.append(dx)
                dy = abs(obj1["center"][1] - obj2["center"][1])
                if dy >= minSpacing/2:
                    deltaY.append(dy)
        deltaX.sort()
        deltaY.sort()
        # now get he minimum distance
        stat = Statistic()
        for i in deltaX:
            if stat.count == 0:
                stat.add(i)
            else:
                if (i - stat.mean()) > minSpacing /2 :
                    if stat.count == 1:
                        stat.clear()
                        stat.add(i)
                    else:
                       break

        spacingX = stat.mean()
        stat.clear()
        for i in deltaY:
            if stat.count == 0:
                stat.add(i)
            else:
                if (i - stat.mean()) > minSpacing /2 :
                    if stat.count == 1:
                        stat.clear()
                        stat.add(i)
                    else:
                       break
        spacingY = stat.mean()

        # ok we got the spacing
        # we need to figure out if it is x,2x,or3x, or 4x
        for i in range(1,9):
            spacing = spacingX / i
            if  (8 * spacing) < self.sudokuBoxSize:
                spacingX = spacing
                break

        for i in range(1,9):
            spacing = spacingY / i
            if  (8 * spacing) < self.sudokuBoxSize:
                spacingY = spacing
                break


        print("spacing X", spacingX,"spacingY", spacingY)

        if (spacingX > 1) and ( spacingY > 1):
            self.digitsSpacing = (spacingX + spacingY)/2
        elif spacingX > 1:
            self.digitsSpacing = spacingX
        elif spacingY > 1:
            self.digitsSpacing = spacingX
        else:
            self.digitsSpacing = self.sudokuBoxSize/9


    # sortGrid
    # return True/False is the sudoku grid has been validated
    # to extract the numbers
    def sortGrid(self):
        # get the center of all detected box
        # return True or False if suduko object exist and > 6 objects
        # will set self.sudokuBoxCenter  (center os sudoku)
        if self.getallDigitsCenter() is False:
            print("grid center not found")

        if len(self.allDigitsCenter) < 7:
            print("Number of Digits {} <  7 .Not enough digits!"
                  .format(len(self.allDigitsCenter)))
            return False
        #from each detect point get distance between  
        # sort and bin them
        self.sudokuBoxSize = ((self.sudokuBox[2] - self.sudokuBox[0])+
                            (self.sudokuBox[3] - self.sudokuBox[1]))/2

        self.getdigitsSpacing(self.allDigitsCenter, self.sudokuBoxSize)
        #let`s figure the spacing between Box
        min_cx=100
        min_cy=100
        max_cx=-100
        max_cy=-100
        for boxCenter in  self.allDigitsCenter:
            rx , ry = boxCenter["center"]
            rx = rx - self.sudokuBoxCenter[0]
            ry = ry - self.sudokuBoxCenter[1]
            cx = rx / self.digitsSpacing
            cy = ry / self.digitsSpacing
            if cx > 0.0:
               cx= int( cx + 0.49) + 4
            elif cx < 0.0:
               cx= int( cx - 0.49) + 4
            else:
               cx = 4
            if cy > 0.0:
               cy= int( cy + 0.49) + 4
            elif cy < 0.0:
               cy= int( cy - 0.49) + 4
            else:
               cy = 4
            if cx < min_cx:
               min_cx = cx
            if cy < min_cy:
               min_cy = cy
            if cx > max_cx:
               max_cx = cx
            if cy < max_cy:
               max_cy = cy
            boxCenter["x"]=cx
            boxCenter["y"]=cy
            #print("{}:{},{}".format(boxCenter["id"],cx,cy))
        # is the grid valid
        if  max_cx - min_cx > 8 :
            print("error min cx:{}  max cx:{}".format(min_cx,max_cx))
            return False
        if  max_cy - min_cy > 8 :
            print("error min cy:{}  max cy:{}".format(min_cy,max_cy))
            return False
        #do we have to shift grid
        offset_x=0
        offset_y=0
        if min_cx < 0:
            offset_x = min_cx
        if min_cy < 0:
            offset_y = min_cy
        if max_cx > 8:
            offset_x = 8 - max_cx
        if min_cy > 8:
            offset_y = 8 - max_cy
        #ok let's fill the grid
        self.grid=[x[:] for x in [[0] * 9] * 9]  
        #print("offset x:{} y:{}".format(offset_x, offset_y))
        for boxCenter in self.allDigitsCenter:
            vx = boxCenter["x"] + offset_x
            if vx < 0 :
                print("vx < 0")
                return False
            if vx > 8 :
                print("vx >8")
                return False
            vy = boxCenter["y"] + offset_y
            if vy < 0 :
                print("vy < 0")
                return False
            if vy > 8 :
                print("vy > 0")
                return False
            vx=int(vx)
            vy=int(vy)
            boxCenter["x"] = vx
            boxCenter["y"] = vy
            self.grid[vy][vx]=int(boxCenter["id"])
            #print("{}:{},{},{}".format(boxCenter["id"],vx,vy,self.grid[vy][vx]))
        return True









    def show(self,im,resolvGrid):
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        h , w, _  = im.shape
        fontsize =  w / 640
        fontWeight = 1
        if w > 320:
            fontWeight = 2

        #print("spacing : {}".format(self.spacing))

#        spacing = self.getGridSpacing(self.sudokuAngle)

        for x in  range(9):
            for y in range(9):
                if self.grid[y][x]==0:
                    if resolvGrid[y][x] is not None:
                        if resolvGrid[y][x] > 0:
                            text=str(resolvGrid[y][x])
                            textsize = cv2.getTextSize(text, font, fontsize,fontWeight)[0]
                            textX = int(textsize[0] / 3)
                            textY = int(textsize[1] / 3)
                            px =  self.sudokuBoxCenter[0] + (x - 4) * self.digitsSpacing
                            py =  self.sudokuBoxCenter[1] + (y - 4) * self.digitsSpacing
#                            px, py = self.rotatePoint(-self.sudokuAngle,(px,py))
                            px = int(px) - textX
                            py = int(py) + textY
                            #print("{},{}:{}".format(px,py,text))
                            cv2.putText(im,text, (px, py),font,
                                        fontsize, (0,0,128),fontWeight)







