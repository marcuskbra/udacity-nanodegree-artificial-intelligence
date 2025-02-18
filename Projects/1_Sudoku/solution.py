import itertools
from typing import List

from utils import *


def diagonal(_rows: List[str], _cols: List[str]) -> List[str]:
    """
    Diagonal concatenation of elements in Rows and elements in Cols
    For example: Rows = [A,B,C] and Cols = [1,2,3], should return [A1,B2,C3]
    """
    assert len(_rows) == len(_cols)
    return [
        _rows[i] + _cols[j]
        for i, j in itertools.product(range(len(_rows)), range(len(_cols)))
        if i == j
    ]


def reverse_diagonal(_rows: List[str], _cols: List[str]) -> List[str]:
    """
    Reverse diagonal concatenation of elements in Rows and elements in Cols
    For example: Rows = [A,B,C] and Cols = [1,2,3], should return [A3,B2,C1]
    """
    assert len(_rows) == len(_cols)
    return [
        rows[i] + _cols[j]
        for i, j in itertools.product(range(len(_rows)), range(len(_cols)))
        if i + j == len(_rows) - 1
    ]


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
unitlist = row_units + column_units + square_units
diagonals = [diagonal(list(rows), list(cols))]
reverse_diagonals = [reverse_diagonal(list(rows), list(cols))]

unitlist = unitlist + diagonals + reverse_diagonals

# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).

    See Also
    --------
    Pseudocode for this algorithm on github:
    https://github.com/udacity/artificial-intelligence/blob/master/Projects/1_Sudoku/pseudocode.md
    """
    # make a deep copy
    out = values.copy()

    # for each boxA in values do
    for boxA in values:
        if len(values[boxA]) != 2:
            # we only care about boxes with exactly two values
            continue

        # for each boxB of PEERS(boxA) do
        for boxB in peers[boxA]:
            # if both values[boxA] and values[boxB] exactly match and have only two feasible digits do
            if values[boxA] == values[boxB] and len(values[boxB]) == 2:
                # for each peer of INTERSECTION(PEERS(boxA), PEERS(boxB)) do
                for peer in set.intersection(peers[boxA], peers[boxB]):
                    # for each digit of values[boxA] do
                    for digit in values[boxA]:
                        # remove digit d from out[peer]
                        out[peer] = out[peer].replace(digit, '')
    return out


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        # Use the Naked Twins Strategy
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        # Failed earlier
        return False
    if all(len(values[s]) == 1 for s in boxes):
        # Solved!
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    min_unsolved, box = min((len(value), box) for box, value in values.items() if len(values[box]) > 1)

    for num in values[box]:
        copied = values.copy()
        copied[box] = num

        attempt = search(copied)
        if attempt:
            return attempt


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku

        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except Exception:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
