# -----------
# User Instructions:
# 
# Modify the function search() so that it returns
# a table of values called expand. This table
# will keep track of which step each node was
# expanded.
#
# For grading purposes, please leave the return
# statement at the bottom.
# ----------

#~ grid = [[0, 0, 1, 0, 0, 0],
        #~ [0, 0, 1, 0, 0, 0],
        #~ [0, 0, 0, 0, 1, 0],
        #~ [0, 0, 1, 1, 1, 0],
        #~ [0, 0, 0, 0, 1, 0]]

grid = [[0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 1, 0]]


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
    expand = [[-1 for i in grid[0]] for j in grid]
    index = 0
    resign = False
    found = False
    

    # the loop ends if open empty (no more nodes to expand)
    while not found and not resign:
        # 1st item in the queue has the lowest g
        if not open_nodes:
            resign = True
            print 'resign'
            print 'seen:', seen
            break
        current = open_nodes.pop(0)
        pos = current[1:]
        if pos == goal:
            found = True
            print 'success'
            print current
            break
        g = current[0]
        if pos not in seen:
            seen.append(pos)
            expand[pos[1]][pos[0]] = index
            index += 1
                       
        for movement in delta:
            newcell = [pos[0] + movement[0], pos[1] + movement[1]]
            # y and x are reversed in grid
            newy = newcell[0]
            newx = newcell[1]
        
            if (newcell not in seen and
                newcell[0] >= 0 and
                newcell[0] < world_w and
                newcell[1] >= 0 and
                newcell[1] < world_h and
                not grid[newy][newx]):
                open_nodes.append([g+1] + newcell)
                index += 1
                expand[newy][newx] = index
                seen.append(newcell)
    return expand #Leave this line for grading purposes!
            

expanded = search()
for line in expanded:
    print line



