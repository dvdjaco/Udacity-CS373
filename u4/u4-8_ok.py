# ----------
# User Instructions:
# 
# Define a function, search() that takes no input
# and returns a list
# in the form of [optimal path length, x, y]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

# Grid format:
#   0 = Navigable space
#   1 = Occupied space

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1] # Make sure that the goal definition stays in the function.

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost = 1

def search():
    open_nodes = []
    open_nodes.append([0] + init)
    seen = []
    world_w = len(grid)
    world_h = len(grid[0])

    # the loop ends if open empty (no more nodes to expand)
    while open_nodes:
        print open_nodes
        # 1st item in the queue has the lowest g
        current = open_nodes.pop(0)
        pos = current[1:]
        if pos == goal:
            return current
        g = current[0]
        if pos not in seen:
            seen.append(pos)
                       
        for movement in delta:
            newcell = [pos[0] + movement[0], pos[1] + movement[1]]
            newx = newcell[0]
            newy = newcell[1]
        
            if (newcell not in seen and
                newcell[0] >= 0 and
                newcell[0] < world_w and
                newcell[1] >= 0 and
                newcell[1] < world_h and
                not grid[newx][newy]):
                open_nodes.append([g + cost] + newcell)
                seen.append(newcell)
    return 'fail'
            

print search()
