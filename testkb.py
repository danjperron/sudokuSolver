# -*- coding: utf-8 -*-

import time
import string
import sys

from select import select
import termios
import atexit


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
    if True:
        print("Linux Version")
        print("Please enter digits! 0 for blank")
        print("        |-------+-------+-------|")
        for row_idx in range(9):
            print("Ligne {} | ".format(row_idx), end="")
            sys.stdout.flush()
#            uneligne=get_a_line(row_idx)
            for col_idx in range(9):
                key = get_a_char()
            #    mysudoku.grid[row_idx][col_idx] = int(key)
                print("{} ".format(key), end="")
                sys.stdout.flush()
                if (col_idx % 3) == 2:
                    print("| ", end="")
            print("")
            if (row_idx % 3) == 2:
                print("        |-------+-------+-------|")
        return True


def EnterGrid(mysudoku):
    #
    #--- test or user supplied ?
    answer=""
    while answer not in ("T","O"):
        answer=input("Your Own grid, or Test grid (O/T) (ESC pour quitter)")
        answer=answer.upper().strip()[0]
    print(answer)
    sys.stdout.flush()
    if answer == "O" :
        return InputGrid(mysudoku)

mysudoku=[]
EnterGrid(mysudoku)
