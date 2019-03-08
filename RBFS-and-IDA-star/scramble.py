import numpy as np
#np.random.seed(0)
direction = {0:"up",1:"down",2:"left",3:"right"}
def to_new_state(grid,i,j,new_i,new_j):
	temp = grid[i][j]
	grid[i][j] = grid[new_i][new_j]
	grid[new_i][new_j] = temp
def transition(dr,i,j):
	if dr=="up":
		return i-1,j
	if dr=="down":
		return i+1,j
	if dr=="left":
		return i,j-1
	if dr=="right":
		return i,j+1
def validity_of_move(dr,i,j):
	if dr=="up" and i==0:
		return False,i,j
	if dr=="down" and i==3:
		return False,i,j
	if dr=="left" and j==0:
		return False,i,j
	if dr == "right" and j==3:
		return False,i,j
	new_i,new_j= transition(dr,i,j)
	#print("got new state")
	return True,new_i,new_j
def if_goal(new_i,new_j):
	if new_i==3 and new_j ==3:
		return True
	return False
def generate(m):
	iteration = 1
	goal_i,goal_j = 3,3
	grid = np.resize(np.array(range(1,17)),(4,4))
	#print(grid)
	i,j=3,3
	cnt=1
	while iteration<=m:
		move = np.random.randint(4,size=1)[0]
		valid,new_i,new_j = validity_of_move(direction[move],i,j)
		#print("count =",cnt, "move",move, "direction",direction[move],new_i,new_j)
		if valid == True and if_goal(new_i,new_j)==False:
			#print("going to a new state")
			to_new_state(grid,i,j,new_i,new_j)
			i = new_i
			j = new_j
			iteration = iteration + 1
		cnt = cnt + 1
	#print("scrambled grid","total_steps_taken = ",cnt)
	return grid
def generate_model(m,n):
	all_grids = []
	for i in range(n):
		all_grids.append(generate(m))
	return all_grids