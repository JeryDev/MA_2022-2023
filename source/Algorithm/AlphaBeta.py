from time import time


def is_valid_direction(next_index: int, end: int, direction: str):
    if direction == "vertical":
        if get_row(end) + 1 == get_row(next_index):
            return True
        elif get_row(end) - 1 == get_row(next_index):
            return True
    elif direction == "horizontal":
        if get_column(end) + 1 == get_column(next_index):
            return True
        elif get_column(end) - 1 == get_column(next_index):
            return True
    elif direction == "diagonal":
        if get_row(end) + 1 == get_row(next_index) and get_column(end) + 1 == get_column(next_index):
            return True
        elif get_row(end) - 1 == get_row(next_index) and get_column(end) - 1 == get_column(next_index):
            return True
        elif get_row(end) + 1 == get_row(next_index) and get_column(end) - 1 == get_column(next_index):
            return True
        elif get_row(end) - 1 == get_row(next_index) and get_column(end) + 1 == get_column(next_index):
            return True
    return False


def get_row(index: int):
    return index // 7 + 1


def get_column(index: int):
    return index % 7 + 1


def get_Color(index: int, board: list):
    if index < len(board):
        return board[index][0]
    else:
        return "n"


def get_free_spaces(board: list):
    free_spaces = []
    for i in range(7):
        for k in range(6):
            v = i + ((5 - k) * 7)
            if board[v][0] == "n":
                free_spaces.append(v)
                break
    return free_spaces


def check_middle_position(index: int):
    return index in (3, 10, 17, 24, 31, 38)


DIRECTION_LOOKUP = {
    -8: (-1, -1, "diagonal"), -7: (-1, 0, "vertical"), -6: (-1, 1, "diagonal"),
    -1: (0, -1, "horizontal"),                          1: (0, 1, "horizontal"),
    6: (1, -1, "diagonal"),  7: (1, 0, "vertical"),   8: (1, 1, "diagonal")
}


def get_direction(start: int, end: int):
    diff = end - start
    if diff in DIRECTION_LOOKUP:
        row_diff, col_diff, direction = DIRECTION_LOOKUP[diff]
        next_index = end + row_diff * 7 + col_diff
        if is_valid_direction(next_index, end, direction) and 0 <= next_index <= 41:
            return next_index
    return False


def get_all_neighbours(index: int):
    all_neighbours = []
    right = False
    left = False
    if index // 7 == (index + 1) // 7:
        right = True
    if index // 7 == (index - 1) // 7:
        left = True
    if (index - 7) // 7 >= 0:
        all_neighbours.append(index - 7)
        if right == True:
            all_neighbours.append(index - 6)
        if left == True:
            all_neighbours.append(index - 8)
    if (index + 7) // 7 <= 5:
        all_neighbours.append(index + 7)
        if right == True:
            all_neighbours.append(index + 8)
        if left == True:
            all_neighbours.append(index + 6)
    if right == True:
        all_neighbours.append(index + 1)
    if left == True:
        all_neighbours.append(index - 1)

    all_neighbours.sort()
    return all_neighbours


def analyse(board: list, position: int, color: str):
    value = 0
    all_neighbours = get_all_neighbours(position)
    for i in range(len(all_neighbours)):
        get_color_of_neighbour = get_Color(all_neighbours[i], board)
        if get_color_of_neighbour == color:
            value = value + 10
            neighbour = get_direction(position, all_neighbours[i])
            if neighbour != False:
                get_color_of_neighbour = get_Color(neighbour, board)
                if get_color_of_neighbour == color:
                    value = value + 100
                    neighbour = get_direction(all_neighbours[i], neighbour)
                    if neighbour != False:
                        get_color_of_neighbour = get_Color(neighbour, board)
                        if get_color_of_neighbour == color:
                            value = 10000
                        else:
                            neighbour = get_direction(
                                all_neighbours[i], position)
                            if neighbour != False:
                                get_color_of_neighbour = get_Color(
                                    neighbour, board)
                                if get_all_neighbours == color:
                                    value = 10000
                    else:
                        neighbour = get_direction(all_neighbours[i], position)
                        if neighbour != False:
                            get_color_of_neighbour = get_Color(
                                neighbour, board)
                            if get_color_of_neighbour == color:
                                value = 10000
                else:
                    neighbour = get_direction(all_neighbours[i], position)
                    if neighbour != False:
                        get_color_of_neighbour = get_Color(neighbour, board)
                        if get_color_of_neighbour == color:
                            value = value + 100
                            neighbour = get_direction(position, neighbour)
                            if neighbour != False:
                                get_color_of_neighbour = get_Color(
                                    neighbour, board)
                                if get_color_of_neighbour == color:
                                    value = 10000
            else:
                neighbour = get_direction(all_neighbours[i], position)
                if neighbour != False:
                    get_color_of_neighbour = get_Color(neighbour, board)
                    if get_color_of_neighbour == color:
                        value = value + 100
                        neighbour = get_direction(position, neighbour)
                        if neighbour != False:
                            get_color_of_neighbour = get_Color(
                                neighbour, board)
                            if get_color_of_neighbour == color:
                                value = 10000

    if color == "y":
        return value
    else:
        return -value


def check_win(board: list):
    won = None
    for row in range(6):
        yellowInRow = 0
        redInRow = 0
        for column in range(7):
            if board[column + row * 7][0] == "r":
                redInRow = redInRow + 1
                yellowInRow = 0
            elif board[column + row * 7][0] == "y":
                yellowInRow = yellowInRow + 1
                redInRow = 0
            else:
                yellowInRow = 0
                redInRow = 0
            if redInRow == 4:
                won = "red"
                break
            if yellowInRow == 4:
                won = "yellow"
                break

    # Überprüfung: Vertikal (oben / unten)
    for column in range(7):
        yellowInRow = 0
        redInRow = 0
        for row in range(6):
            if board[column + row * 7][0] == "r":
                redInRow = redInRow + 1
                yellowInRow = 0
            elif board[column + row * 7][0] == "y":
                yellowInRow = yellowInRow + 1
                redInRow = 0
            else:
                yellowInRow = 0
                redInRow = 0
            if redInRow == 4:
                won = "red"
                break
            if yellowInRow == 4:
                won = "yellow"
                break

    # Überprüfung: Diagonal (rechts unten / links oben)
    for row in range(3):
        for column in range(4):
            yellowInRow = 0
            redInRow = 0
            for diagonal in range(4):
                if board[column + row * 7 + diagonal * 8][0] == "r":
                    redInRow = redInRow + 1
                    yellowInRow = 0
                elif board[column + row * 7 + diagonal * 8][0] == "y":
                    yellowInRow = yellowInRow + 1
                    redInRow = 0
                else:
                    yellowInRow = 0
                    redInRow = 0
                if redInRow == 4:
                    won = "red"
                    break
                if yellowInRow == 4:
                    won = "yellow"
                    break

    # Überprüfung: Diagonal (rechts oben / links unten)
    for row in range(3):
        for column in range(4):
            yellowInRow = 0
            redInRow = 0
            for diagonal in range(4):
                if board[column + 3 + row * 7 + diagonal * 6][0] == "r":
                    redInRow = redInRow + 1
                    yellowInRow = 0
                elif board[column + 3 + row * 7 + diagonal * 6][0] == "y":
                    yellowInRow = yellowInRow + 1
                    redInRow = 0
                else:
                    yellowInRow = 0
                    redInRow = 0
                if redInRow == 4:
                    won = "red"
                    break
                if yellowInRow == 4:
                    won = "yellow"
                    break
    return won


def make_move(board: list, move: int, color: str):
    newBoard = []
    for i in range(len(board)):
        newBoard.append(board[i])
    newBoard[move] = f"{color}{newBoard[move][1:]}"
    return newBoard


def to_minimax(board: list, depth: int, color: str, alpha: int, beta: int):
    if depth > 0:
        results = []
        for position in get_free_spaces(board):
            newBoard = make_move(board, position, color)
            if color == "y":
                maxPlayer = False
                value = minimax(newBoard, position, depth - 1, maxPlayer, alpha, beta)
                if check_middle_position(position):
                    value = value + 4
            elif color == "r":
                maxPlayer = True
                value = minimax(newBoard, position, depth - 1, maxPlayer, alpha, beta)
                if check_middle_position(position):
                    value = value - 4
            results.append([value, position])
        print(results)
        if color == "y":
            max = [-1000000, None]
            for res in results:
                if res[0] >= max[0]:
                    max = res
            return max

        if color == "r":
            min = [1000000, None]
            for res in results:
                if res[0] <= min[0]:
                    min = res
            return min

        return results
    return False


def minimax(board: list, position: int, depth: int, maxPlayer: bool, alpha: int, beta: int):
    if depth == 0 or check_win(board) != None:
        if check_win(board) == "yellow":
            return 10000
        elif check_win(board) == "red":
            return -10000
        if depth == 0:
            if maxPlayer:
              return analyse(board, position, "r")
            else:
              return analyse(board, position, "y")

    if maxPlayer:
        bestValue = -1000000
        for move in get_free_spaces(board):
            newBoard = make_move(board, move, "y")
            value = minimax(newBoard, move, depth - 1, False, alpha, beta)
            bestValue = max(bestValue, value)
            alpha = max(alpha, bestValue)
            if beta <= alpha:
                break
        return bestValue

    else:
        bestValue = 1000000
        for move in get_free_spaces(board):
            newBoard = make_move(board, move, "r")
            value = minimax(newBoard, move, depth - 1, True, alpha, beta)
            bestValue = min(bestValue, value)
            beta = min(beta, bestValue)
            if beta <= alpha:
                break
        return bestValue


board_from_Excel = [
    "n00", "n01", "n02", "n03", "n04", "n05", "n06",
    "n07", "n08", "n09", "n10", "n11", "n12", "n13",
    "n14", "n15", "n16", "n17", "n18", "n19", "n20",
    "n21", "n22", "n23", "n24", "n25", "n26", "n27",
    "n28", "n29", "n30", "n31", "n32", "n33", "n34",
    "n35", "n36", "n37", "n38", "n39", "n40", "n41"
]

board_to_use = []

for i in range(len(board_from_Excel)):
    board_to_use.append(board_from_Excel[i])


color = "y"
depth = 7
alpha = -1000000
beta = 1000000

StartTime = time()
results = to_minimax(board_to_use, depth, color, alpha, beta)
EndTime = time()

print(f"Best Index: {results[1]}")
print(f"Value: {results[0]}")
print(f"Time: {round(EndTime - StartTime, 2)} Seconds")
