import collections
import sys
brd = "........."


def win(b):
    constraints = []
    constraints.append(b[0:3])
    constraints.append(b[3:6])
    constraints.append(b[6:9])
    constraints.append(b[0] + b[3] + b[6])
    constraints.append(b[1] + b[4] + b[7])
    constraints.append(b[2] + b[5] + b[8])
    constraints.append(b[0] + b[4] + b[8])
    constraints.append(b[2] + b[4] + b[6])
    for each in constraints:
        if each.count("X") is 3:
            return "X"
        elif each.count("O") is 3:
            return "O"
    if "." not in b:
        return "DRAW"
    return False


def get_children(b):
    xamount = b.count("X")
    oamount = b.count("O")

    if xamount > oamount:
        return placeo(b)
    else:
        return placex(b)


def placex(b):
    possible = []
    for i in range(0, 9):
        if b[i] is ".":
            copy = b
            copy = copy[0:i] + "X" + copy[i + 1:]
            possible.append(copy)
    return possible


def placeo(b):
    possible = []
    for i in range(0, 9):
        if b[i] is ".":
            copy = b
            copy = copy[0:i] + "O" + copy[i + 1:]
            possible.append(copy)
    return possible


def bfs(board):
    all = set()
    visited = set()
    visited.add(board)
    unexplored = collections.deque()
    unexplored.append((board, 0))
    while len(unexplored) > 0:
        node = unexplored.pop()
        visited.add(node[0])
        if win(node[0]) is not False:
            all.add((node, win(node[0])))
        else:
            for eachChild in get_children(node[0]):
                if eachChild not in visited:
                    unexplored.appendleft((eachChild, node[1] + 1))

    return all


def bfs2(board):
    count = 0

    unexplored = collections.deque()
    unexplored.append(board)
    while len(unexplored) > 0:
        node = unexplored.pop()

        if win(node) is not False:
            count += 1
        else:
            for eachChild in get_children(node):
                unexplored.appendleft(eachChild)

    return count


def stats():
    a = bfs(brd)
    print(len(a))
    fivecount = 0
    sixcount = 0
    sevencount = 0
    eightcount = 0
    ninecount = 0
    drawcount = 0
    for each in a:
        result = each[1]
        if result is "DRAW":
            drawcount += 1
        else:
            count = each[0][1]
            if count is 5:
                fivecount += 1
            if count is 6:
                sixcount += 1
            if count is 7:
                sevencount += 1
            if count is 8:
                eightcount += 1
            if count is 9:
                ninecount += 1
    print(fivecount, sixcount, sevencount, eightcount, ninecount, drawcount)
    a = bfs2(brd)
    print(a)






def get_index_children(b):
    return placeindex(b)

def placeindex(b):
    possible = []
    for i in range(0, 9):
        if b[i] is ".":
            possible.append(i)
    return possible


def printBoard(b):
    count = 0
    print("---")
    for each in b:
        if count % 3 == 0 and count is not 0:
            print()
        print(each, end='')
        count += 1
    print("\n---")

user_symbol = None
cpu_symbol = None




def minimax(board, turn):
    result = win(board)
    if result is "X":
        return {-1:1}
    elif result is "O":
        return {-1:-1}
    elif result is "DRAW":
        return {-1:0}

    if turn is 0:
        tkn = cpu_symbol
    else:
        tkn = user_symbol

    res = {}
    for move in get_index_children(board):
        new_board = board[0:move] + tkn + board[move+1:]
        if turn is 0:
            mmx = minimax(new_board, turn+1)
        if turn is 1:
            mmx = minimax(new_board, turn-1)
        boardEval = min(mmx.values()) if tkn == 'X' else max(mmx.values())
        res[move] = boardEval

    return res


def game():
    global user_symbol
    global cpu_symbol
    start_board = brd
    printBoard(start_board)
    print()
    if "X" in start_board or "O" in start_board:
        if start_board.count("X") == start_board.count("O"):
            user_symbol = "O"
            cpu_symbol = "X"
        else:
            cpu_symbol = "O"
            user_symbol = "X"
    else:
        user_symbol = str.upper(input("X or O?  "))
    print("You are " + str(user_symbol))
    cpu_symbol = None
    if "X" in user_symbol:
        cpu_symbol = "O"
    else:
        cpu_symbol = "X"
    print("I am " + str(cpu_symbol))
    turn = None
    print()
    if start_board.count("X") == start_board.count("O"):
        if cpu_symbol is "X":
            print("My turn.")
            turn = 0
        else:
            print("Your turn.")
            turn = 1
    else:
        if cpu_symbol is "O":
            print("My turn.")
            turn = 0
        else:
            print("Your turn.")
            turn = 1
    print()
    while win(start_board) is False:
        if turn is 1:
            ava = []
            for i in range(0, len(start_board)):
                if start_board[i] is ".":
                    ava.append(i)
            print()
            print("0 1 2\n3 4 5\n6 7 8")
            print("Possible indexes to place your piece are: " + str(ava))
            index = int(input("What position do you want to play?  "))
            if start_board[index] is not ".":
                while start_board[index] is not ".":
                    print("That spot is already taken.")
                    index = int(input("What position do you want to play?  "))
            start_board = start_board[0:index] + user_symbol + start_board[index+1:]
            printBoard(start_board)
            turn = 0
        if turn is 0:
            #print("Running minimax.")
            moves = minimax(start_board, turn)
            #print(moves)
            if cpu_symbol is "X":
                desired = 1
            else:
                desired = -1
            des = False
            print("Using minimax to analyze all move outcomes.")
            for each in moves:
                if moves[each] is desired:
                    print("Putting a piece at index " + str(each) + " results in a win.")
                elif moves[each] is 0:
                    print("Putting a piece at index " + str(each) + " results in a tie.")
                else:
                    print("Putting a piece at index " + str(each) + " results in a loss.")
            for each in moves:
                if moves[each] is desired:
                    start_board = start_board[0:each] + cpu_symbol + start_board[each+1:]
                    des = True
                    break
            if des is False:
                for each in moves:
                    if moves[each] is 0:
                        start_board = start_board[0:each] + cpu_symbol + start_board[each + 1:]
                        break

            turn = 1
            printBoard(start_board)
    result = win(start_board)
    if result is "DRAW":
        print("We tied.")
    elif result is user_symbol:
        print("You win.")
    elif result is cpu_symbol:
        print("I win.")


game()
