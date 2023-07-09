from time import time

def isValidDirection(next_index: int, end: int, direction: str):
    if direction == "vertical":
        if getRow(end) + 1 == getRow(next_index):
            return True
        elif getRow(end) - 1 == getRow(next_index):
            return True
    elif direction == "horizontal":
        if getColumn(end) + 1 == getColumn(next_index):
            return True
        elif getColumn(end) - 1 == getColumn(next_index):
            return True
    elif direction == "diagonal":
        if getRow(end) + 1 == getRow(next_index) and getColumn(end) + 1 == getColumn(next_index):
            return True
        elif getRow(end) - 1 == getRow(next_index) and getColumn(end) - 1 == getColumn(next_index):
            return True
        elif getRow(end) + 1 == getRow(next_index) and getColumn(end) - 1 == getColumn(next_index):
            return True
        elif getRow(end) - 1 == getRow(next_index) and getColumn(end) + 1 == getColumn(next_index):
            return True
    return False


def getRow(index: int):
    return index // 7 + 1


def getColumn(index: int):
    return index % 7 + 1


def getColor(index: int, board: list):
    if index < len(board):
        return board[index][0]
    else:
        return "n"


def getFreePositions(board: list):
    free_spaces = []
    for i in range(7):
        for k in range(6):
            v = i + ((5 - k) * 7)
            if board[v][0] == "n":
                free_spaces.append(v)
                break
    return free_spaces

def checkMiddlePosition(index: int):
    return index in (3, 10, 17, 24, 31, 38)


DIRECTION_LOOKUP = {
    -8: (-1, -1, "diagonal"), -7: (-1, 0, "vertical"), -6: (-1, 1, "diagonal"),
    -1: (0, -1, "horizontal"),                          1: (0, 1, "horizontal"),
    6: (1, -1, "diagonal"),  7: (1, 0, "vertical"),   8: (1, 1, "diagonal")
}


def getDirection(start: int, end: int):
    diff = end - start
    if diff in DIRECTION_LOOKUP:
        row_diff, col_diff, direction = DIRECTION_LOOKUP[diff]
        next_index = end + row_diff * 7 + col_diff
        if isValidDirection(next_index, end, direction) and 0 <= next_index <= 41:
            return next_index
    return False


def getAllNeighbours(index: int):
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


def evaluate(board: list, position: int, color: str):
    """
    Analysiert das Spiel anhand einer Position.

    Args:
        board: Eine Liste, die das Spielbrett repräsentiert.
        position: Ein Index, der die Position eines Steines repräsentiert.
        color: Die Farbe des Steines

    Returns:
        Gibt einen Wert zurück, der ausgibt, wie gut eine Position ist.
    """
    value = 0
    all_neighbours = getAllNeighbours(position)
    # Iteriere durch die Nachbarn des Steins
    for neighbour in all_neighbours:
        # Wenn die Farbe des Nachbarn nicht die gleiche ist wie die Farbe des Spielers, ignoriere ihn
        neighbour_color = getColor(neighbour, board)
        if neighbour_color != color:
            continue
        value += 10

        # Wenn der Nachbar auch einen Nachbarn in der gleichen Richtung hat, erhöhe den Wert um 100
        neighbour_2 = getDirection(position, neighbour)
        if neighbour_2 is False:
            continue

        neighbour_2_color = getColor(neighbour_2, board)
        if neighbour_2_color == color:
            value += 100

            # Wenn der Nachbar auch einen zweiten Nachbarn in der gleichen Richtung hat, erhöhe den Wert auf 10000
            neighbour_3 = getDirection(neighbour, neighbour_2)

            if neighbour_3 is not False:
                neighbour_3_color = getColor(neighbour_3, board)

                if neighbour_3_color == color:
                    value = 10000
                    break

                # Wenn der Nachbar auch einen Nachbarn in der entgegengesetzten Richtung hat, erhöhe den Wert auf 10000
                neighbour_3 = getDirection(neighbour, position)

                if neighbour_3 is not False and getColor(neighbour_3, board) == color:
                    value = 10000
                    break

        else:
            # Wenn der Nachbar keinen zweiten Nachbarn in der gleichen Richtung hat, aber einen in die entgegengesetzte Richtung hat, erhöhe den Wert um 100
            neighbour_3 = getDirection(neighbour, position)

            if neighbour_3 is not False and getColor(neighbour_3, board) == color:
                value += 100
    
    if color == "y":
        return value
    else:
        return -value


def checkWin(board: list):
    """
    Überprüft ob jemand gewonnen hat

    Args:
        board: Eine Liste, die das Spielbrett repräsentiert.

    Returns:
        yellow: Gelb hat gewonnen.
        red: Rot hat gewonnen.
        None: Niemand hat gewonnen.
    """
    won = None

    # Überprüfung der horizontalen Gewinnbedingung
    for row in range(6):
        for column in range(4):
            cell_index = column + row * 7
            if board[cell_index][0] != "n":
                if all(
                    board[cell_index + i][0] == board[cell_index][0]
                    for i in range(1, 4)
                ):
                    if board[cell_index][0] == "y":
                        return "yellow"
                    else:
                        return "red"

    # Überprüfung der vertikalen Gewinnbedingung
    for column in range(7):
        for row in range(3):
            cell_index = column + row * 7
            if board[cell_index][0] != "n":
                if all(
                    board[cell_index + i * 7][0] == board[cell_index][0]
                    for i in range(1, 4)
                ):
                    if board[cell_index][0] == "y":
                        return "yellow"
                    else:
                        return "red"

    # Überprüfung der Diagonalen (rechts unten nach links oben) Gewinnbedingung
    for row in range(3):
        for column in range(4):
            cell_index = column + row * 7
            if board[cell_index][0] != "n":
                if all(
                    board[cell_index + i * 8][0] == board[cell_index][0]
                    for i in range(1, 4)
                ):
                    if board[cell_index][0] == "y":
                        return "yellow"
                    else:
                        return "red"

    # Überprüfung der Diagonalen (links unten nach rechts oben) Gewinnbedingung
    for row in range(3):
        for column in range(4):
            cell_index = column + 3 + row * 7
            if board[cell_index][0] != "n":
                if all(
                    board[cell_index + i * 6][0] == board[cell_index][0]
                    for i in range(1, 4)
                ):
                    if board[cell_index][0] == "y":
                        return "yellow"
                    else:
                        return "red"

    return won


def makeMove(board: list, move: int, color: str):
    newBoard = []
    for i in range(len(board)):
        newBoard.append(board[i])
    newBoard[move] = f"{color}{newBoard[move][1:]}"
    return newBoard


def getResults(board: list, depth: int, color: str):
    if depth > 0:
        results = []
        for position in getFreePositions(board):
            newBoard = makeMove(board, position, color)
            if color == "y":
                maxPlayer = False
                value = minimax(newBoard, position, depth - 1, maxPlayer)
                if checkMiddlePosition(position):
                    value = value + 4
            elif color == "r":
                maxPlayer = True
                value = minimax(newBoard, position, depth - 1, maxPlayer)
                if checkMiddlePosition(position):
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


def minimax(board: list, position: int, depth: int, maxPlayer: bool):
    if depth == 0 or checkWin(board) != None:
        if checkWin(board) == "yellow":
            return 10000
        elif checkWin(board) == "red":
            return -10000
        if depth == 0:
            if maxPlayer:
                return evaluate(board, position, "r")
            else:
                return evaluate(board, position, "y")

    if maxPlayer:
        bestValue = -1000000
        for move in getFreePositions(board):
            newBoard = makeMove(board, move, "y")
            value = minimax(newBoard, move, depth - 1, False)
            bestValue = max(bestValue, value)
        return bestValue

    else:
        bestValue = 1000000
        for move in getFreePositions(board):
            newBoard = makeMove(board, move, "r")
            value = minimax(newBoard, move, depth - 1, True)
            bestValue = min(bestValue, value)
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
depth = 6

StartTime = time()
results = getResults(board_to_use, depth, color)
EndTime = time()

print(f"Best Index: {results[1]}")
print(f"Value: {results[0]}")
print(f"Time: {round(EndTime - StartTime, 2)} Seconds")
