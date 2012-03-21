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

def compute_value():
    value = [[99 for i in grid[0]] for j in grid]
    seen = []
    v = 0
    open_nodes = [[v, goal[0], goal[1]]]
    while open_nodes:
        current_node = open_nodes.pop(0)
        x = current_node[1]
        y = current_node[2]
        v = current_node[0]
        value[x][y] = v
        seen.append([x, y])
        for movement in delta:
            x2 = x + movement[0]
            y2 = y + movement[1]
            next_node = [x2, y2]
            v2 = v + cost_step
            if (x2 >= 0 and
                x2 < len(grid) and
                y2 >=0 and
                y2 < len(grid[0]) and
                not grid[x2][y2] and
                next_node not in seen):
                    open_nodes.append([v2, x2, y2])
    
    return value #make sure your function returns a grid of values as demonstrated in the previous video.

value = compute_value()
for line in value:
    print line



























