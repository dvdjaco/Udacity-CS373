# ----------
# User Instructions:
# 
# Create a function compute_value() which returns
# a grid of values. Value is defined as the minimum
# number of moves required to get from a cell to the
# goal. 
#
# If it is impossible to reach the goal from a cell
# you should assign that cell a value of 99.

# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost_step = 1 # the cost associated with moving from a cell to an adjacent one.

# ----------------------------------------
# insert code below
# ----------------------------------------

'''
 use an (i,j) scan to take into account stochastic movement. Goes through
 every x,y position, calculates neighbours' values, iterates until all 
 values are minimal
'''
def compute_value():
    value = [[99 for i in grid[0]] for j in grid]
    changed = True
    while changed:
        changed = False
        for x, row in enumerate(grid):
            for y, node in enumerate(grid[0]):
                v = value[x][y]
                # goal value is zero by definition:
                if [x,y] == goal and value[x][y] != 0:
                    value[x][y] = 0
                    changed = True

                for movement in delta:
                    x2 = x + movement[0]
                    y2 = y + movement[1]
                    next_node = [x2, y2]
                    v2 = v + cost_step
                    # if [x2,y2] is a valid position:
                    if (x2 >= 0 and
                        x2 < len(grid) and
                        y2 >=0 and
                        y2 < len(grid[0]) and
                        not grid[x2][y2]):
                        # if the new value is lower than the one already stored:
                        if v2 < value[x2][y2]:
                            value[x2][y2] = v2
                            changed = True
      
    return value #make sure your function returns a grid of values as demonstrated in the previous video.

value = compute_value()
for line in value:
    print line



























