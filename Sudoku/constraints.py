def row_cell(i):
    # return all other row elements
    row_num = i // 9
    return [j for j in range(row_num * 9, row_num * 9 + 9, 1) if j is not i]

def col_cell(i):
    # return all other col elements
    col_num = i % 9
    return [j * 9 + col_num for j in range(9) if j * 9 + col_num is not i]

def sub_grid(k):
    # return all other sub grid elements
    res = []
    if k in [i for j in (range(0, 3), range(9, 12), range(18, 21)) for i in j]:
        res = [i for j in (range(0, 3), range(9, 12), range(18, 21)) for i in j if i is not k]
    elif k in [i for j in (range(3, 6), range(12, 15), range(21, 24)) for i in j]:
        res = [i for j in (range(3, 6), range(12, 15), range(21, 24)) for i in j if i is not k]
    # sub grid 3
    elif k in [i for j in (range(6, 9), range(15, 18), range(24, 27)) for i in j]:
        res = [i for j in (range(6, 9), range(15, 18), range(24, 27)) for i in j if i is not k]
    # sub grid 4
    elif k in [i for j in (range(27, 30), range(36, 39), range(45, 48)) for i in j]:
        res = [i for j in (range(27, 30), range(36, 39), range(45, 48)) for i in j if i is not k]
    # sub grid 5
    elif k in [i for j in (range(30, 33), range(39, 42), range(48, 51)) for i in j]:
        res = [i for j in (range(30, 33), range(39, 42), range(48, 51)) for i in j if i is not k]
    # sub grid 6
    elif k in [i for j in (range(33, 36), range(42, 45), range(51, 54)) for i in j]:
        res = [i for j in (range(33, 36), range(42, 45), range(51, 54)) for i in j if i is not k]
    # sub grid 7
    elif k in [i for j in (range(54, 57), range(63, 66), range(72, 75)) for i in j]:
        res = [i for j in (range(54, 57), range(63, 66), range(72, 75)) for i in j if i is not k]
    # sub grid 8
    elif k in [i for j in (range(57, 60), range(66, 69), range(75, 78)) for i in j]:
        res = [i for j in (range(57, 60), range(66, 69), range(75, 78)) for i in j if i is not k]
    # sub grid 9
    elif k in [i for j in (range(60, 63), range(69, 72), range(78, 81)) for i in j]:
        res = [i for j in (range(60, 63), range(69, 72), range(78, 81)) for i in j if i is not k]
    # print(res)
    return res


# constraints 1, 2, 3 need separate checker first
# constraint 1
def check_rows(i, cell_status):
    for col_idx in row_cell(i):
        if cell_status[col_idx][0] == cell_status[i][0]:
            return False
    return True

# constraint 2
def check_cols(i, cell_status):
    for col_idx in col_cell(i):
        if cell_status[col_idx][0] == cell_status[i][0]:
            return False
    return True

# constraint 3
def check_grids(i, cell_status):
    for col_idx in sub_grid(i):
        if cell_status[col_idx][0] == cell_status[i][0]:
            return False
    return True

def constraints_violation(cell_status):

    for i in range(81):
        if cell_status[i][0] == 0 and cell_status[i][1] == []:
            return True
        if cell_status[i][0] !=0:
            if not check_rows(i, cell_status):
                return True
            if not check_cols(i, cell_status):
                return True
            if not check_grids(i, cell_status):
                return True
    return False

def check_constraints(i, cell_status):
    return check_rows(i, cell_status) and check_cols(i, cell_status) and check_grids(i, cell_status)

# all domain goal checker with constraints
def goal_checker(cell_status):
    for i in range(81):
        if cell_status[i][0] == 0:
            return False
        if not check_constraints(i, cell_status):
            return False
    return True

