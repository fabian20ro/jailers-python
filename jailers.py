# See http://datagenetics.com/blog/december12014/index.html for the problem

from random import randrange
from functools import reduce

board_size_in_bits = 3 # 3 means 2^3, meaning 8x8
# board_size_in_bits = 4 # 4 means 2^4, meaning 16x16

total_runs = 1000 # how many times the prisoners try to escape


def init(board_size_in_bits):

    board_size = pow(2, board_size_in_bits)

    # initialize the random board
    board = []
    for i in range(0, board_size):
        board.append([])
        for j in range(0, board_size):
            board[i].append(bool(randrange(0, 2)))

    # pick a square
    x = randrange(0, board_size)
    y = randrange(0, board_size)

    return x, y, board


# nice way of iterating over every board element
def go_over(board):
    board_size = len(board[0])
    for i in range(0, board_size):
        for j in range(0, board_size):
            yield i * board_size + j, board[i][j]


# first prisoner flips one
def solve(x, y, board):
    board_size = len(board[0])
    sum = reduce(lambda x, y: x ^ y, [index for index, value in go_over(board) if value], 0)
    sum ^= x * board_size + y
    # we flip this
    board[sum // board_size][sum % board_size] = not board[sum // board_size][sum % board_size]
    return board


# second prisoner guesses
def predict(board):
    board_size = len(board[0])
    square = reduce(lambda x, y: x ^ y, [index for index, value in go_over(board) if value], 0)
    return square // board_size, square % board_size


successes = 0

for count in range(0, total_runs):

    x, y, board = init(board_size_in_bits)
    print(str(count + 1) + ": " + str(x) + " " + str(y) + " on " + str(board))

    # first prisoner flips one
    changed_board = solve(x, y, board)

    # second prisoner says which one was flipped
    myX, myY = predict(changed_board)

    print("My guess is: " + str(myX) + " " + str(myY))

    if myX == x and myY == y:
        successes += 1

print("Worked! " + str(successes * 100 / total_runs) + ": " + str(successes) + " of " + str(total_runs))

