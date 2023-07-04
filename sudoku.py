import sys
from copy import deepcopy

alphabet = "ABCDEFGHI"
sudoku = {}
input_string = sys.argv[1]
sudoku_domain = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
for i in range(0, 81):
    row_number = int(i / 9)
    row = alphabet[row_number]
    column = str((i % 9) + 1)
    position = row + column

    sudoku[position] = input_string[i]

sudokus = {}
unassigned = []
for sudoku_tile in sudoku:
    if sudoku[sudoku_tile] == '0':
        sudokus[sudoku_tile] = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        unassigned.append(sudoku_tile)
    else:
        value = sudoku[sudoku_tile]
        sudokus[sudoku_tile] = [value]


def AC3(domain):
    constraint = []

    for unassigned_tile in unassigned:
        for i in range(1, 10):
            if str(i) != unassigned_tile[1]:
                second_variable = unassigned_tile[0] + str(i)
                constraint.append((unassigned_tile, second_variable))

        for i in range(0, 9):
            if alphabet[i] != unassigned_tile[0]:
                second_variable = alphabet[i] + unassigned_tile[1]
                constraint.append((unassigned_tile, second_variable))

        row_group_number = int(alphabet.find(unassigned_tile[0]) / 3)
        column_group_number = int((int(unassigned_tile[1]) - 1) / 3)

        for n in range(0, 3):
            for c in range(0, 3):
                if alphabet[(row_group_number * 3) + n] != unassigned_tile[0] or str(
                        (column_group_number * 3) + c + 1) != unassigned_tile[1]:
                    second_x = alphabet[(row_group_number * 3) + n] + str((column_group_number * 3) + c + 1)
                    constraint.append((unassigned_tile, second_x))

    while len(constraint) != 0:
        (xi, xj) = constraint.pop()
        if revise(domain, xi, xj):
            if len(domain[xi]) == 0:
                return False
            for n in range(1, 10):
                if str(n) != xi[1]:
                    second_x = xi[0] + str(n)
                    if second_x != xj:
                        constraint.append((second_x, xi))

            for n in range(0, 9):
                if alphabet[n] != xi[0]:
                    second_x = alphabet[n] + xi[1]
                    if second_x != xj:
                        constraint.append((second_x, xi))

            row_g_number = int(alphabet.find(xi[0]) / 3)
            column_g_number = int((int(xi[1]) - 1) / 3)

            for n in range(0, 3):
                for c in range(0, 3):
                    if alphabet[(row_g_number * 3) + n] != xi[0] or str(
                            (column_g_number * 3) + c + 1) != xi[1]:
                        second_x = alphabet[(row_g_number * 3) + n] + str((column_g_number * 3) + c + 1)
                        if second_x != xj:
                            constraint.append((second_x, xi))

    return sudokus


def revise(domain, xi, xj):
    revised = False

    for value_xi in domain[xi]:
        xj_domain = deepcopy(domain[xj])

        if value_xi in xj_domain:
            xj_domain.remove(value_xi)
        if len(xj_domain) == 0:
            domain[xi].remove(value_xi)
            revised = True

    return revised


def solved(assignment):
    for element in assignment:
        if len(assignment[element]) != 1:
            return False
    return True


def solve(sudoku_board):
    sudoku_BTS = deepcopy(sudoku_board)
    this_assignment = AC3(sudoku_board)
    if solved(this_assignment):
        sudoku_string = ""
        for element in this_assignment:
            sudoku_string += this_assignment[element][0]
        return sudoku_string + " AC3"
    result = BTS(sudoku_BTS)
    sudoku_result = ""
    for x in sudoku_BTS:
        sudoku_result += sudoku_BTS[x][0]
    return sudoku_result + " BTS"


def BTS(sudoku_BTS):
    assignment = {}
    for element in unassigned:
        assignment[element] = []
    return backtrack(assignment, sudoku_BTS, unassigned)


def complete(solving_sudoku):
    for element in solving_sudoku:
        if len(solving_sudoku[element]) != 1:
            return False
    return True


def select_unassigned_variable(solving_sudoku, unassigned_variables):
    maximum_value = 0
    for var in unassigned_variables:
        values = 0
        for i in range(1, 10):
            if str(i) != var[1]:
                second_variable = var[0] + str(i)
                if len(solving_sudoku[second_variable]) == 1:
                    values += 1

        for i in range(0, 9):
            if alphabet[i] != var[0]:
                second_variable = alphabet[i] + var[1]
                if len(solving_sudoku[second_variable]) == 1:
                    values += 1

        row_group_number = int(alphabet.find(var[0]) / 3)
        column_group_number = int((int(var[1]) - 1) / 3)

        for n in range(0, 3):
            for c in range(0, 3):
                if alphabet[(row_group_number * 3) + n] != var[0] or str(
                        (column_group_number * 3) + c + 1) != var[1]:
                    second_x = alphabet[(row_group_number * 3) + n] + str((column_group_number * 3) + c + 1)
                    if len(solving_sudoku[second_x]) == 1:
                        values += 1
        maximum_value = max(maximum_value, values)

    for var in unassigned_variables:
        values = 0
        for i in range(1, 10):
            if str(i) != var[1]:
                second_variable = var[0] + str(i)
                if len(solving_sudoku[second_variable]) == 1:
                    values += 1

        for i in range(0, 9):
            if alphabet[i] != var[0]:
                second_variable = alphabet[i] + var[1]
                if len(solving_sudoku[second_variable]) == 1:
                    values += 1

        row_group_number = int(alphabet.find(var[0]) / 3)
        column_group_number = int((int(var[1]) - 1) / 3)

        for n in range(0, 3):
            for c in range(0, 3):
                if alphabet[(row_group_number * 3) + n] != var[0] or str(
                        (column_group_number * 3) + c + 1) != var[1]:
                    second_x = alphabet[(row_group_number * 3) + n] + str((column_group_number * 3) + c + 1)
                    if len(solving_sudoku[second_x]) == 1:
                        values += 1

        if values == maximum_value:
            return var


def consistent(var, var_value, assignment):
    for i in range(1, 10):
        if str(i) != var[1]:
            second_variable = var[0] + str(i)
            if assignment[second_variable] == var_value:
                return False

    for i in range(0, 9):
        if alphabet[i] != var[0]:
            second_variable = alphabet[i] + var[1]
            if assignment[second_variable] == var_value:
                return False

    row_group_number = int(alphabet.find(var[0]) / 3)
    column_group_number = int((int(var[1]) - 1) / 3)

    for n in range(0, 3):
        for c in range(0, 3):
            if alphabet[(row_group_number * 3) + n] != var[0] or str(
                    (column_group_number * 3) + c + 1) != var[1]:
                second_x = alphabet[(row_group_number * 3) + n] + str((column_group_number * 3) + c + 1)
                if assignment[second_x] == var_value:
                    return False

    return True


def forward_check(var, value, forward):
    add = {}
    for i in range(1, 10):
        if str(i) != var[1]:
            second_variable = var[0] + str(i)
            if value in forward[second_variable]:

                add[second_variable] = value
                forward[second_variable].remove(value)

    for i in range(0, 9):
        if alphabet[i] != var[0]:
            second_variable = alphabet[i] + var[1]
            if value in forward[second_variable]:

                add[second_variable] = value
                forward[second_variable].remove(value)

    row_group_number = int(alphabet.find(var[0]) / 3)
    column_group_number = int((int(var[1]) - 1) / 3)

    for n in range(0, 3):
        for c in range(0, 3):
            if alphabet[(row_group_number * 3) + n] != var[0] or str(
                    (column_group_number * 3) + c + 1) != var[1]:
                second_x = alphabet[(row_group_number * 3) + n] + str((column_group_number * 3) + c + 1)
                if value in forward[second_x]:

                    add[second_x] = value
                    forward[second_x].remove(value)
    a = True
    for x in forward:
        if len(forward[x]) == 0:
            a = False
    for element in add:
        forward[element].append(value)
    if a:
        return True
    return False


def backtrack(assignment, sudokuBTS, unassigned_sudoku):

    if complete(assignment):
        return assignment
    var = select_unassigned_variable(sudokuBTS, unassigned_sudoku)
    unassigned_sudoku.remove(var)
    domain = []

    for x in sudokuBTS[var]:
        if forward_check(var, x, sudokuBTS):
            domain.append(x)
    for value in domain:
        if consistent(var, value, sudokuBTS):
            sudokuBTS[var] = [value]
            assignment[var].append(value)
            result = backtrack(assignment, sudokuBTS, unassigned_sudoku)
            if result is not None:
                return result
            unassigned_sudoku = []
            for element in assignment:
                if len(assignment[element]) == 0:
                    unassigned_sudoku.append(element)
                    sudokuBTS[element] = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        assignment[var].remove(value)
    return None


g = open("output.txt", "w+")
g.write(solve(sudokus))
g.close()