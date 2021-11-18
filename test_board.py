board = []
isLeftRight = True
for i in range(0, 10):
    temp = []
    for j in range(0, 10):
        temp.append(100 - (i * 10 + j))
    if (not isLeftRight):
        temp.reverse()
    board.append(temp)
    print(temp)
    isLeftRight = not isLeftRight
# print(board)