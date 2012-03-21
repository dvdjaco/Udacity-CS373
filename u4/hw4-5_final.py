# --------------
# USER INSTRUCTIONS
#
# Write a function called stochastic_value that 
# takes no input and RETURNS two grids. The
# first grid, value, should contain the computed
# value of each cell as shown in the video. The
# second grid, policy, should contain the optimum
# policy for each cell.
#
# Stay tuned for a homework help video! This should
# be available by Thursday and will be visible
# in the course content tab.
#
# Good luck! Keep learning!
#
# --------------
# GRADING NOTES
#
# We will be calling your stochastic_value function
# with several different grids and different values
# of success_prob, collision_cost, and cost_step.
# In order to be marked correct, your function must
# RETURN (it does not have to print) two grids,
# value and policy.
#
# When grading your value grid, we will compare the
# value of each cell with the true value according
# to this model. If your answer for each cell
# is sufficiently close to the correct answer
# (within 0.001), you will be marked as correct.
#
# NOTE: Please do not modify the values of grid,
# success_prob, collision_cost, or cost_step inside
# your function. Doing so could result in your
# submission being inappropriately marked as incorrect.

# -------------
# GLOBAL VARIABLES
#
# You may modify these variables for testing
# purposes, but you should only modify them here.
# Do NOT modify them inside your stochastic_value
# function.

grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]]

#~ grid = [[0, 1, 0],
        #~ [0, 0, 0]]
       
goal = [0, len(grid[0])-1] # Goal is in top right corner


delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>'] # Use these when creating your policy grid.

success_prob = 0.5                      
failure_prob = (1.0 - success_prob)/2.0 # Probability(stepping left) = prob(stepping right) = failure_prob
collision_cost = 100                    
cost_step = 1        
                     

############## INSERT/MODIFY YOUR CODE BELOW ##################
#
# You may modify the code below if you want, but remember that
# your function must...
#
# 1) ...be called stochastic_value().
# 2) ...NOT take any arguments.
# 3) ...return two grids: FIRST value and THEN policy.

def node_is_valid(x, y):
    if (x >= 0 and
        x < len(grid) and
        y >=0 and
        y < len(grid[0]) and
        grid[x][y] == 0):
        return True
    else:
        return False
        
def get_node_value(x, y, value):
    if node_is_valid(x,y):
        return value[x][y]
    else:
        return collision_cost

def stochastic_value():
    sigma = [-1, 0, 1]
    
    value = [[1000 for row in range(len(grid[0]))] for col in range(len(grid))]
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    changed = True
    while changed:
        changed = False
        for x, row in enumerate(grid):
            for y, node in enumerate(row):
                if grid[x][y] == 1: continue
                v = value[x][y]
                # goal value is zero by definition:
                if [x,y] == goal and value[x][y] != 0:
                    value[x][y] = 0
                    policy[x][y] = '*'
                    changed = True
                
                for m, movement in enumerate(delta):
                    x2 = x + movement[0]
                    y2 = y + movement[1]
                    if node_is_valid(x2, y2):
                        v_success = success_prob * get_node_value(x2, y2, value)
                        v_left = failure_prob * get_node_value(x + delta[(m + 1) % 4][0], y + delta[(m + 1) % 4][1], value)
                        v_right = failure_prob * get_node_value(x + delta[(m - 1) % 4][0], y + delta[(m - 1) % 4][1], value)
                        v2 = v_success + v_left + v_right + cost_step

                        # if the new value is lower than the one already stored:
                        if v2 < v:
                            value[x][y] = v2
                            policy[x][y] = delta_name[m]
                            changed = True    
    return value, policy

#~ [[0, 0, 0],
 #~ [0, 0, 0]]
#~ 
#~ [60.472, 37.193, 0.000]
#~ [63.503, 44.770, 37.193]
#~ ['>', '>', '*']
#~ ['>', '^', '^']

value, policy = stochastic_value()

for line in value:
    print line

for line in policy:
    print line


