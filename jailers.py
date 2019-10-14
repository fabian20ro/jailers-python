from random import getrandbits

# http://datagenetics.com/blog/december12014/index.html
from functools import reduce


def init():
    board = []
    x = getrandbits(3)
    y = getrandbits(3)
    for i in range(0, 8):
        board.append([])
        for j in range(0,8):
            board[i].append(bool(getrandbits(1)))
    return x, y, board

# nice way of iterating over every board element
def go_over(board):
    for i in range(0,8):
        for j in range(0,8):
            yield i * 8 + j, board[i][j]


# first prisoner flips one
def solve(x, y, board):
    sum = reduce(lambda x, y: x ^ y, [index for index, value in go_over(board) if value])
    sum ^= x * 8 + y
    # we flip this
    board[sum // 8][sum % 8] = not board[sum // 8][sum % 8]
    return board


# second prisoner guesses
def predict(board):
    square = reduce(lambda x, y: x ^ y, [index for index, value in go_over(board) if value])
    return square // 8, square % 8


total = 0
success = 0
fail = 0

while True:
    total += 1
    x, y, board = init()

    print(str(x) + " " + str(y) + " on " + str(board))

    changed_board = solve(x, y, board)

    myX, myY = predict(changed_board)

    print("My guess is: " + str(myX) + " " + str(myY))

    if myX == x and myY == y:
        success += 1
        print("Worked! " + str(success * 100 / total) + " of " + str(total))
    else:
        fail += 1
        print("Missed " + str(fail * 100 / total) + " of " + str(total))
