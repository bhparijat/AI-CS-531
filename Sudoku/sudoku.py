from fixedbaseline import fixedbaseline
from mcv import mcv
import time
import sys
sys.setrecursionlimit(1000000)
# how to get data from sample_problems.txt file.
#
def get_data(filename):
    with open(filename, 'r') as f:
        data = f.readlines()
        res = {}        # to make dictionary with data to store
        i = 0
        str = ""
        key = ""

        for line in data:                # make numbers in one line string
            line = line.replace("\n", "")
            line = line.replace("\t", "")
            line = line.replace(" ", "")

            if len(line.strip()) == 0:    # check if there is char in the line
                continue
            if (line.isdigit()):          # check if a line has only numbers
                str += line
            else:
                if i > 0:
                    res[i] = (str, key, len(str))
                key = line
                str = ""
                i += 1
        res[i] = (str, key, len(str))
    return res

def init_state(input):
    # return a dictionary
    res = {}
    for i in range(81):
        if input[i] == '0':
            res[i] = [0, [j for j in range(1, 10)]]
        else:
            res[i] = [int(input[i]), []]
    return res


def sudoku_solvers(initial_state, inferences):
    # check the cell is empty or not first
    cell_status = init_state(initial_state)

    fb_start = time.time()
    succ_fb, res_cell_fb, step_fb = fixedbaseline(cell_status, 0, 0, inferences)
    fb_end = time.time()

    fb_time = fb_end - fb_start

    mcv_start = time.time()
    succ_mcv, res_cell_mcv, step_mcv = mcv(cell_status, 0, inferences)
    mcv_end = time.time()

    mcv_time = mcv_end - mcv_start

    return succ_fb, step_fb, fb_time, succ_mcv, step_mcv, mcv_time


def run_experiment(samples):
    inferences = []
    # inferences.append([])
    inferences.append([1, 2])
    # inferences.append([1, 2, 3, 4])
    # inferences.append([1, 2, 3, 4, 5, 6])

    for idx, inferences in enumerate(inferences):
        for i in range(77):
            test = samples[i+1][0]
            succ_fb, step_fb, fb_time, succ_mcv, step_mcv, mcv_time = sudoku_solvers(test, inferences)
            print(i+1, step_fb, step_mcv, fb_time, mcv_time, step_fb > step_mcv, succ_fb, succ_mcv)

def main():
    filename = 'sample_problmes'
    samples = get_data(filename)
    run_experiment(samples)


if __name__ == '__main__':
    main()
