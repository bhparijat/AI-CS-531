
from matplotlib import pyplot as plt
import random
random.seed(0)
iterations = 0
g = {}
dirty = 0
position = (9,0)
suck = 100
forward = 200
turn_right = 300
turn_left = 400
turn_off = 500
walls = {}
for i in range(10):
	walls[(0,i)] = 1
for i in range(1,10):
	walls[(9,i)]=1
def not_door(position):
	if position==(0,4) or position==(5,0) or position == (4,9) or position==(9,5):
		return 0
	else:
		return 1
def if_wall_1(state,position):
	if state==0:
		return 1 if position[0]==0 or (position[0]==5 and not_door(position)) else 0
	if state==3:
		return 1 if position[0]==9 or (position[0]==4 and not_door(position)) else 0
	if state==4:
		return 1 if position[1]==9 else 0
def if_wall_2(state,position):
	if state==0:
		return 1 if position[0]==0 else 0
	if state==3:
		return 1 if position[0]==9 else 0
	if state==4:
		return 1 if position[1]==9 else 0
def perceive(grid,state):
	global position
	i = position[0]
	j = position[1]
	inside = grid[i][j]
	observation = [grid[i][j],0,0]
	
	observation[1]= if_wall_2(state,position)
	if (i==9 and j==0):
		observation[2]=1
	return observation
def FORWARD(state):
	global position
	i = position[0]
	j = position[1]
	if state==0:
		position = (i-1,j)
	if state==2 :
		position = (i,j+1)
	if state == 3:
		position =(i+1,j)
	if state == 5:
		position = (i,j+1)
	return position
def find_rule(state,percept,grid):
	global suck, forward,turn_right,turn_left,position
	action = -1
	if percept[0] == 1:
		action=suck
	elif state==0 and percept[1] == 1:
		state=1
		action = turn_right
	elif state ==0 and percept[0] == 0:
		action=forward
	elif state==1 and percept[0]  == 0:
		action= forward
		state = 2
	elif state ==2 and percept[0] == 0:
		action=turn_right
		state = 3
	elif state == 3 and percept[1] == 1:
		action= turn_left
		state = 4 
	elif state == 3 and percept[0] == 0:
		action = forward
	elif state == 4 and percept[1] == 1:
		action= turn_left
		state = 6
	elif state ==4 and percept[0] == 0:
		action = forward
		state = 5
	elif state == 5 and percept[0]  == 0:
		action = turn_left
		state = 0
	elif state == 6:
	 action = turn_left
	 state = 7
	elif state == 7:
		action = turn_off
	i = position[0]
	j = position[1]
	print("position=",position,"iterations= ",iterations,"action taken",action,"state",state)
	if action==suck:
		grid[i][j] = 0
		g[iterations] = g[iterations-1] + 1
		return position,state,0
	if action==forward:
		position = FORWARD(state)
		g[iterations] = g[iterations-1]
		return position,state,0
	if action == turn_left or action==turn_right:
		g[iterations] = g[iterations-1]
		return position,state,0
	if action == turn_off:
		g[iterations]=g[iterations-1]
		return position,state,1
def T(state,stop,grid):
	global iterations,position
	if iterations == 250 or stop==1:
		return
	iterations += 1
	percept = perceive(grid,state)
	position,state,stop = find_rule(state,percept,grid)
	T(state,stop,grid)
def  clean(grid):
	
	T(0,0,grid)

def generate_empty_ENVIRONMENT(n):
	grid = []
	for i in range(n):
		grid.append([1]*n)
	return grid
def count_clean(grid):
	clean = 0
	for i in range(10):
		for j in range(10):
			if grid[i][j]==0:
				clean +=1
	return clean
grid=generate_empty_ENVIRONMENT(10)
for i in range(10):
	print(grid[i])
g[0]= count_clean(grid)
print(g[0])
clean(grid)
print(count_clean(grid))
print(g.keys())
print(g.values())

plt.plot(g.keys(), g.values())
plt.xlabel('Number of actions taken')
plt.ylabel('Number of cleaned cells')
plt.savefig('3_wall_agent.png')
plt.gcf().clear()
