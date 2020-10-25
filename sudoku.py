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
from sudokuSolver import sudokuSolver, SudokuDeepLevelError, SudokuTimeLimitError
import string
import sys

if sys.platform != "win32":
    from select import select
    import termios
    import atexit


'''
Keyboard  handling
'''
##HARDEST
target_sudoku = [
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


if sys.platform != "win32":
#
#--- Linux grid input routines
#
    def set_normal_term():
        termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, old_term)
        pass

    old_term = termios.tcgetattr(sys.stdin)
    my_term = termios.tcgetattr(sys.stdin)
    my_term[3] = (my_term[3] & ~termios.ICANON & ~termios.ECHO)
    termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, my_term)
    atexit.register(set_normal_term)

    def kbhit():
#        dr, dw, de = select([sys.stdin], [], [], 0)
        dr, _, _ = select([sys.stdin], [], [], 0)
        return dr != []
               
    def getkey():
        return sys.stdin.read(1)

    def get_a_char():
        while True:
            while not kbhit():
                pass
                key = getkey()
                if key == '\x1b':
                    print()
                    print("Exiting")
                    sys.stdout.flush()
                    sys.exit()
                if key == ' ':
                    key = "0"
                if ord(key) < 48:
                    continue
                if ord(key) > 57:
                    continue
                break
            return key

    def get_a_line(row_index):
        a_line=""
        for _ in range(9):
            a_line+=get_a_char()
        return a_line

    def InputGrid(mysudoku):
        print("Linux Version")
        print("Please enter 9 digits per line! 0 for blank")
        print("        |-------+-------+-------|")
        for row_idx in range(9):
            print("Ligne {} | ".format(row_idx), end="")
            sys.stdout.flush()
#            uneligne=get_a_line(row_idx)
            for col_idx in range(9):
                key = get_a_char()
                mysudoku.grid[row_idx][col_idx] = int(key)
                print("{} ".format(key), end="")
                sys.stdout.flush()
                if (col_idx % 3) == 2:
                    print("| ", end="")
            print("")
            if (row_idx % 3) == 2:
                print("        |-------+-------+-------|")
        return True

    def get_answer():
        answer=""
        while answer not in ("T","O","\x1b"):
            answer=input("Your Own grid, or Test grid (O/T) (ESC pour quitter)")
            answer=answer.upper().strip()[0]
        print(answer)
        sys.stdout.flush()
        if answer == '\x1b':
             print()
             print("Exiting")
             sys.stdout.flush()
             sys.exit()
        return answer

#
#--- Windows ALMOST equivalent grid input routines
#
else:
               
    def getkey():
        key= input()
        if '\x1b' in key:
            print()
            print("Exiting")
            sys.stdout.flush()
            sys.exit()
        return key

    def get_a_line(row_index):
        ligne_ok = False
        while not ligne_ok:
            print("Ligne {} | ".format(row_index), end="")
            a_line=getkey()
            if len([x for x in a_line if x in string.digits]) != 9 : continue
            break
        return a_line


    def InputGrid(mysudoku):
        print("Windows Version")
        print("Please enter 9 digits per line! 0 for blank")
        print("        | --------- |")
        for row_idx in range(9):
            uneligne=get_a_line(row_idx)
            for col_idx in range(9):
                mysudoku.grid[row_idx][col_idx] = int(uneligne[col_idx])
        return True

    def get_answer():
        answer=""
        while answer not in ("T","O","\x1b"):
            answer=input("Your Own grid, or Test grid (O/T) (ESC pour quitter)")
            answer=answer.upper().strip()[0]
#        print(answer)
        sys.stdout.flush()
        if answer == '\x1b':
             print()
             print("Exiting")
             sys.stdout.flush()
             sys.exit()
        return answer


def EnterGrid(mysudoku):
    #
    #--- test or user supplied ?
    myanswer = get_answer()
    if myanswer == "O" or target_sudoku == []:
        return InputGrid(mysudoku)
    else :    
        mysudoku.grid = target_sudoku
    return True


sudoku = sudokuSolver(deepLevelMax=15,maxTime=50)

if EnterGrid(sudoku):
    sudoku.printGrid()
    try:
        sudoku.solveGrid()
        if sudoku.isValid():
            if sudoku.isDone():
                print("Solved Sudoku (used %3d levels) in %6.2f seconds" %
                     (sudoku.deepestLevel, time.time() - sudoku.startTime)) 
            else:
                print("Sudoku not completely solved")
        else:
            print("Sudoku grid is invalid!") 

    except (SudokuDeepLevelError, SudokuTimeLimitError) as Erreur: 
        print("An ERROR occurred")
        print("Error = ",str(Erreur))
        sys.exit()

    sudoku.printGrid()    
else:
    print("Sudoku grid is invalid!") 
    sudoku.printGrid()

