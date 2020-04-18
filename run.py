from pulp import *

# ask user for number of queens to work with
nr_queens = int(input("Hello!\nHow many queens do you want us to position on a board of the same size?\n"))

# create a new linear problem
prob = LpProblem("Queens", LpMinimize)
# create a list of strings that goes from 1 to the number of queens, for enumeration purposes
Sequence = []
for i in range(nr_queens):
    Sequence.append(str(i+1))
# print(Sequence)  #prints the enumeration of the board


# initialize a rows and a columns lists, with the enumeration
Rows = Sequence
Cols = Sequence

# initialize a list of the diagonals
Diagonals = []

# loop through the the initial positions
for i in range(nr_queens):
    # initialize empty lists for the 4 directions we record diagonals with
    # the diagonals starting on the left always move towards the right, and vice versa
    #                     arrayLeftUp->              <-arrayRightUp
    #                     ----------------------------------------
    #    arrayLeftDown   |                                        |  arrayRightDown
    #        |           |                                        |        |
    #        V           |                                        |        V
    #                    |                                        |
    #                    |                                        |
    #                     ----------------------------------------
    arrayLeftUp = []
    arrayRightUp = []
    arrayLeftDown = []
    arrayRightDown = []
    # add to each list(diagonal) the next element of the diagonal
    for j in range(nr_queens - i):
        arrayLeftUp += [(Rows[i+j],Cols[j])]
        arrayRightUp += [(Rows[nr_queens-1-(i+j)],Cols[j])]
        arrayLeftDown += [(Rows[j],Cols[i+j])]
        arrayRightDown += [(Rows[nr_queens-1-j],Cols[i+j])]
    # add the lists (diagonals) to the list of diagonals
    Diagonals.append(arrayLeftUp)
    Diagonals.append(arrayLeftDown)
    Diagonals.append(arrayRightUp)
    Diagonals.append(arrayRightDown)


# print diagonals function
# for d in Diagonals:
#     print(d)

# initialize the dictionary, representing the board
choices = LpVariable.dicts("Choice", (Rows, Cols), 0, 1, LpInteger)

# add constraint: only 1 queen per row
for r in Rows:
    prob += lpSum([choices[r][c] for c in Cols]) == 1, ""

# add constraint: only 1 queen per column
for c in Cols:
    prob += lpSum([choices[r][c] for r in Rows]) == 1, ""

# add constraint: at most 1 queen per diagonal
for d in Diagonals:
    prob += lpSum(choices[r][c] for (r,c) in d) <= 1, ""

# print(prob)  #print the detail description - definition and constraints

# solve the problem
prob.solve()

# print("Status:", LpStatus[prob.status]) #print the status of the problem

# output
solution = ""
# if there is a solution, construct a board to visualize it
if LpStatus[prob.status] == "Optimal":
    for r in Rows:
        solution+="|"
        for c in Cols:
            if value(choices[r][c]) == 1:
                solution+=" * "
            else:
                solution+="   "
            solution+="|"
        solution+="\n"
else:
    # else tell the user there was no solution found
    solution+="An optional solution was not found :("
# print the result
print(solution)