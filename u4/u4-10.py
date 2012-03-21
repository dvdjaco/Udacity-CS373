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

grid = [[0, 0, 1, 0, 0, 0],
        [1, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0]]

#~ grid = [[0, 1, 0, 0, 0],
        #~ [0, 1, 0, 0, 0],
        #~ [0, 0, 0, 1, 0],
        #~ [0, 1, 1, 1, 0],
        #~ [0, 0, 0, 1, 0]]


init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1] # Make sure that the goal definition stays in the function.

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost = 1

            
def neighbors(expand, pos):
    '''returns a list with [g, x, y] of the nearest neighbors of pos.
    Returns values for valid positions only
    '''
    g_list = []
    for movement in delta:
        x = pos[0] + movement[0]
        y = pos[1] + movement[1]
        if x < len(grid) and y < len(grid[0]):
            g = expand[x][y]
            if g != -1:
                g_list.append([g, x, y])
    return g_list


def search():
    open_nodes = []
    open_nodes.append([0] + init)
    seen = []
    world_w = len(grid)
    world_h = len(grid[0])
    action = [[-1 for i in grid[0]] for j in grid]
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
                        open_nodes.append([g+1] + newcell)
                        action[newx][newy] = delta_name[delta.index(movement)]
                        #~ print newx, newy, action[newx][newy]
                        seen.append(newcell)
    for move in action:
        print move
    print ''
    path = [['' for i in grid[0]] for j in grid]
    if found:
        path[goal[0]][goal[1]] = '*'
        pos = goal[:]
        backpos = goal[:]
        while pos != init:
            movement = delta[delta_name.index(action[pos[0]][pos[1]])]
            backpos[0] = pos[0] - movement[0]
            backpos[1] = pos[1] - movement[1]
            print pos, backpos, movement
            path[backpos[0]][backpos[1]] = action[pos[0]][pos[1]]
            pos = backpos[:]
    return path

path = search()
for line in path:
    print line

















