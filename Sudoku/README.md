# PA3_Sudoku_AI
## CS531 AI Programming Assignment3

In this assignment you will be implementing a solver for SuDoKu. Figure 6.4 in the book gives an example and there are plenty of pages on the web with examples.

SuDoKu is a constraint satisfaction problem, with all-diff constraints on each row, column, and box. The variables are cells and the values are numbers 1-9. You are going to implement backtracking search with constraint propagation. It maintains all possible candidate values, i.e., the current domain, for each cell after each assignment. The baseline system implements forward checking which removes candidate values for a variable when it violate some constraints, given the currently assigned values for other variables.

The search begins by storing all possible values for each of the empty spots. Then it does constraint propagation through domain-specific inference rules. When the constraint propagation converges, then: 
- if no candidates left for some cell, then backtrack from the current state. 
- else pick a cell, and assign it a consistent value (keep other choices of values as options to backtrack to; there is no need to backtrack over the cell choice since all cells need to be filled).

Experiment with two different ways of picking a cell.

- Fixed  Baseline. Use a fixed order, say, row-wise and top to bottom.
- Most Constrained Variable: Pick a slot that has the least number of values in its domain.

 Apply the following inference rules in the given priority order, i.e., keep applying rule 1 as long as it applies. When it does not, apply rule 2, and go back to rule 1, and so on. The constraint propagation terminates when no rule is applicable, at which point a search action (assignment) is taken. At any search state, the program maintains the set of assignments made in that state, and the candidate numbers available in all other cells. Here are the inference rules to be tried in that sequence.  

- Naked Singles
- Hidden Singles.
- Naked Pairs.
- Hidden Pairs.
- Naked Triples.
- Hidden Triples.

Please refer to this [page](http://www.sudokuessentials.com/sudoku_tips.html) for an explanation of these rules. Conduct experiments with the following subsets of rules.

- No inference
- Naked and Hidden Singles.
- Naked and Hidden Singles and Pairs
- Naked and Hidden Singles, Pairs, and Triples.
- Give a reasonable fixed bound on the number of search steps, say 1000, for each experiment.

There is a set of sample problems [here](http://web.engr.oregonstate.edu/~tadepall/cs531/18/sudoku-problems.txt). The numbers are written in the file row-wise, with 0 representing empty slots. Each team should try to solve all the problems, starting with the easy ones. Report the number of problems solved and the number of backtracks with each problem. Experts appear to grade the problems by the complexity of rules needed to solve them without backtracking. Is this conjecture roughly correct? Grade each problem, by the set of rules used in solving it. Report also the average number of filled-in numbers (in the beginning) for each of these types of problems. Would this accurately reflect the difficulty of the problem?

Report your results in the form of a mini-paper as you did for the other two assignments. Give the pseudocode for the algorithm. Discuss how the results vary with the difficulty of the problems, and the effectiveness of the most-constrained variable heuristic compared to fixed selection. Also report on the effectiveness of rule subsets in reducing the search. Is the number of backtracks reduced by increased inference rules? What about the total time for solving the puzzles? Please feel free to include any other observations.

