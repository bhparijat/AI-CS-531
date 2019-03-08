from copy import deepcopy
from inferences import recursive_inference
from constraints import goal_checker, constraints_violation

##-------------------------------------------------------------------------------------------------------
## sudoku solvers : backtracking search + inferences ------------------------------------------------
# Experiment with two different ways of picking a cell.
# Fixed Baseline. Use a fixed order, say, row-wise and top to bottom.
# Most Constrained Variable: Pick a slot that has the least number of values in its domain.

# assign value to cell i (domain variable), return the old list
def asgn_val(i, cell_status, val):
    res = cell_status[i][1]
    cell_status[i][0] = val
    cell_status[i][1] = []
    return res


def fixedbaseline(cell_status, n, idx, inferences):
    # fixed order of row(top --> down)
    # idx <- 81 variables

    # # check constraints and initial conditions first
    # if idx == 81:
    #     return goal_checker(cell_status), cell_status, n

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

    while idx < 80 and cell_status[idx][0] != 0:
        idx += 1

    if idx == 80:
        if cell_status[idx][1] != []:
            pass
        else:
            if goal_checker(cell_status):
                return True, deepcopy(cell_status), n
            return False, None, n

    val_dom = cell_status[idx][1]
    for val in val_dom:
        cp = deepcopy(cell_status)
        asgn_val(idx, cp, val)
        succ, res_cell, step = fixedbaseline(cp, n + 1, idx + 1, inferences)
        if succ:
            cell_status = deepcopy(res_cell)
            return True, cell_status, step
        n = step
    return False, None, n