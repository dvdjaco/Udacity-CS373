# ----------
# User Instructions:
# 
# Create a function optimum_policy() that returns
# a grid which shows the optimum policy for robot
# motion. This means there should be an optimum
# direction associated with each navigable cell.
# 
# un-navigable cells must contain an empty string
# WITH a space, as shown in the previous video.
# Don't forget to mark the goal with a *

# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost_step = 1 # the cost associated with moving from a cell to an adjacent one.

# ----------------------------------------
# modify code below
# ----------------------------------------


'''
 use an (i,j) scan to take into account stochastic movement. Goes through
 every x,y position, calculates neighbours' values, iterates until all 
 values are minimal
'''
def optimum_policy():
    value = [[99 for i in grid[0]] for j in grid]
    policy = [[' ' for i in grid[0]] for j in grid]
    changed = True
    while changed:
        changed = False
        for x, row in enumerate(grid):
            for y, node in enumerate(grid[0]):
                v = value[x][y]
                # goal value is zero by definition:
                if [x,y] == goal and value[x][y] != 0:
                    value[x][y] = 0
                    policy[x][y] = '*'
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
                            policy[x2][y2] = delta_name[delta.index(movement) - 2]
                            changed = True
      
    return policy #make sure your function returns a grid of values as demonstrated in the previous video.
           

policy = optimum_policy()
for line in policy:
    print line
