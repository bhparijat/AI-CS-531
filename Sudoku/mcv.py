from heapq import heapify, heappop, heappush
from inferences import recursive_inference
from fixedbaseline import asgn_val
from constraints import constraints_violation, goal_checker
from copy import deepcopy

# Most Constrained Variable: Most Remaining Value heuristic function
# use priority queue

def get_heap(cell_status):
    pq = []
    heapify(pq)
    for i in range(81):
        if len(cell_status[i][1]) != 0:
            heappush(pq, (len(cell_status[i][1]), i))
    return pq

def mcv(cell_status, n, inferences):

    # check if it satisfy goal state condition
    if goal_checker(cell_status):
        return True, cell_status, n

    # Check if violate constraints
    if constraints_violation(cell_status):
        return False, None, n

    # Give a reasonable fixed bound on the number of search steps, say 1000, for each experiment.
    if n > 1000:
        return False, None, n

    # apply inferences here #
    recursive_inference(cell_status, inferences, 1000)
    # Check if violate constraints
    if constraints_violation(cell_status):
        return False, None, n
    # check if it satisfy goal state condition
    if goal_checker(cell_status):
        return True, deepcopy(cell_status), n

    pq = get_heap(cell_status)

    if len(pq) == 0:
        return False, None, n

    _, idx = heappop(pq)

    val_dom = cell_status[idx][1]
    for val in val_dom:
        cp = deepcopy(cell_status)
        asgn_val(idx, cp, val)
        succ, res_cell, step = mcv(cp, n + 1, inferences)
        if succ:
            cell_status = deepcopy(res_cell)
            return True, cell_status, step
        n = step
    return False, None, n