# Vier-Gewinnt Python-Programm (pygame) gegen Alpha-Beta (minimax) von Jery:
import pygame as p

# Den "Size" Parameter setzen
size = 800

# Suchtiefe des Algorithmus
depth = 7

# Initialisierungsfunktion
p.init()


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
        if get_row(end) + 1 == get_row(next_index) and get_column(
            end
        ) + 1 == get_column(next_index):
            # Der nächste Index ist diagonal unten rechts
            return True
        elif get_row(end) - 1 == get_row(next_index) and get_column(
            end
        ) - 1 == get_column(next_index):
            # Der nächste Index ist diagonal oben links
            return True
        elif get_row(end) + 1 == get_row(next_index) and get_column(
            end
        ) - 1 == get_column(next_index):
            # Der nächste Index ist diagonal unten links
            return True
        elif get_row(end) - 1 == get_row(next_index) and get_column(
            end
        ) + 1 == get_column(next_index):
            # Der nächste Index ist diagonal oben rechts
            return True
    # Der nächste Index ist in keiner der erlaubten Richtungen gültig.
    return False


def get_row(index: int):
    """
    Gibt die Zeile zurück, in der sich der gegebene Index befindet.

    Args:
        index: Der Index, dessen Zeile zurückgegeben werden soll.

    Returns:
        Die Zeile, in der sich der gegebene Index befindet.
    """
    return index // 7 + 1


def get_column(index: int):
    """
    Gibt die Spalte zurück, in der sich der gegebene Index befindet.

    Args:
        index: Der Index, dessen Spalte zurückgegeben werden soll.

    Returns:
        Die Spalte, in der sich der gegebene Index befindet.
    """
    return index % 7 + 1


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
    if index < len(
        board
    ):  # Überprüfen, ob der gegebene Index im Bereich des Spielbretts liegt
        return board[index][0]
    else:
        return "n"


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
    -8: (-1, -1, "diagonal"),
    -7: (-1, 0, "vertical"),
    -6: (-1, 1, "diagonal"),
    -1: (0, -1, "horizontal"),
    1: (0, 1, "horizontal"),
    6: (1, -1, "diagonal"),
    7: (1, 0, "vertical"),
    8: (1, 1, "diagonal"),
}


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
            value = minimax(newBoard, position, depth - 1, maxPlayer, alpha, beta)
            # Füge einen Bonus hinzu, wenn der Spielzug in der Mitte der untersten Reihe erfolgt
            if check_middle_position(position):
                value = value + 4
        elif color == "r":
            maxPlayer = True
            value = minimax(newBoard, position, depth - 1, maxPlayer, alpha, beta)
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


def minimax(
    board: list, position: int, depth: int, maxPlayer: bool, alpha: int, beta: int
):
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


# Grösse von einem Feld bestimmen
sizeOne = int(size / 7)

width = size
height = size

# Hier werden die Grössen eingetragen.
screen = p.display.set_mode((width, height))

# Fensterbeschriftung
p.display.set_caption("Vier-Gewinnt")

# Liste, welche die besetzten Felder speichert
occupied = []

# Liste, welche das aktuelle Feld speichert
board = []

# Leeres Feld wird generiert
for n in range(42):
    board.append("nnn")

# Aktueller Spielzug
move = 0

# Int wird in einen gültigen String umgewandelt


def moveSyntax(move):
    if move < 10:
        move = "0" + str(move)
        return move
    else:
        return str(move)


# Die Spielfläche wird gezeichnet


def drawGame():
    for i in range(8):
        p.draw.line(
            screen,
            [255, 255, 255],
            [0, i * sizeOne + sizeOne - 2.5],
            [size, i * sizeOne + sizeOne - 2.5],
            5,
        )
        p.draw.line(
            screen, [255, 255, 255], [i * sizeOne, sizeOne], [i * sizeOne, size], 5
        )


# Ein gelder oder roter Kreis wird gezeichnet
def drawBall(x, y):
    if player:
        color = [255, 255, 0]
    else:
        color = [255, 0, 0]
    p.draw.circle(screen, color, [x, y], sizeOne / 2 - 5)


# Hier werden die Koordinaten geprüft und verarbeitet.
# Es wird nach dem nächst freien Feld ein einer Spalte gesucht.
# Schlussendlich werden die verarbeiteten Daten in den Listen occupied und board gespeichert.
def put(column: int):
    i = 35
    inColumn = False
    while i >= 0:
        if (i + column) not in occupied:
            occupied.append(i + column)
            if player:
                board[i + column] = "y" + moveSyntax(move)
            else:
                board[i + column] = "r" + moveSyntax(move)
            inColumn = True
            x = column * sizeOne + (sizeOne / 2)
            y = (i // 7) * sizeOne + (sizeOne * 1.5)
            drawBall(x, y)
            break
        else:
            i = i - 7

    return inColumn


# Boolean: True = (Das Spiel ist am laufen) False = (Das Spiel ist nicht mehr am laufen)
online = True

# Boolean: True = (Gelber Spieler) False = (Roter Spieler)
player = True

# Solange das Spiel online ist, sollte es dauernd das Feld überprüfen.
while online:
    for event in p.event.get():
        if event.type == p.QUIT:
            # Spiel wird beendet
            online = False

        # Das Fenster wird neugeladen
        p.display.update()
        if len(occupied) == len(board):
            player = None
            font = p.font.Font("freesansbold.ttf", 32)
            text = font.render("Unentschieden!", True, (0, 255, 0), (0, 0, 255))
            textRect = text.get_rect()
            textRect.center = (180, height // 20)
            screen.blit(text, textRect)
            text = font.render("Neustarten", True, (0, 255, 0), (0, 0, 255))
            textRect = text.get_rect()
            textRect.center = (width - 110, height // 20)
            screen.blit(text, textRect)

        if player == False:
            result = to_minimax(board, depth, "r", -1000000, 1000000)
            occupied.append(result[1])
            board[result[1]] = f"r{moveSyntax(move)}"
            column = get_column(result[1]) - 1
            row = get_row(result[1]) - 1
            x = column * sizeOne + (sizeOne / 2)
            y = row * sizeOne + (sizeOne * 1.5)
            drawBall(x, y)
            move = move + 1
            status = check_win(board)
            if played and not player:
                if not status:
                    player = True
                    rect =  p.draw.rect(screen, [0, 0, 0], (width/2 - 75, height//20 - 20, 150, 40))
                    p.display.update()

                else:
                    rect =  p.draw.rect(screen, [0, 0, 0], (width/2 - 75, height//20 - 20, 150, 40))
                    p.display.update()
                    # Erster Parameter bestimmt die Schriftart
                    # Zweiter Parameter bestimmt die Schriftgrösse
                    font = p.font.Font("freesansbold.ttf", 32)

                    if player:
                        # Text und koordinaten werden bestimmt
                        text = font.render(
                            "Gelb hat gewonnen!", True, (0, 255, 0), (0, 0, 255)
                        )
                        textRect = text.get_rect()
                        textRect.center = (180, height // 20)
                    else:
                        # Text und koordinaten werden bestimmt
                        text = font.render(
                            "Rot hat gewonnen!", True, (0, 255, 0), (0, 0, 255)
                        )
                        textRect = text.get_rect()
                        textRect.center = (160, height // 20)

                    # player wird auf None gesetzt, damit man nicht mehr setzen kann.
                    player = None
                    # Text wird gesetzt
                    screen.blit(text, textRect)

                    text = font.render("Neustarten", True, (0, 255, 0), (0, 0, 255))
                    textRect = text.get_rect()
                    textRect.center = (width - 110, height // 20)
                    screen.blit(text, textRect)

                if player is None:
                    position = p.mouse.get_pos()
                    # Es wird überprüft wo ob man auf "Neustarten" gedürckt hat
                    if textRect.x <= position[0] <= textRect.x + textRect.size[0]:
                        if textRect.y <= position[1] <= textRect.y + textRect.size[1]:
                            # Alle Werte werden zurückgesetzt, damit das Spiel von vorne beginnt
                            occupied = []
                            board = []
                            for n in range(42):
                                board.append("nnn")

                            move = 0
                            screen.fill(p.Color(0, 0, 0))
                            player = True

        if event.type == p.MOUSEBUTTONDOWN:
            if player:
                # In played wird gespeichert ob jemand gesetzt hat.
                played = put(p.mouse.get_pos()[0] // sizeOne)
                # Spielzug wird um 1 erhöht
                move = move + 1
                # In status wird gespeichert ob jemand gewonnen hat.
                status = check_win(board)
            if played and player:
                if not status:
                    if player:
                        # Spieler wird gewechselt
                        player = False
                        font = p.font.Font("freesansbold.ttf", 32)
                        wait = font.render("Warten!", True, (0, 255, 0), (0, 0, 255))
                        waitRect = wait.get_rect()
                        waitRect.center = (width / 2, height // 20)
                        screen.blit(wait, waitRect)
                    else:
                        # Spieler wird gewechselt
                        player = True

                # Jemand hat gewonnen
                else:
                    # Erster Parameter bestimmt die Schriftart
                    # Zweiter Parameter bestimmt die Schriftgrösse
                    font = p.font.Font("freesansbold.ttf", 32)

                    if player:
                        # Text und koordinaten werden bestimmt
                        text = font.render(
                            "Gelb hat gewonnen!", True, (0, 255, 0), (0, 0, 255)
                        )
                        textRect = text.get_rect()
                        textRect.center = (180, height // 20)
                    else:
                        # Text und koordinaten werden bestimmt
                        text = font.render(
                            "Rot hat gewonnen!", True, (0, 255, 0), (0, 0, 255)
                        )
                        textRect = text.get_rect()
                        textRect.center = (160, height // 20)

                    # player wird auf None gesetzt, damit man nicht mehr setzen kann.
                    player = None
                    # Text wird gesetzt
                    screen.blit(text, textRect)

                    text = font.render("Neustarten", True, (0, 255, 0), (0, 0, 255))
                    textRect = text.get_rect()
                    textRect.center = (width - 110, height // 20)
                    screen.blit(text, textRect)

            if player is None:
                position = p.mouse.get_pos()
                # Es wird überprüft wo ob man auf "Neustarten" gedürckt hat
                if textRect.x <= position[0] <= textRect.x + textRect.size[0]:
                    if textRect.y <= position[1] <= textRect.y + textRect.size[1]:
                        # Alle Werte werden zurückgesetzt, damit das Spiel von vorne beginnt
                        occupied = []
                        board = []
                        for n in range(42):
                            board.append("nnn")
                        move = 0
                        screen.fill(p.Color(0, 0, 0))
                        player = True

        # Das Feld wird gezeichnet
        drawGame()
p.quit()
