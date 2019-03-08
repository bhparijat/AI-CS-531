import collections   # https://docs.python.org/3.6/library/collections.html
import itertools
from constraints import row_cell, col_cell, sub_grid

# need to implement six inferences as below
# 1. Naked Singles
# 2. Hidden Singles.
# 3. Naked Pairs.
# 4. Hidden Pairs.
# 5. Naked Triples.
# 6. Hidden Triples.

def rmv_unexpected(cell_status, i, j):
    # remove j from ith key
    if j in cell_status[i][1] and len(cell_status[i][1]) != 0:
        cell_status[i][1].remove(j)


def del_row(cell_status, i):
    val = cell_status[i][0]
    for idx in row_cell(i):
        rmv_unexpected(cell_status, idx, val)


def del_col(cell_status, i):
    val = cell_status[i][0]
    for idx in col_cell(i):
        rmv_unexpected(cell_status, idx, val)


def del_grid(cell_status, i):
    val = cell_status[i][0]
    for idx in sub_grid(i):
        rmv_unexpected(cell_status, idx, val)


def del_num(cell_status, cell_idx):
    del_row(cell_status, cell_idx)
    del_col(cell_status, cell_idx)
    del_grid(cell_status, cell_idx)


# [1. Naked Single]
# Assign to any cell a value x if it is the only value left in its domain
# I am alone in my cell and no other cells have my number.
# before = [[],[],[6,8,9],[6,7,9],[9],[7,9],[4,6,8,9],[],[]]
# target single value = 9
# after = [[],[],[6,8],[6,7,9],[],[7],[4,6,8],[],[]]
def naked_single(cell_status):
    remain_num = [len(elem[1]) for elem in cell_status.values()]
    idx_list = [idx for idx, value in enumerate(remain_num) if value == 1]

    solved= False
    for cell_idx in idx_list:
        cell_status[cell_idx][0] = cell_status[cell_idx][1][0]
        cell_status[cell_idx][1] = []
        # delete this assigned val from the other relevant cells
        del_num(cell_status, cell_idx)
        solved= True
        return solved
    return solved


# [2. Hidden Singles]
# Assign to any cell a value x if x is not in the domain of any other cell
# in that row (column or box)
# There are a pair (no other numbers) in at least two cells.
# domain_col = [[],[],[2,6,7],[2,6],[],[2,6],[2,5,6],[],[4,5]]
# target single value = 7
# after = [[],[],[7],[2,6],[],[2,6],[2,5,6],[],[4,5]]
def hidden_single(cell_status, zone_idx):
    domain = [cell_status[x][1] for x in zone_idx]
    domain_col = [item for sublist in domain for item in sublist]
    counter_val = collections.Counter(domain_col).values()
    counter_key = collections.Counter(domain_col).keys()
    counter_idx_list = [idx for idx, value in enumerate(counter_val) if value == 1]

    solved = False
    if len(counter_idx_list) > 0:
        cnt_idx = counter_idx_list[0]
        # print("cnt_idx",cnt_idx)
        val = None #
        if cnt_idx in counter_key:
            val = counter_key[cnt_idx]
        i = 0
        for sublist in domain:
            if val in sublist:
                cell_idx = zone_idx[i]
                cell_status[cell_idx][0] = val
                cell_status[cell_idx][1] = []
                del_num(cell_status, cell_idx)
                solved= True
                return solved
            i += 1

    return solved


# [3. Naked Pairs]
# An identical pair that occurs in a row, column, or box.
# Remove it from other rows, columns or boxes that share both these cells.
# Two indentical pair: only two numbers in a cell and only two cells that have the pair
# domain = [[4,6],[],[4,6],[],[],[],[3,4,6,8],[],[3,4,6,8]]
# target pair = (4,6)
# after = [[4,6],[],[4,6],[],[],[],[3,8],[],[3,8]]
def naked_pairs(cell_status, zone_idx):
    domain = [cell_status[x][1] for x in zone_idx]
    overlap = [x for n, x in enumerate(domain) if x in domain[:n]]
    pair = [val for idx, val in enumerate(overlap) if len(val) == 2]

    solved = False
    if len(pair) > 0:
        for cell_idx in zone_idx:
            if (len(cell_status[cell_idx][1]) > 0
                    and cell_status[cell_idx][1] != pair[0]):
                overlap_val = set(cell_status[cell_idx][1]) & set(pair[0])
                if len(overlap_val) > 0:
                    cell_status[cell_idx][1] = list(set(cell_status[cell_idx][1]) - set(overlap_val))
                    solved= True
    return solved


# [4. Hidden Pairs]
# A pair of numbers that occurs only in two cells in a row, column, or box.
# Eliminate the other numbers from them.
# Two identical pair with friends in only two cells: a pair with other numbers but only appear in two cells
# domain = [[],[1,7],[2,7,9],[3,4,5,7],[3,4,5,7],[3,4,7],[1,2,3,5,9],[1,3,5],[]]
# target pair = (2,9)
# after = [[4,6],[],[4,6],[],[],[],[3,8],[],[3,8]]
def hidden_pairs(cell_status, zone_idx):
    domain = [cell_status[x][1] for x in zone_idx]
    domain_col = [item for sublist in domain for item in sublist]
    pairs = list(itertools.combinations(set(domain_col), 2)) # https://docs.python.org/3/library/itertools.html

    counter = collections.Counter(domain_col)
    counter_pair_val = collections.Counter(pairs).values()
    counter_pair_key = collections.Counter(pairs).keys()
    counter_pair_idx = [idx for idx, val in enumerate(counter_pair_val) if val == 2]

    solved= False
    for counter_idx in counter_pair_idx:
        pair = counter_pair_key[counter_idx]
        if (counter[pair[0]] == 2 and counter[pair[1]] == 2):
            cell_idx = [zone_idx[idx] for idx, val in enumerate(domain) if len(set(val) & set(pair)) == 2]
            for idx in cell_idx:
                cell_status[idx][1] = list(pair)
                solved = True
        return solved
    return solved


# [5. Naked Triples]
# Three numbers that do not have any other numbers residing in the cells with them.
# Eliminate them from the rest of the cells in the same row, column, or box.
# Any composition of three numbers that do not have any other friends in any cells
# domain = [[],[5,6],[1,4,6,9],[],[6,9],[2,4,5,6],[],[5,9],[1,4,6,9]]
# target triples = (5,6,9)
# after = [[],[5,6],[1,4],[],[6,9],[2,4],[],[5,9],[1,4]]
def naked_triples(cell_status, zone_idx):
    domain = [cell_status[x][1] for x in zone_idx]
    domain_col = [item for sublist in domain for item in sublist]
    triples = list(itertools.combinations(set(domain_col), 3))

    solved = False
    for triple in triples:
        cell_idx = [zone_idx[idx] for idx, val in enumerate(domain)
                    if len(val) > 0 and len(set(val) - set(triple)) == 0]
        remain_cell_idx = set(zone_idx) - set(cell_idx)
        if len(cell_idx) > 2:
            for idx in remain_cell_idx:
                overlap_val = set(cell_status[idx][1]) and set(triple)
                if len(overlap_val) > 0:
                    cell_status[idx][1] = list(set(cell_status[idx][1]) - set(overlap_val))
                    solved = True
        return solved
    return solved


# [6. Hidden Triples]
# Three numbers with other numbers only in three cells
# domain = [[1,2,6],[1,2,5,6],[4,5,8,9],[],[1,4,6,8],[2,3,8,9],[2,3,5,6],[2,3,6],[2,3,5]]
# target triples = (4,8,9)
# after = [[1,2,6],[1,2,5,6],["4,8,9"],[],["4,8"],["8,9"],[2,3,5,6],[2,3,6],[2,3,5]]
def hidden_triples(cell_status, zone_idx):
    domain = [cell_status[x][1] for x in zone_idx]
    domain_col = [item for sublist in domain for item in sublist]
    triples = list(itertools.combinations(set(domain_col), 3))

    solved = False
    for triple in triples:
        cell_idx = [zone_idx[idx] for idx, val in enumerate(domain) if len(val) > 0 and len(set(triple) & set(val)) > 0]
        if len(cell_idx) == 3:
            for idx in cell_idx:
                overlap_val = list(set(triple) & set(cell_status[idx][1]))
                del_val = list(set(cell_status[idx][1]) - set(overlap_val))
                if len(overlap_val) > 0 and len(del_val) > 0:
                    cell_status[idx][1] = list(set(triple) & set(cell_status[idx][1]))
                    solved = True
        return solved
    return solved


# calling inferences

def forward_checking(cell_status):
    for i in range(81):
        if cell_status[i][0] != 0:
            del_row(cell_status, i)
            del_col(cell_status, i)
            del_grid(cell_status, i)


def inference_zone(cell_status, inference, zone_idx):
    if inference == 2:
        return hidden_single(cell_status, zone_idx)
    elif inference == 3:
        return naked_pairs(cell_status, zone_idx)
    elif inference == 4:
        return hidden_pairs(cell_status, zone_idx)
    elif inference == 5:
        return naked_triples(cell_status, zone_idx)
    elif inference == 6:
        return naked_triples(cell_status, zone_idx)
    else:
        exit(0)


def inference(cell_status, inference):
    if inference == 1:
        return naked_single(cell_status)
    else:
        solved= False
        for i in range(0, 10):
            zone_idx = [i] + col_cell(i)
            solved = solved or inference_zone(cell_status, inference, zone_idx)
            zone_idx = [i] + row_cell(i)
            solved = solved or inference_zone(cell_status, inference, zone_idx)
            zone_idx = [i] + sub_grid(i)
            solved = solved or inference_zone(cell_status, inference, zone_idx)
        return solved

def run_inference(cell_status, inferences, n):
    forward_checking(cell_status)
    res = []
    if 1 in inferences:
        res.append(inference(cell_status, 1))
    if 2 in inferences:
        res.append(inference(cell_status, 2))
    if 3 in inferences:
        res.append(inference(cell_status, 3))
    if 4 in inferences:
        res.append(inference(cell_status, 4))
    if 5 in inferences:
        res.append(inference(cell_status, 5))
    if 6 in inferences:
        res.append(inference(cell_status, 6))
    res = sum(res)
    return res

def recursive_inference(cell_status, inferences, n):
    if run_inference(cell_status, inferences, n-1) == 0 or n == 0:
        return False
    recursive_inference(cell_status, inferences, n-1)
