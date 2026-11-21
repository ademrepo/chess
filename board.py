# Board constants and helpers shared by the whole project.
# Coordinates: position = (x, y). (0, 0) is the top-left square (a8 in chess notation),
# x grows to the right (column), y grows downwards (row).

BOARD_SIZE = 8
NB_SQUARES = BOARD_SIZE * BOARD_SIZE   # 64 = maximum fitness
NB_GENES = NB_SQUARES - 1              # 63 moves to visit the 63 other squares
NB_MOVES = 8                           # a knight has 8 possible moves

# The 8 directions, numbered clockwise starting from "up-right" (Figure 1 of the statement):
#   1: up-right   2: right-up   3: right-down   4: down-right
#   5: down-left  6: left-down  7: left-up      8: up-left
MOVES = {
    1: (1, -2),
    2: (2, -1),
    3: (2, 1),
    4: (1, 2),
    5: (-1, 2),
    6: (-2, 1),
    7: (-2, -1),
    8: (-1, -2),
}


def on_board(pos):
    # True if the position is inside the 8x8 chessboard.
    return 0 <= pos[0] < BOARD_SIZE and 0 <= pos[1] < BOARD_SIZE


def square_name(pos):
    # (0, 0) -> "a8", (7, 7) -> "h1" (chess notation, only used for display).
    return "abcdefgh"[pos[0]] + str(BOARD_SIZE - pos[1])
