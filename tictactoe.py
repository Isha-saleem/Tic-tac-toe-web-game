
import copy
import math
X = "X"
O = "O"
EMPTY = None
def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    # Count Xs and Os to determine whose turn it is
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count <= o_count else O


def actions(board):
    # Return all empty cells as possible actions
    return {(i, j)
            for i in range(3)
            for j in range(3)
            if board[i][j] == EMPTY}


def result(board, action):
    i, j = action
    if board[i][j] is not EMPTY:
        raise Exception("Invalid action: cell already filled")

    # Deep copy the board to avoid modifying original
    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    # Check rows, columns, and diagonals
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not EMPTY:
            return board[0][i]

    # Diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]

    return None


def terminal(board):
    # Game ends if there's a winner or no empty cells
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)


def utility(board):
    # Value of a terminal board
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    return 0

def minimax(board):
    if terminal(board):
        return None

    turn = player(board)

    def max_value(state):
        if terminal(state):
            return utility(state), None
        v = -math.inf
        best_move = None
        for action in actions(state):
            min_v, _ = min_value(result(state, action))
            if min_v > v:
                v = min_v
                best_move = action
            if v == 1:
                break  # Prune if best possible outcome reached
        return v, best_move

    def min_value(state):
        if terminal(state):
            return utility(state), None
        v = math.inf
        best_move = None
        for action in actions(state):
            max_v, _ = max_value(result(state, action))
            if max_v < v:
                v = max_v
                best_move = action
            if v == -1:
                break  # Prune if best possible outcome reached
        return v, best_move

    _, move = max_value(board) if turn == X else min_value(board)
    return move
