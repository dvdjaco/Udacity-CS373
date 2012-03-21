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

def optimum_policy():
    value = [[99 for i in grid[0]] for j in grid]
    policy = [[' ' for i in grid[0]] for j in grid]
    seen = []
    v = 0
    # create a list of inverted movements
    r_delta = [[-1 * m for m in movement] for movement in delta]
    # open nodes is a queue of nodes to expand
    open_nodes = [[v, goal[0], goal[1]]]
    while open_nodes:
        # remove the 1st node of the list so it is always the one with
        # lowest v (depth)
        current_node = open_nodes.pop(0)
        x = current_node[1]
        y = current_node[2]
        v = current_node[0]
        value[x][y] = v
        # keep a list of nodes already expanded:
        seen.append([x, y])
        # mark goal
        if current_node[1:] == goal:
            policy[x][y] = '*'
        for movement in delta:
            x2 = x + movement[0]
            y2 = y + movement[1]
            next_node = [x2, y2]
            v2 = v + cost_step
            # TODO: check whether these can be added several times (add 
            # them to "seen" or check open_nodes before append?
            if (x2 >= 0 and
                x2 < len(grid) and
                y2 >=0 and
                y2 < len(grid[0]) and
                not grid[x2][y2] and
                next_node not in seen):
                    open_nodes.append([v2, x2, y2])
                    # subtract 2 from the index to get the opposite direction
                    policy[x2][y2] = delta_name[delta.index(movement) - 2]
    return policy # Make sure your function returns the expected grid.

optimum_policy()
