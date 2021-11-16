from board_logic import *
import numpy as np

def is_win(board):
    """
    Transposition to check rows, then columns and return True or False. If return True then finish game.
    Push_list was created for control game logic and current events. It's a copy of current situation in GUI board.
    """
    for new_board in [board, np.transpose(board)]:
        result = check_rows(new_board)
        if result:
            return result
    # Check diagonals and return True or False
    return check_diagonals(board)


def check_rows(board, optional={"-"}):
    # Iterates through board and if
    for row in board:
        # Check if exists only one shape(X or O) in row and symbol can't be "-".
        # Symbol "-" represents empty cell in the board of the game.
        if len(set(row)) == 1 and set(row) != optional:
            return True
    return False


def check_diagonals(board, optional={"-"}):
    # Check diagonal ((0,0), (1,1), (2,2)....etc)
    check_one = set([board[i][i] for i in range(len(board))])
    # Check if exists only one shape(X or O) in first diagonal and symbol there can't be "-".
    # Symbol "-" represents empty cell in the board of the game.
    if len(check_one) == 1 and check_one != optional:
        return True
    # check diagonal (from last column in first row to last row and first column)
    check_two = set([board[i][len(board) - i - 1] for i in range(len(board))])
    # Check if exists only one shape(X or O) in second diagonal and symbol there can't be "-".
    # Symbol "-" represents empty cell in the board of the game.
    if len(check_two) == 1 and check_two != optional:
        return True
    return False


def is_draw(board, optional="-"):
    """Checks existing empty cells. If not, then return True and finish game."""
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == optional:
                return False
    return True