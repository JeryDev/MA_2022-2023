"""
Alpha-Beta-Pruning (minimax) in Vier-Gewinnt von Jery
"""

from time import time

depth = 7


def function_statistics(func):
    """
    Eine Funktion, die als Decorator dient und eine andere Funktion modifiziert,
    indem sie ihr zusätzliche Funktionalität hinzufügt, um Statistiken über die
    Anzahl der Aufrufe und die Dauer der Ausführung der ursprünglichen Funktion zu sammeln.

    Args:
        func: Die Funktion, die modifiziert werden soll.

    Returns:
        Eine neue Funktion, die als Wrapper fungiert und die ursprüngliche Funktion ausführt.
    """
    def wrapper(*args, **kwargs):
        """
        Ein Wrapper, der die ursprüngliche Funktion ausführt und Statistiken sammelt.

        Args:
            *args: Die Positional Arguments, die an die ursprüngliche Funktion übergeben werden.
            **kwargs: Die Keyword Arguments, die an die ursprüngliche Funktion übergeben werden.

        Returns:
            Das Ergebnis der ursprünglichen Funktion.
        """
        start_time = time()  # Startzeit des Funktionsaufrufs
        result = func(*args, **kwargs)  # Die ursprüngliche Funktion ausführen
        end_time = time()  # Endzeit des Funktionsaufrufs

        # Die Statistiken aktualisieren
        if not hasattr(func, 'stats'):
            func.stats = {'count': 0, 'duration': 0}

        func.stats['count'] += 1
        func.stats['duration'] += end_time - start_time

        return result

    def print_stats():
        """
        Eine Funktion, die die gesammelten Statistiken auf der Konsole ausgibt.
        """
        yellow = "\033[93m"
        reset = "\033[0m"
        print("\n")
        print(f"Statistics for {yellow}{func.__name__}{reset}:")
        print(f"Function called {func.stats['count']} time(s).")
        print(f"Total duration of {func.stats['duration']} seconds.")
        Average_duration = func.stats['duration'] / func.stats['count']
        print(f"Average duration of {Average_duration} seconds.")

    def get_duration():
        """
        Eine Funktion, die die totale Zeit zurückgibt
        """
        return func.stats['duration']

    # Das Attribut 'print_stats' zum Wrapper hinzufügen
    wrapper.print_stats = print_stats

    # Das Attribut 'get_duration' zum Wrapper hinzufügen
    wrapper.get_duration = get_duration

    # Den Wrapper zurückgeben
    return wrapper


@function_statistics
def is_valid_direction(next_index: int, end: int, direction: str):
    """
    Überprüft, ob ein Index in der gegebenen Richtung gültig ist, wenn er als
    nächstes besucht wird.

    Args:
        next_index: Der nächste Index, der überprüft werden soll.
        end: Der Index, von dem aus gestartet wird.
        direction: Die Richtung, in der überprüft werden soll.

    Returns:
        True, wenn der nächste Index in der gegebenen Richtung gültig ist, andernfalls False.
    """
    if direction == "vertical":
        if get_row(end) + 1 == get_row(next_index):
            # Der nächste Index ist eine Zeile darunter
            return True
        elif get_row(end) - 1 == get_row(next_index):
            # Der nächste Index ist eine Zeile darüber
            return True
    elif direction == "horizontal":
        if get_column(end) + 1 == get_column(next_index):
            # Der nächste Index ist eine Spalte rechts
            return True
        elif get_column(end) - 1 == get_column(next_index):
            # Der nächste Index ist eine Spalte links
            return True
    elif direction == "diagonal":
        if get_row(end) + 1 == get_row(next_index) and get_column(end) + 1 == get_column(next_index):
            # Der nächste Index ist diagonal unten rechts
            return True
        elif get_row(end) - 1 == get_row(next_index) and get_column(end) - 1 == get_column(next_index):
            # Der nächste Index ist diagonal oben links
            return True
        elif get_row(end) + 1 == get_row(next_index) and get_column(end) - 1 == get_column(next_index):
            # Der nächste Index ist diagonal unten links
            return True
        elif get_row(end) - 1 == get_row(next_index) and get_column(end) + 1 == get_column(next_index):
            # Der nächste Index ist diagonal oben rechts
            return True
    # Der nächste Index ist in keiner der erlaubten Richtungen gültig.
    return False


@function_statistics
def get_row(index: int):
    """
    Gibt die Zeile zurück, in der sich der gegebene Index befindet.

    Args:
        index: Der Index, dessen Zeile zurückgegeben werden soll.

    Returns:
        Die Zeile, in der sich der gegebene Index befindet.
    """
    return index // 7 + 1


@function_statistics
def get_column(index: int):
    """
    Gibt die Spalte zurück, in der sich der gegebene Index befindet.

    Args:
        index: Der Index, dessen Spalte zurückgegeben werden soll.

    Returns:
        Die Spalte, in der sich der gegebene Index befindet.
    """
    return index % 7 + 1


@function_statistics
def get_Color(index: int, board: list):
    """
    Gibt die Farbe des Steins am gegebenen Index auf dem gegebenen Spielbrett zurück.

    Args:
        index: Der Index, an dem sich der Stein befindet.
        board: Eine Liste, die das Spielbrett repräsentiert.

    Returns:
        Die Farbe des Steins am gegebenen Index auf dem Spielbrett.
        Gibt "n" zurück, wenn kein Stein an diesem Index vorhanden ist.
    """
    if index < len(board):  # Überprüfen, ob der gegebene Index im Bereich des Spielbretts liegt
        return board[index][0]
    else:
        return "n"


@function_statistics
def get_free_spaces(board: list):
    """
    Gibt eine Liste von Indexe zurück, die auf freie Plätze auf dem Spielbrett verweisen.

    Args:
        board: Eine Liste, die das Spielbrett repräsentiert.

    Returns:
        Eine Liste von Indexe, die auf freie Plätze auf dem Spielbrett verweisen.
    """
    free_spaces = []
    for i in range(7):
        for k in range(6):
            # Berechnung des Index des Elements in der aktuellen Spalte und Zeile.
            v = i + ((5 - k) * 7)
            if board[v][0] == "n":
                free_spaces.append(v)
                break
    return free_spaces


@function_statistics
def check_middle_position(index: int):
    """
    Überprüft, ob der gegebene Index in der Mitte auf dem Spielbrett ist.

    Args:
        index: Der Index, der überprüft werden soll.

    Returns:
        True, wenn der gegebene Index in der Mitte auf dem Spielbrett ist.
        False, wenn der gegebene Index nicht in der Mitte auf dem Spielbrett ist.
    """
    return index in (3, 10, 17, 24, 31, 38)


DIRECTION_LOOKUP = {
    -8: (-1, -1, "diagonal"), -7: (-1, 0, "vertical"), -6: (-1, 1, "diagonal"),
    -1: (0, -1, "horizontal"),                          1: (0, 1, "horizontal"),
    6: (1, -1, "diagonal"),  7: (1, 0, "vertical"),   8: (1, 1, "diagonal")
}


@function_statistics
def get_direction(start: int, end: int):
    """
    Bestimmt die Richtung basierend auf dem Start- und Endindex.

    Args:
        start: Der Startindex.
        end: Der Endindex.

    Returns:
        Der nächste Index in der berechneten Richtung, wenn die Richtung gültig ist.
        False, wenn die Richtung ungültig ist oder der nächste Index außerhalb des Spielbretts liegt.
    """
    diff = end - start  # Die Differenz zwischen Start- und Endindex wird berechnet.
    # Wenn die Differenz in der DIRECTION_LOOKUP-Liste enthalten ist, gibt es eine gültige Richtung.
    if diff in DIRECTION_LOOKUP:
        # Die Zeilen- und Spaltenunterschiede sowie die Richtung werden aus der DIRECTION_LOOKUP-Liste abgerufen.
        row_diff, col_diff, direction = DIRECTION_LOOKUP[diff]
        # Der nächste Index in der berechneten Richtung wird berechnet.
        next_index = end + row_diff * 7 + col_diff
        # Überprüfung, ob der nächste Index in der berechneten Richtung gültig ist und innerhalb des Spielbretts liegt.
        if is_valid_direction(next_index, end, direction) and 0 <= next_index <= 41:
            return next_index  # Der nächste Index wird zurückgegeben.
    # Wenn die Richtung ungültig ist oder der nächste Index außerhalb des Spielbretts liegt, wird False zurückgegeben.
    return False


@function_statistics
def get_all_neighbours(index: int):
    """
    Bestimmt alle Steine, welche sich um einen bestimmten Index befinden.

    Args:
        index: Der Index, an dem sich der Stein befindet.

    Returns:
        Gibt eine Liste mit allen Indexen zurück.
    """
    all_neighbours = []
    right = False
    left = False
    # Überprüfe, ob der Index und der Index+1 in derselben Zeile sind.
    if index // 7 == (index + 1) // 7:
        right = True
    # Überprüfe, ob der Index und der Index-1 in derselben Zeile sind
    if index // 7 == (index - 1) // 7:
        left = True
    # Überprüfe, ob über dem der Index eine freie Zeile ist.
    if (index - 7) // 7 >= 0:
        all_neighbours.append(index - 7)
        if right == True:
            all_neighbours.append(index - 6)
        if left == True:
            all_neighbours.append(index - 8)
    # Überprüfe, ob unter dem der Index eine freie Zeile ist.
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


@function_statistics
def analyse(board: list, position: int, color: str):
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
    all_neighbours = get_all_neighbours(position)
    # Iteriere durch die Nachbarn des Steins
    for neighbour in all_neighbours:
        # Wenn die Farbe des Nachbarn nicht die gleiche ist wie die Farbe des Spielers, ignoriere ihn
        neighbour_color = get_Color(neighbour, board)
        if neighbour_color != color:
            continue
        value += 10

        # Wenn der Nachbar auch einen Nachbarn in der gleichen Richtung hat, erhöhe den Wert um 100
        neighbour_2 = get_direction(position, neighbour)
        if neighbour_2 is False:
            continue

        neighbour_2_color = get_Color(neighbour_2, board)
        if neighbour_2_color == color:
            value += 100

            # Wenn der Nachbar auch einen zweiten Nachbarn in der gleichen Richtung hat, erhöhe den Wert auf 10000
            neighbour_3 = get_direction(neighbour, neighbour_2)

            if neighbour_3 is not False:
                neighbour_3_color = get_Color(neighbour_3, board)

                if neighbour_3_color == color:
                    value = 10000
                    break

                # Wenn der Nachbar auch einen Nachbarn in der entgegengesetzten Richtung hat, erhöhe den Wert auf 10000
                neighbour_3 = get_direction(neighbour, position)

                if neighbour_3 is not False and get_Color(neighbour_3, board) == color:
                    value = 10000
                    break

        else:
            # Wenn der Nachbar keinen zweiten Nachbarn in der gleichen Richtung hat, aber einen in die entgegengesetzte Richtung hat, erhöhe den Wert um 100
            neighbour_3 = get_direction(neighbour, position)

            if neighbour_3 is not False and get_Color(neighbour_3, board) == color:
                value += 100
    if color == "y":
        return value
    else:
        return -value


@function_statistics
def check_win(board: list):
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
                if all(board[cell_index + i][0] == board[cell_index][0] for i in range(1, 4)):
                    if board[cell_index][0] == "y":
                        return "yellow"
                    else:
                        return "red"

    # Überprüfung der vertikalen Gewinnbedingung
    for column in range(7):
        for row in range(3):
            cell_index = column + row * 7
            if board[cell_index][0] != "n":
                if all(board[cell_index + i*7][0] == board[cell_index][0] for i in range(1, 4)):
                    if board[cell_index][0] == "y":
                        return "yellow"
                    else:
                        return "red"

    # Überprüfung der Diagonalen (rechts unten nach links oben) Gewinnbedingung
    for row in range(3):
        for column in range(4):
            cell_index = column + row * 7
            if board[cell_index][0] != "n":
                if all(board[cell_index + i*8][0] == board[cell_index][0] for i in range(1, 4)):
                    if board[cell_index][0] == "y":
                        return "yellow"
                    else:
                        return "red"

    # Überprüfung der Diagonalen (links unten nach rechts oben) Gewinnbedingung
    for row in range(3):
        for column in range(4):
            cell_index = column + 3 + row * 7
            if board[cell_index][0] != "n":
                if all(board[cell_index + i*6][0] == board[cell_index][0] for i in range(1, 4)):
                    if board[cell_index][0] == "y":
                        return "yellow"
                    else:
                        return "red"

    return won


@function_statistics
def make_move(board: list, move: int, color: str):
    """
    Führt einen Spielzug durch, indem ein Stein des Spielers auf dem Spielbrett platziert wird.

    Args:
        board: Eine Liste, die das Spielbrett repräsentiert.
        move: Der Index, in die der Spieler sein Stein setzen möchte (0-basiert).
        color: Die Farbe des Spielers (z.B. 'y' für gelb oder 'r' für rot).

    Returns:
        newBoard: Eine Kopie des ursprünglichen Spielbretts mit dem hinzugefügten Stein des Spielers.
    """
    # Kopiere das Spielbrett, um es nicht zu verändern
    newBoard = list(board)

    # Setze das Symbol des Spielers in der gewählten Spalte
    newBoard[move] = f"{color}{newBoard[move][1:]}"

    return newBoard


@function_statistics
def to_minimax(board: list, depth: int, color: str, alpha: int, beta: int):
    """
    Wandelt das Spielbrett in ein Format um, das von der Minimax-Funktion verwendet werden kann.

    Args:
        board: Eine Liste, die das Spielbrett repräsentiert.
        depth: Die maximale Tiefe der Rekursion, die vom Minimax-Algorithmus durchlaufen werden soll.
        color: Die Farbe des Spielers, dessen bester Spielzug berechnet werden soll (z.B. 'y' für gelb oder 'r' für rot).
        alpha: Der aktuelle Alpha-Wert des Alpha-Beta-Pruning-Algorithmus.
        beta: Der aktuelle Beta-Wert des Alpha-Beta-Pruning-Algorithmus.

    Returns:
        Eine Liste mit dem besten Spielzug und seinem Bewertungswert, wenn die maximale Rekursionstiefe erreicht wurde.
        Andernfalls eine Liste mit den Bewertungswerten aller möglichen Spielzüge.
    """
    # Wenn die maximale Rekursionstiefe erreicht wurde, gebe False zurück
    if depth <= 0:
        return False

    # Initialisiere eine leere Ergebnisliste
    results = []

    # Durchlaufe alle freien Positionen auf dem Spielbrett
    for position in get_free_spaces(board):
        # Führe den Spielzug aus und berechne den Bewertungswert des Spielbretts
        newBoard = make_move(board, position, color)
        if color == "y":
            maxPlayer = False
            value = minimax(newBoard, position, depth -
                            1, maxPlayer, alpha, beta)
            # Füge einen Bonus hinzu, wenn der Spielzug in der Mitte der untersten Reihe erfolgt
            if check_middle_position(position):
                value = value + 4
        elif color == "r":
            maxPlayer = True
            value = minimax(newBoard, position, depth -
                            1, maxPlayer, alpha, beta)
            # Ziehe einen Malus ab, wenn der Spielzug in der Mitte der untersten Reihe erfolgt
            if check_middle_position(position):
                value = value - 4

        # Füge den Bewertungswert des Spielzugs und seine Position der Ergebnisliste hinzu
        results.append([value, position])

    # Gib die Ergebnisliste basierend auf der Farbe des Spielers zurück
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


@function_statistics
def minimax(board: list, position: int, depth: int, maxPlayer: bool, alpha: int, beta: int):
    """
    Ein Algorithmus, der den bestmöglichen Spielzug in einer Connect-4-Partie findet.

    Args:
        board: Eine Liste, die das Spielbrett repräsentiert.
        position: Die Position des letzten Zugs.
        depth: Die aktuelle Tiefe im Suchbaum.
        maxPlayer: Ein Boolean, der angibt, ob der maximierende Spieler am Zug ist.
        alpha: Der aktuelle Alpha-Wert.
        beta: Der aktuelle Beta-Wert.

    Returns:
        Der Wert des besten Spielzugs.
    """

    # Wenn die maximale Tiefe erreicht wurde oder das Spiel gewonnen wurde
    if depth == 0 or check_win(board) != None:
        # Falls Gelb gewonnen hat, gib 10000 zurück
        if check_win(board) == "yellow":
            return 10000
        # Falls Rot gewonnen hat, gib -10000 zurück
        elif check_win(board) == "red":
            return -10000
        # Falls die maximale Tiefe erreicht wurde, berechne den Wert des aktuellen Boards und gib ihn zurück
        if depth == 0:
            if maxPlayer:
                return analyse(board, position, "r")
            else:
                return analyse(board, position, "y")

    # Wenn der maximierende Spieler am Zug ist
    if maxPlayer:
        bestValue = -1000000
        # Für jeden möglichen Zug
        for move in get_free_spaces(board):
            # Mach den Zug auf dem Board
            newBoard = make_move(board, move, "y")
            # Berechne den Wert des Zuges mit Hilfe des Minimax-Algorithmus
            value = minimax(newBoard, move, depth - 1, False, alpha, beta)
            # Wenn der berechnete Wert besser als der aktuelle beste Wert ist, aktualisiere den besten Wert
            bestValue = max(bestValue, value)
            # Aktualisiere den Alpha-Wert
            alpha = max(alpha, bestValue)
            # Wenn der Beta-Wert kleiner als oder gleich dem Alpha-Wert ist, breche die Schleife ab
            if beta <= alpha:
                break
        # Gib den besten Wert zurück
        return bestValue

    # Wenn der minimierende Spieler am Zug ist
    else:
        bestValue = 1000000
        # Für jeden möglichen Zug
        for move in get_free_spaces(board):
            # Mach den Zug auf dem Board
            newBoard = make_move(board, move, "r")
            # Berechne den Wert des Zuges mit Hilfe des Minimax-Algorithmus
            value = minimax(newBoard, move, depth - 1, True, alpha, beta)
            # Wenn der berechnete Wert besser als der aktuelle beste Wert ist, aktualisiere den besten Wert
            bestValue = min(bestValue, value)
            # Aktualisiere den Beta-Wert
            beta = min(beta, bestValue)
            # Wenn der Beta-Wert kleiner als oder gleich dem Alpha-Wert ist, breche die Schleife ab
            if beta <= alpha:
                break
        # Gib den besten Wert zurück
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
alpha = -1000000
beta = 1000000

StartTime = time()
results = to_minimax(board_to_use, depth, color, alpha, beta)
EndTime = time()

print("\nResults:")
print(f"Best Index: {results[1]}")
print(f"Value: {results[0]}")
print(f"Time: {round(EndTime - StartTime, 2)} Seconds")

is_valid_direction.print_stats()
get_row.print_stats()
get_column.print_stats()
get_Color.print_stats()
get_free_spaces.print_stats()
check_middle_position.print_stats()
get_direction.print_stats()
get_all_neighbours.print_stats()
analyse.print_stats()
check_win.print_stats()
make_move.print_stats()
to_minimax.print_stats()
minimax.print_stats()

print(f"\nTotal time: {EndTime-StartTime} Seconds\n")
