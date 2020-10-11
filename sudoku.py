# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 17:29:08 2020

@author: Daniel Perron

this example  show how fill manually the
sudoku grid usign the keyboard.
The space bar is converted to '0'
'0' correspond to an empty case
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


import time
from sudokuSolver import sudokuSolver

import sys
from select import select
import termios
import atexit


'''
Keyboard  handling
'''


def set_normal_term():
    termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, old_term)

old_term = termios.tcgetattr(sys.stdin)

my_term = termios.tcgetattr(sys.stdin)
my_term[3] = (my_term[3] & ~termios.ICANON & ~termios.ECHO)
termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, my_term)
atexit.register(set_normal_term)


def kbhit():
    dr, dw, de = select([sys.stdin], [], [], 0)
    return dr != []


def getkey():
    return sys.stdin.read(1)


def EnterGrid(sudoku):
    print("Please enter digits! 0 for blank")
    print("|--------+--------+--------|")
    for row_idx in range(9):
        print("| ", end="")
        for col_idx in range(9):
            while True:
                while not kbhit():
                    pass
                key = getkey()
                if key == '\x1b':
                    return False
                if key == ' ':
                    key = "0"
                if ord(key) < 48:
                    continue
                if ord(key) > 57:
                    continue
                sudoku.grid[row_idx][col_idx] = int(key)
                break
            print("{} ".format(key), end="")
            sys.stdout.flush()
            if (col_idx % 3) == 2:
                print(" | ", end="")
        print("")
        if (row_idx % 3) == 2:
            print("|--------+--------+--------|")
    return True

sudoku = sudokuSolver()
if EnterGrid(sudoku):
    sudoku.fillGrid()
    if sudoku.isValid():
        if sudoku.isDone():
            print("Solved Sudoku")
        else:
            print("Sudoku not completely solved")
    else:
        print("Sudoku grid is invalid!") 
    sudoku.printGrid()

