import time, copy
from random import randint
from itertools import chain

grid=[]
for fill in range(9):
    grid.append([randint(1,9)]*9)
startTime = 0

def init(src_grid=None):
    global grid
#    nonlocal startTime 
    if src_grid is None:
        for row in range(9):
            for col in range(9):
                grid[row][col] = randint(1,9)
    else:
        grid = copy.deepcopy(src_grid)
    allNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
#        how deep the number of guess  will be
    deepLevelMax = 5
    maxTime = 5
    startTime = time.time()
    return grid

def isDone(grid):
    for row_i in range(9):
        for col_i in range(9):
            if grid[row_i][col_i] is None:
                return False
            if grid[row_i][col_i] == 0:
                return False
    return True

def isDone2(grid):
    for row_i in range(9):
        if None in grid[row_i] or 0 in grid[row_i]:
            return False
    return True

def isDone3(grid):
    for row_i in range(9):
        if not all(grid[row_i]):
            return False
    return True

def isDone4(grid):
    if not all(list(chain(*grid))):
        return False
    return True

#grid = []
#grid=init(None)
#print (grid)
grid=init(None)
#print (grid)
print (isDone(grid))
print (isDone2(grid))
print (isDone3(grid))
print (isDone4(grid))
import timeit
print(timeit.timeit('isDone(grid)', number=10000, globals=globals()))
print(timeit.timeit('isDone2(grid)', number=10000, globals=globals()))
print(timeit.timeit('isDone3(grid)', number=10000, globals=globals()))
print(timeit.timeit('isDone4(grid)', number=10000, globals=globals()))

