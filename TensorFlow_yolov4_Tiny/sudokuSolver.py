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

class sudokuSolver:

    def __init__(self, grid=None):
        if grid is None:
            self.grid = [x[:] for x in [[0] * 9]*9]
        else:
            self.grid = copy.deepcopy(grid)
        self.allNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
#        how deep the number of guess  will be
        self.deepLevelMax = 5
        self.maxTime = 5
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
            if Number is None:
                continue
            if Number == 0:
                continue
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
            if Number is None:
                continue
            if Number == 0:
                continue
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
                if Number is None:
                    continue
                if Number == 0:
                    continue
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
            nbDigits = nbDigits + self.grid[row_i].count(0)
            nbDigits = nbDigits + self.grid[row_i].count(None)

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
            if Number is None:
                continue
            if Number > 0:
                try:
                    allPossibility.remove(Number)
                except ValueError:
                    pass
        return allPossibility

    def getColPossibility(self, col_i):
        allPossibility = self.allNumbers[:]
        for row_i in range(9):
            Number = self.grid[row_i][col_i]
            if Number is None:
                continue
            if Number > 0:
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
                if Number is None:
                    continue
                if Number > 0:
                    try:
                        allPossibility.remove(Number)
                    except ValueError:
                        pass
        return allPossibility

    def getCellPossibility(self, row_i, col_i, rowP=None,
                           colP=None, boxP=None):

        if not self.grid[row_i][col_i] is None:
            if self.grid[row_i][col_i] > 0:
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
                    return
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

        if Number is None:
            Number, row_i, col_i = self.getRowUniquePosition()
            if Number is None:
                Number, row_i, col_i = self.getColUniquePosition()
        return Number, row_i, col_i

    def isDone(self):
        for row_i in range(9):
            for col_i in range(9):
                if self.grid[row_i][col_i] is None:
                    return False
                if self.grid[row_i][col_i] == 0:
                    return False
        return True

    def huntForIt(self, deepLevel=0):
        originalGrid = self.grid
        for row_i in range(9):
            for col_i in range(9):
                if not self.grid[row_i][col_i] is None:
                    if self.grid[row_i][col_i] > 0:
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
                        return False
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
