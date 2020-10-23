#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 21:05:13 2020
@author: daniel
Class to solve sudoku grid
   
"""
# Copyright © 2020, Daniel Perron
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.



import copy
import time

class SudokuDeepLevelError(Exception):
    """Exception when SudokuSolver exceeds DEEPLEVELMAX number of recursions"""
    def __init__(self, deeplevel):
        Exception.__init__(self)
        self.messageDLE = "SudokuSolver - requires more than {} levels".format(deeplevel)
    def __str__(self):
        return repr(self.messageDLE)

class SudokuTimeLimitError(Exception):
    """Exception when SudokuSolver exceeds MAXTIME for solving puzzle"""
    def __init__(self, maxtime):
        Exception.__init__(self)
        self.messageTLE = "SudokuSolver - requires more than {} second(s) to complete".format(maxtime)
    def __str__(self):
        return repr(self.messageTLE)

class sudokuSolver:

    DEEPLEVELMAX = 5  #maximum level of recursive analysis
    MAXTIME = 5       #maximum time (in seconds) allowed
    
    def __init__(self, grid=None,deepLevelMax=DEEPLEVELMAX, maxTime=MAXTIME):
        if grid is None:
            self.grid = [x[:] for x in [[0] * 9]*9]
        else:
            self.grid = copy.deepcopy(grid)
        self.allNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
#        how deep the number of guess  will be
        self.deepLevelMax = deepLevelMax
        self.deepestLevel = 0
        self.maxTime = maxTime
        self.startTime = time.time()

#print Grid   (0=empty)
    def printGrid(self, grid=None):
        if grid is None:
            grid = self.grid
        for r in range(9):
            if (r % 3) == 0:
                print("+-----------+-----------+-----------+")
            for c in range(9):
                if (c % 3) == 0:
                    print("| ", end="")
                else:
                    print("  ", end="")
                print("{} ".format(grid[r][c]), end="")
            print("|")
        print("+-----------+-----------+-----------+")


    def validateRow(self, row_i):
        Valid = []
        for col_i in range(9):
            Number = self.grid[row_i][col_i]
            if Number :
                try:
                    Valid.index(Number)
                except ValueError:
                    Valid.append(Number)
                    continue
                # if we are there then we have number twice
                return False, row_i, col_i
        return True, None, None

    def validateCol(self, col_i):
        Valid = []
        for row_i in range(9):
            Number = self.grid[row_i][col_i]
            if Number:
                try:
                    Valid.index(Number)
                except ValueError:
                    Valid.append(Number)
                    continue
                # if we are there then we have number twice
                return False, row_i, col_i
        return True, None, None

    def validateBox(self, box_i):
        row_base = (box_i//3) * 3
        col_base = (box_i % 3) * 3
        Valid = []
        for row_i in range(3):
            for col_i in range(3):
                Number = self.grid[row_base+row_i][col_base+col_i]
                if Number:
                    try:
                        Valid.index(Number)
                    except ValueError:
                        Valid.append(Number)
                        continue
                    # if we are there then we have number twice
                    return False, row_base+row_i, col_base+col_i
        return True, None, None

    def validateGrid(self):
        # Get number of Empty digits
        nbDigits = 0
        for row_i in range(9):
            nbDigits += (self.grid[row_i].count(0) + self.grid[row_i].count(None))

        if (81 - nbDigits) < 17:
            return False, 10, 10

        for i in range(9):
            valid, row, col = self.validateRow(i)
            if not valid:
                return False, row, col
            valid, row, col = self.validateCol(i)
            if not valid:
                return False, row, col
            valid, row, col = self.validateBox(i)
            if not valid:
                return False, row, col
        return True, None, None

    def isValid(self):
        valid, _, _  = self.validateGrid()
        return valid

    def getRowPossibility(self, row_i):
        allPossibility = self.allNumbers[:]
        for Number in self.grid[row_i]:
            if Number :
                try:
                    allPossibility.remove(Number)
                except ValueError:
                    pass
        return allPossibility

    def getColPossibility(self, col_i):
        allPossibility = self.allNumbers[:]
        for row_i in range(9):
            Number = self.grid[row_i][col_i]
            if Number:
                try:
                    allPossibility.remove(Number)
                except ValueError:
                    pass
        return allPossibility

    def getBoxPossibility(self, box_i):
        allPossibility = self.allNumbers[:]
        row_base = (box_i//3) * 3
        col_base = (box_i % 3) * 3

        for row_i in range(3):
            for col_i in range(3):
                Number = self.grid[row_base + row_i][col_base + col_i]
                if Number:  
                    try:
                        allPossibility.remove(Number)
                    except ValueError:
                        pass
        return allPossibility

    def getCellPossibility(self, row_i, col_i, rowP=None,
                           colP=None, boxP=None):

        if self.grid[row_i][col_i] : 
            return []
        box_i = (row_i // 3) * 3 + (col_i // 3)

        if rowP is None:
            rowP = self.getRowPossibility(row_i)[:]
        if colP is None:
            colP = self.getColPossibility(col_i)[:]
        if boxP is None:
            boxP = self.getBoxPossibility(box_i)[:]
        possibility = boxP[:]
        possibility = self.intersection(possibility[:], rowP)[:]
        possibility = self.intersection(possibility[:], colP)[:]
        return possibility

    def intersection(self, list1, list2):
        list3 = [value for value in list1 if value in list2]
        return list3

    def fillGrid(self, deepLevel=0):
        if deepLevel == 0:
            self.startTime = time.time()
        while True:
            Number, row_i, col_i = self.getNextNumber()
            if Number is None:
                if row_i is not None:
                    return
                if deepLevel > self.deepLevelMax:
                    raise SudokuDeepLevelError(self.deepLevelMax)
                self.deepestLevel=max(self.deepestLevel, deepLevel+1)
                self.huntForIt(deepLevel+1)
                break
            else:
                self.grid[row_i][col_i] = Number
#       self.printGrid()

    def getNextNumberByPossibility(self):
        cols_possibility = 9*[None]
        boxs_possibility = 9*[None]

        for row_i in range(9):
            row_possibility = self.getRowPossibility(row_i)
            if len(row_possibility) == 0:
                continue
            for col_i in range(9):
                if cols_possibility[col_i] is None:
                    cols_possibility[col_i] = self.getColPossibility(col_i)
                box_i = (row_i // 3) * 3 + (col_i // 3)
                if boxs_possibility[box_i] is None:
                    boxs_possibility[box_i] = self.getBoxPossibility(box_i)
                possibility = self.getCellPossibility(row_i, col_i,
                                                      row_possibility,
                                                      cols_possibility[col_i],
                                                      boxs_possibility[box_i])
                if len(possibility) == 1:
                    return possibility[0], row_i, col_i
                if len(possibility) == 0:
                    if self.grid[row_i][col_i] == 0:
                        return None, row_i, col_i
        return None, None, None

    def getBoxUniquePosition(self, box_i):
        row_base = (box_i//3) * 3
        col_base = (box_i % 3) * 3

        boxPossibility = self.getBoxPossibility(box_i)

        for Number in boxPossibility:
            count = 0
            row_found = None
            col_found = None
            for row_i in range(3):
                for col_i in range(3):
                    cellPossibility = self.getCellPossibility(row_base+row_i,
                                                              col_base+col_i)
                    try:
                        cellPossibility.index(Number)
                    except ValueError:
                        continue
                    count = count + 1
                    row_found = row_i + row_base
                    col_found = col_i + col_base
            if count == 1:
                #  we got one Number to a unique place
                return Number, row_found, col_found
        return None, None, None

    def getRowUniquePosition(self, row_i):
        rowPossibility = self.getRowPossibility(row_i)

        for Number in rowPossibility:
            count = 0
            col_found = None
            for col_i in range(9):
                cellPossibility = self.getCellPossibility(row_i, col_i)
                try:
                    cellPossibility.index(Number)
                except ValueError:
                    continue
                count = count + 1
                col_found = col_i
            if count == 1:
                #  we got one Number to a unique place
                return Number, row_i, col_found
        return None, None, None

    def getColUniquePosition(self, col_i):
        colPossibility = self.getColPossibility(col_i)

        for Number in colPossibility:
            count = 0
            row_found = None
            for row_i in range(9):
                cellPossibility = self.getCellPossibility(row_i, col_i)
                try:
                    cellPossibility.index(Number)
                except ValueError:
                    continue
                count = count + 1
                row_found = row_i
            if count == 1:
                #  we got one Number to a unique place
                return Number, row_found, col_i
        return None, None, None

    def getNextNumberByUniquePosition(self):
        for box_index in range(9):
            Number, row_i, col_i = self.getBoxUniquePosition(box_index)
            if Number is not None:
                return Number, row_i, col_i
        for row_index in range(9):
            Number, row_i, col_i = self.getRowUniquePosition(row_index)
            if Number is not None:
                return Number, row_i, col_i
        for col_index in range(9):
            Number, row_i, col_i = self.getColUniquePosition(col_index)
            if Number is not None:
                return Number, row_i, col_i
        return None, None, None



    def isDone(self):
        for row_i in range(9):
            if all(self.grid[row_i]):
                continue
            return False
        return True

    def huntForIt(self, deepLevel=0):
        originalGrid = self.grid
        for row_i in range(9):
            for col_i in range(9):
                if self.grid[row_i][col_i]:
                    continue
                cellPossibility = self.getCellPossibility(row_i, col_i)
                for guessNumber in cellPossibility:
                    #  copy original grid
                    self.grid = copy.deepcopy(originalGrid)
                    self.grid[row_i][col_i] = guessNumber
                    self.fillGrid(deepLevel)
                    if self.isDone():
                        return True
                    if (time.time() - self.startTime) > self.maxTime:
                        raise SudokuTimeLimitError(self.maxTime)
        return False

    def getNextNumber(self):
        valid, row_i, col_i = self.validateGrid()
        if not valid:
            return None, row_i, col_i
        Number, row_i, col_i = self.getNextNumberByPossibility()
        if Number is None:
            return self.getNextNumberByUniquePosition()
        return Number, row_i, col_i

    def getAllCellsPossibility(self):
        allPossibility = []
        cols_possibility = 9*[None]
        boxs_possibility = 9*[None]
        for row_i in range(9):
            row_possibility = self.getRowPossibility(row_i)
            for col_i in range(9):
                if cols_possibility[col_i] is None:
                    cols_possibility[col_i] = self.getColPossibility(col_i)
                box_i = (row_i // 3) * 3 + col_i % 3
                if boxs_possibility[box_i] is None:
                    boxs_possibility[box_i] = self.getBoxPossibility(box_i)
                possibility = self.getCellPossibility(row_i, col_i,
                                                      row_possibility,
                                                      cols_possibility[col_i],
                                                      boxs_possibility[box_i])
                allPossibility.append([row_i, col_i,
                                      self.grid[row_i][col_i],
                                      possibility[:]])
        return allPossibility

    def printPossibility(self):
        valid, row_i, col_i = self.validateGrid()
        if not valid:
            print("Grid Invalid Row:{}  Col:{}".format(row_i, col_i))
            return None, row_i, col_i
        cols_possibility = 9*[None]
        boxs_possibility = 9*[None]
        for row_i in range(9):
            row_possibility = self.getRowPossibility(row_i)
            for col_i in range(9):
                if cols_possibility[col_i] is None:
                    cols_possibility[col_i] = self.getColPossibility(col_i)
                box_i = (row_i // 3) * 3 + col_i % 3
                if boxs_possibility[box_i] is None:
                    boxs_possibility[box_i] = self.getBoxPossibility(box_i)
                possibility = self.getCellPossibility(row_i, col_i,
                                                      row_possibility,
                                                      cols_possibility[col_i],
                                                      boxs_possibility[box_i])
                print("grid[{}][{}]={} p:{} pr:{} pc:{} pb:{}".format(
                        row_i, col_i,
                        self.grid[row_i][col_i], possibility,
                        row_possibility, cols_possibility[col_i],
                        boxs_possibility[box_i]))

if __name__ == "__main__":
##HARDEST
    import sys
    
    hard_sudoku = [
    [8,0,0,0,0,0,0,0,0],
    [0,0,3,6,0,0,0,0,0],
    [0,7,0,0,9,0,2,0,0],
    [0,5,0,0,0,7,0,0,0],
    [0,0,0,0,4,5,7,0,0],
    [0,0,0,1,0,0,0,3,0],
    [0,0,1,0,0,0,0,6,8],
    [0,0,8,5,0,0,0,1,0],
    [0,9,0,0,0,0,4,0,0]
    ]
    hard_sudoku_solution = [
    [8,1,2,7,5,3,6,4,9],
    [9,4,3,6,8,2,1,7,5],
    [6,7,5,4,9,1,2,8,3],
    [1,5,4,2,3,7,8,9,6],
    [3,6,9,8,4,5,7,2,1],
    [2,8,7,1,6,9,5,3,4],
    [5,2,1,9,7,4,3,6,8],
    [4,3,8,5,2,6,9,1,7],
    [7,9,6,3,1,8,4,5,2]
    ]
#
#---Test valid Grid
#
    target_sudoku = copy.deepcopy(hard_sudoku)
    sudoku = sudokuSolver(deepLevelMax=15,maxTime=999)
    sudoku.grid = target_sudoku
    print("sudokuSolver - testing valid sudoku grid : ", end="")
    if sudoku.isValid():
        print("PASSED")
    else:
        print("FAILED")
#
#---Test invalid Grid 
#
    print("sudokuSolver - testing INvalid sudoku grid : ", end="")
    sudoku.grid[1][1]=8
    if not sudoku.isValid():
        print("PASSED")
    else:
        print("FAILED")

#
#---Test too little time allowed (raise SudokuTimeLimitError) 
#
    print("sudokuSolver - testing with hard sudoku grid that requires time, using 0.01 seconds ")
    print("               expecting 'SudokuTimeLimitError' raised : ",end="")
    target_sudoku = copy.deepcopy(hard_sudoku)
    sudoku = sudokuSolver(deepLevelMax=15,maxTime=0.01)
    sudoku.grid=target_sudoku
    try:
        sudoku.fillGrid()
    except Exception as Erreur: 
        if hasattr(Erreur, "messageTLE"):
            print("PASSED")
        else:
            print("FAILED")
            print("sudokuSolver - Unexpected error :",str(Erreur))
            print("sudokuSolver - exiting")
            sys.exit()
#
#---Test not enough recursive levels (raise SudokuDeepLevelError) 
#
    print("sudokuSolver - testing with hard sudoku grid that requires 14 levels, using 5 ")
    print("               expecting 'SudokuDeepLevelError' raised : ",end="")
    target_sudoku = copy.deepcopy(hard_sudoku)
    sudoku = sudokuSolver(deepLevelMax=5,maxTime=999)
    sudoku.grid=target_sudoku
    try:
        sudoku.fillGrid()
    except Exception as Erreur: 
        if hasattr(Erreur, "messageDLE"):
            print("PASSED")
        else:
            print("FAILED")
            print("sudokuSolver - Unexpected error :",str(Erreur))
            print("sudokuSolver - exiting")
            sys.exit()
#
#---Test solution and provided by algorythm 
#
    print("sudokuSolver - testing solutioning a hard sudoku grid")
    print("               expecting successful internal checks : ",end="")
    target_sudoku = copy.deepcopy(hard_sudoku)
    sudoku = sudokuSolver(deepLevelMax=15,maxTime=999)
    sudoku.grid=target_sudoku
    try:
        sudoku.fillGrid()
        timespent= time.time() - sudoku.startTime 
        if sudoku.isValid():
            if sudoku.isDone():
                print("PASSED")
            else:
                print("FAILED")
                print("sudokuSolver - Unexpected error : <is.Done> returned False")
                sys.exit()
        else:
            print("FAILED")
            print("sudokuSolver - Unexpected error : <is.Valid> returned False")
            sys.exit()
    except Exception as Erreur:
        print("FAILED")
        print("sudokuSolver - Unexpected error :",str(Erreur))
        print("sudokuSolver - exiting")
        sys.exit()
#
#---compare solution of algorythm against known result 
#
    print("sudokuSolver - comparing solution to expected result : ",end="")
    if sudoku.grid == hard_sudoku_solution :
        print("PASSED")
        print()
        print("Solved Sudoku (used %3d levels) in %6.2f seconds" %
             (sudoku.deepestLevel, timespent)) 
    else:
        print("FAILED")
        print("sudokuSolver - Unexpected resulting solution")
        print("ORIGINAL sudoku matrix")
        sudoku.printGrid(hard_sudoku)
        print()
        print("ERRONEOUS SOLUTION sudoku matrix")
        sudoku.printGrid()
        print()
        print("EXPECTED  SOLUTION sudoku matrix")
        sudoku.printGrid(hard_sudoku_solution)
        sys.exit()
#
# --- print successful resolution
#
    print()
    print("ORIGINAL sudoku matrix")
    sudoku.printGrid(hard_sudoku)
    print()
    print("SOLUTION sudoku matrix")
    sudoku.printGrid()
#
# --- end of tests
#
    print("sudokuSolver - Testing completed, exiting")
    sys.exit()
 