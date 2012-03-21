# ----------
# User Instructions:
# 
# Implement the function optimum_policy2D() below.
#
# You are given a car in a grid with initial state
# init = [x-position, y-position, orientation]
# where x/y-position is its position in a given
# grid and orientation is 0-3 corresponding to 'up',
# 'left', 'down' or 'right'.
#
# Your task is to compute and return the car's optimal
# path to the position specified in `goal'; where
# the costs for each motion are as defined in `cost'.

# EXAMPLE INPUT:

# grid format:
#     0 = navigable space
#     1 = occupied space 
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]
goal = [2, 0] # final position
init = [4, 3, 0] # first 2 elements are coordinates, third is direction
cost = [2, 1, 20] # the cost field has 3 values: right turn, no turn, left turn

# EXAMPLE OUTPUT:
# calling optimum_policy2D() should return the array
# 
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]
#
# ----------


# there are four motion directions: up/left/down/right
# increasing the index in this array corresponds to
# a left turn. Decreasing is is a right turn.

forward = [[-1,  0], # go up
           [ 0, -1], # go left
           [ 1,  0], # go down
           [ 0,  1]] # do right
forward_name = ['up', 'left', 'down', 'right']

# the cost field has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']


# ----------------------------------------
# modify code below
# ----------------------------------------

def node_is_valid(x, y):
    if (x >= 0 and
        x < len(grid) and
        y >=0 and
        y < len(grid[0]) and
        grid[x][y] == 0):
        return True
    else:
        return False

def optimum_policy2D():
    value = [[[99 for i in forward] for j in grid[0]] for k in grid]
    policy = [[[99 for i in forward] for j in grid[0]] for k in grid]
    policy2D = [[' ' for i in grid[0]] for j in grid]
    changed = True
    while changed:
        changed = False
        for x, row in enumerate(value):
            for y, node in enumerate(row):
                # if we're in an obstacle, continue with the loop
                if grid[x][y]: continue
                for h, heading in enumerate(node):

                    if [x,y] == goal and policy[x][y][h] != '*':
                        value[x][y][h] = 0
                        policy[x][y][h] = '*'
                        changed = True

                    v = value[x][y][h]
                    for d, do in enumerate(action):
                        h2 = (h + do) % 4
                        x2 = x + forward[h2][0]
                        y2 = y + forward[h2][1]
 
                        if node_is_valid(x2,y2):
                            v2 = value[x2][y2][h2] + cost[d]                            
                            # if the new value is lower than the one already stored:
                            if v2 < v:
                                value[x][y][h] = v2
                                policy[x][y][h] = action_name[d]
                                changed = True

    # build the policy2D grid:
    [x, y, h] = init
    p = policy[x][y][h]
    policy2D[x][y] = p

    while p != '*':
        if p == 'L':
            h = (h + 1) % 4
        elif p == 'R':
            h = (h - 1) % 4
        x = x + forward[h][0]
        y = y + forward[h][1]
        p = policy[x][y][h]
        policy2D[x][y] = p
     
    return policy2D # Make sure your function returns the expected grid.



policy2D = optimum_policy2D()
for line in policy2D:
    print line


