# ----------
# User Instructions:
#
# Modify the the search function so that it returns
# a shortest path as follows:
# 
# [['>', 'v', ' ', ' ', ' ', ' '],
#  [' ', '>', '>', '>', '>', 'v'],
#  [' ', ' ', ' ', ' ', ' ', 'v'],
#  [' ', ' ', ' ', ' ', ' ', 'v'],
#  [' ', ' ', ' ', ' ', ' ', '*']]
#
# Where '>', '<', '^', and 'v' refer to right, left, 
# up, and down motions. NOTE: the 'v' should be 
# lowercase.
#
# Your function should be able to do this for any
# provided grid, not just the sample grid below.
# ----------


# Sample Test case
grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost = 1

# ----------------------------------------
# modify code below
# ----------------------------------------

def search():
    open_nodes = []
    open_nodes.append([0] + init)
    seen = []
    world_w = len(grid)
    world_h = len(grid[0])
    expand = [[-1 for i in grid[0]] for j in grid]
    resign = False
    found = False
    

    # the loop ends if open empty (no more nodes to expand)
    while not found and not resign:
        # 1st item in the queue has the lowest g
        if not open_nodes:
            resign = True
            print 'resign'
            print 'seen:', seen
        else:
            current = open_nodes.pop(0)
            pos = current[1:]
            if pos == goal:
                found = True
                print 'success:', current
            else:
                g = current[0]
                if pos not in seen:
                    seen.append(pos)
                    expand[pos[1]][pos[0]] = g
                               
                for movement in delta:
                    newcell = [pos[0] + movement[0], pos[1] + movement[1]]
                    newy = newcell[0]
                    newx = newcell[1]
                
                    if (newcell not in seen and
                        newcell[0] >= 0 and
                        newcell[0] < world_w and
                        newcell[1] >= 0 and
                        newcell[1] < world_h and
                        not grid[newy][newx]):
                        open_nodes.append([g+1] + newcell)
                        expand[newy][newx] = g+1
                        seen.append(newcell)
    path = [['' for i in grid[0]] for j in grid]
    if found:
        path[goal[0]][goal[1]] = '*'
        pos = goal
        while pos != init:
            #~ g_neighbors = neighbors(expand, pos)            
            g_list = []
            for movement in delta:
                x = pos[0] + movement[0]
                y = pos[1] + movement[1]
                if x < len(grid) and y < len(grid[0]):
                    g = expand[x][y]
                    if g != -1:
                        g_list.append([g, x, y])
            g_neighbors = g_list
            backpos = min(g_neighbors)
            movement = []
            movement.append(pos[0] - backpos[1])
            movement.append(pos[1] - backpos[2])
            symbol = delta_name[delta.index(movement)]
            pos = backpos[1:]
            path[pos[0]][pos[1]] = symbol
    for line in path:
      print line
    return path

search()
