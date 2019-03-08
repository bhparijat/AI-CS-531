import numpy as np
import scramble
import math
import time
import sys
sys.setrecursionlimit(1000000)
loc = {}
record = {}
INF = 100000000
G = {}
F = {}
R = {}
number_of_nodes = 1
visitted = {}
encode = {1:"0001",2:"0010",3:"0011",4:"0100",5:"0101",6:"0110",7:"0111",8:"1000",
9:"1001",10:"1010",11:"1011",12:"1100",13:"1101",14:"1110",15:"1111",16:"0000"}
def manhattan_distance():
	global loc
	for i in range(1,17):
		row = math.floor((i-1)/4)
		col = math.floor((i-1)%4)
		loc[i]=(row,col)
def get_manhattan_distance(grid):
	d = 0
	for i in range(4):
		for j in range(4):
			d = d + abs(i-loc[grid[i][j]][0])+ abs(j-loc[grid[i][j]][1])
	return d
def get_unmatched_cells(grid):
	c = 0
	for i in range(4):
		for j in range(4):
			if grid[i][j]!=(i*4+j+1):
				c = c + 1
	return c
def get_heuristic(grid,flag):
	if flag==0:
		return get_manhattan_distance(grid)
	else:
		return get_unmatched_cells(grid)
def position_of_blank(grid):
	for i in range(4):
		for j in range(4):
			if grid[i][j] == 16:
				return i,j
def is_goal(grid):
	c = 1
	for i in range(4):
		for j in range(4):
			if grid[i][j]!=c:
				return False
			c = c + 1
	#print("matched",grid)
	return True
def get_valid_actions(i,j):
	valid_actions = []
	if i!=0:
		valid_actions.append("up")
	if i!=3:
		valid_actions.append("down")
	if j!=0:
		valid_actions.append("left")
	if j!=3:
		valid_actions.append("right")
	return valid_actions
def cycle(child,solution):
	for sol in solution:
		if np.array_equal(child,sol):
			return True
	return False
def get_children(curr_state,x,y,actions,solution):
	children = []
	positions = []
	#print("solutions",solution)
	for action in actions:
		child = np.copy(curr_state)
		#print("child is",child)
		child_x,child_y = scramble.transition(action,x,y)
		scramble.to_new_state(child,x,y,child_x,child_y)
		if cycle(np.array(child),solution)==False:
			children.append(child)
			positions.append((child_x,child_y))
	return children,positions

def perform_IDA(solution,g,h,x,y,heuristic):
	global number_of_nodes
	state = solution[-1]
	f = g + get_heuristic(state,heuristic)
	if f > h:
		return f,solution
	if x==3 and y==3 and is_goal(state):
		return -1,solution
	mn = INF
	actions = get_valid_actions(x,y)
	children,positions = get_children(state,x,y,actions,solution)
	for i,child in enumerate(children):
		number_of_nodes = number_of_nodes + 1
		solution.append(np.array(child))
		x,y = positions[i]
		new_threshold,solution = perform_IDA(solution,g+1,h,x,y,heuristic)
		if new_threshold == -1:
			return -1,solution
		if new_threshold< mn:
			mn = new_threshold
		solution.pop()
	return mn,solution
def compute_ida(m,heuristic):
	global number_of_nodes
	grids = scramble.generate_model(m,10)
	record[m]=[]
	#print(grids)
	for grid in grids:
		#print(grid)
		h = get_heuristic(grid,heuristic)
		f = h
		iteration = 1
		solution = [np.array(grid)]
		start_time = time.clock()
		number_of_nodes= 1
		x,y = position_of_blank(grid)
		while number_of_nodes<=100000:
			new_threshold,solution= perform_IDA(solution,0,f,x,y,heuristic)
			if new_threshold == -1:
				record[m].append((number_of_nodes,time.clock()-start_time,len(solution)))
				break
			f = new_threshold
			#iteration = iteration + 1
		# 	if iteration%100 == 0 or m==40 or m==50:
		# 		print("number of iterations",iteration,new_threshold,number_of_nodes)
		# #print("solution",record)
manhattan_distance()
print("IDA","m","heuristic","avg. number_of_nodes","avg. time_taken","avg. length of solution")
dta = []
for heuristic in [0,1]:
	xx = [10,20,30,40,50]
	yy1 = []
	yy2 = []
	yy3 = []
	for i in [10,20,30,40,50]:
	
		compute_ida(i,0)
		#print(i,'\n',record[i])
		lm = record[i]
		p , q,r =0,0,0
		for j in range(10):
			p = p + lm[j][0]
			q = q + lm[j][1]
			r = r + lm[j][2]
		p = p/10
		q = q/10
		r = r/10
		yy1.append(p)
		yy2.append(q)
		yy3.append(r)
		record[i]=(p,q,r)
		print("IDA",i,heuristic,record[i])

	dta.append([xx,yy1,yy2,yy3])

def encode_state(state,recursive=None):
	global encode
	encoding = ""
	# if recursive==0:
	# 	print("called during recursive")
	# elif recursive==1:
	# 	print("called during getting bests")
	# print("to be encoded",state)
	for i in range(4):
		for j in range(4):
			encoding = encoding + encode[state[i][j]]
	return encoding
def get_the_two(children):
	best_string = ""
	second_best_string= ""
	for i,child in enumerate(children):
		if i==0:
			best_string= encode_state(child,1)
			continue
		if i==1:
			second_best_string = encode_state(child,1)
			if F[second_best_string]<F[best_string]:
				best_string,second_best_string = second_best_string,best_string
			continue
		st = encode_state(child,1)
		value = F[st]
		value1 = F[best_string]
		value2 = F[second_best_string]
		if value<=value1:
			best_string,second_best_string = st,best_string
		elif value<value2:
			second_best_string = st
	best = None
	second_best = None
	for child in children:
		st = encode_state(child,1)
		if st == best_string:
			best = child
		elif st == second_best_string:
			second_best = child
	return best,second_best
def get_tile_position(state):
	for i in range(4):
		for j in range(4):
			if state[i][j]== 16:
				return i,j
	return None
def g_state(parent,child):
	global G
	if child not in G:
		G[child]= INF
	# if parent not in G:
	# 	print("not in G")
	G[child] = min(G[child],G[parent]+1)
	return G[child]
def h_state(child,flag):
	if flag == 0:
		return get_manhattan_distance(child)
	else:
		return get_unmatched_cells(child)
def print_children(children,current_fvalues):
	#print("children for current state are")
	for i,child in enumerate(children):
		print(child,'\n',current_fvalues[i])
def perform_RBFS(curr_state,parent,f_limit,flag,depth):

	#print("current state is",'\n',curr_state)
	global G,F,visitted,R,gf,number_of_nodes
	if is_goal(curr_state)==True:
		#print("Got to a goal state")
		return F[encode_state(curr_state)],True,depth
	x,y = get_tile_position(curr_state)
	actions = get_valid_actions(x,y)
	children = []
	positions = []
	dep = 0
	for action in actions:
		child = np.copy(curr_state)
		child_x,child_y = scramble.transition(action,x,y)
		scramble.to_new_state(child,x,y,child_x,child_y)
		#print("checking for duplicate")
		if encode_state(child) in visitted.keys():
			#print("Gotch duplicate")
			continue
		#print("without duplicate")
		children.append(child)
		number_of_nodes = number_of_nodes + 1
		visitted[encode_state(child)]=1
		positions.append((child_x,child_y))
	if len(children)==0:
		#print("******************************************************88888888")
		return INF,False,INF
	current_fvalues = []
	for child in children:
		bit_child = encode_state(child)
		bit_parent = encode_state(curr_state)
		current_fvalue = g_state(bit_parent,bit_child)+ h_state(child,flag)
		if current_fvalue < F[bit_parent]:
			F[bit_child] = max(F[bit_parent],current_fvalue)
		else:
			F[bit_child] = current_fvalue
		current_fvalues.append(current_fvalue)
	#print_children(children,current_fvalues)
	best,second_best = get_the_two(children)
	# if second_best is None and best is None:
	# 	print("Both are None")
	if second_best is None:
		return perform_RBFS(best,curr_state,f_limit,flag,depth+1)
		#print("here second_best is NOne")
		#second_best = best
	#print("The two best ones are",'\n',best,'\n',second_best)
	
	exit = False
	while(F[encode_state(best)]<=f_limit and F[encode_state(best)]<INF and exit==False):
		alternative = min(f_limit,F[encode_state(second_best,0)])
		F[encode_state(best)],exit,dep=perform_RBFS(best,curr_state,alternative,flag,depth+1)
		best,second_best = get_the_two(children)
		R[encode_state(best)]=exit
	return F[encode_state(best)],exit,dep		
rbfs_solution = {}
def compute_rbfs(heuristic):
	global G,F,R,visitted,number_of_nodes
	print("RBFS","m","heuristic","avg. number_of_nodes","avg. time_taken","avg. length of solution")
	rbf_dta = []
	for h in heuristic:
		xx = [10,20,30,40,50]
		yy1 = []
		yy2 = []
		yy3 = []
		for m in [10,20,30,40,50]:
			rbfs_solution[m] = []
			
			c = 0
			while c<10:
				grid = scramble.generate_model(m,1)[0]
				G = {}
				F = {}
				R = {}
				number_of_nodes = 1
				visitted = {}
				#print(grid)
				#print(encode_state(grid))
				G[encode_state(grid)]=0
				F[encode_state(grid)]=h_state(grid,h)
				#print("h_state grid",h_state(grid,h))
				visitted[encode_state(grid)]=1
				start_time = time.clock()
				solution,_,dep = perform_RBFS(grid,None,INF,h,0)
				if dep==INF:
					continue
				c = c+1
				rbfs_solution[m].append((number_of_nodes,time.clock()-start_time,dep))
				#print(solution,number_of_nodes)
			lm = rbfs_solution[m]
			p , q,r =0,0,0
			for j in range(10):
				p = p + lm[j][0]
				q = q + lm[j][1]
				r = r + lm[j][2]
			p=p/10
			q=q/10
			r=r/10
			yy1.append(p)
			yy2.append(q)
			yy3.append(r)
			rbfs_solution[m]=(p,q,r)
		
			print("RBFS",m,h,rbfs_solution[m])
		rbf_dta.append([xx,yy1,yy2,yy3])
compute_rbfs([0,1])
