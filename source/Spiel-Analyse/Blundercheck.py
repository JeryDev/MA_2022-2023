import pygame as p
import os
import json
import openpyxl as xl

# Initialisierungsfunktion
p.init()

# Pfade für die nötigen Dateien
file_path_xlsx = "/Users/jerykuster/Desktop/Datensammlung/Maturaarbeit_Jery/data.xlsx"
file_path_config = "/Users/jerykuster/Desktop/Datensammlung/Maturaarbeit_Jery/config.json"

# Titel der Mappe -> Format: Spieler1 vs Spieler2
# sheet_name = str(input("Geben Sie einen Titel ein: "))
# gameID = int(input("Geben Sie die GameID ein: "))
sheet_name = "Mischa vs Jery"
gameID = 0


# Werte aus Excel abrufen
def getValue(row: int, column: int, worksheet):
    return worksheet.cell(row=row, column=column).value


# Überprüfen ob es die Excel Datei bereits gibt
# Wenn nicht dann einen neuen Datei anlegen mit Standardwert
if not os.path.isfile(file_path_xlsx):
    exit("Diese Datei gibt es nicht!")

workbook = xl.load_workbook(file_path_xlsx)

# Mappe abrufen
try:
    worksheet = workbook[sheet_name]
except KeyError:
    exit("Diese Mappe existiert nicht!")

# Überprüfen ob es die Konfigurationsdatei bereits gibt
# Wenn nicht dann einen neuen Datei anlegen mit Standardwert
if not os.path.isfile(file_path_config):
    data = {"size": 800}
    with open(file_path_config, "w") as file:
        json.dump(data, file, indent=1)

# Die Konfigurationsdatei öffnen
f = open(file_path_config)

# Konfigurationsdatei in ein Dictionary umwandeln
data = json.load(f)

# Den "Size" Parameter abrufen
size = data["size"]
f.close()

# Grösse von einem Feld bestimmen
sizeOne = int(size / 7)

width = size
height = size

# Hier werden die Grössen eingetragen.
screen = p.display.set_mode((width, height))

# Fensterbeschriftung
p.display.set_caption(
    f"Vier-Gewinnt | BLUNDERCHECK GameID: {gameID} | Players: {sheet_name}"
)

# Liste, welche von Excel übernommen wurde
board_from_excel = []
for i in range(1, 7):
    for j in range(1, 8):
        board_from_excel.append(str(getValue(i + gameID * 14, j, worksheet)))

# Liste, welche das aktuelle Feld speichert
board = []

# Leeres Feld wird generiert
for n in range(42):
    board.append("nnn")

# Aktueller Spielzug
move = 0

# Maximale Anzahl Moves:
maxMoves = int(getValue(12 + gameID * 14, 5, worksheet) - 1)


def difference(num1: int, num2: int):
    """
    Berechnet die Differenz von zwei Zahlen

    Args:
        num1: Erste Zahl
        num2: Zweite Zahl

    Returns:
        diff: Differenz der Zahlen
    """
    if num1 > num2:
        diff = num1 - num2
    else:
        diff = num2 - num1

    return diff


def getAccuracy(move: int, maxValue: int, minValue: int, color: str):
    """
    Überprüft die Qualität des Zuges

    Args:
        move: Repräsentiert den Wert des Zuges
        best: Repräsentiert den bestmöglichen Wert
        worst: Repräsentiert den schlechtesten Wert

    Returns:
        accuracy: Qualität des Zuges
    """
    if color == "y":
        spectrum = difference(maxValue, minValue)
        value = difference(move, minValue)
        if spectrum > 0:
            accuracy = 100 / spectrum * value
        else:
            accuracy = 100
        return round(accuracy, 3)
    elif color == "r":
        spectrum = difference(maxValue, minValue)
        value = difference(move, maxValue)
        if spectrum > 0:
            accuracy = 100 / spectrum * value
        else:
            accuracy = 100
        return round(accuracy, 3)


def isBlunder(accuracy, maxValue, minValue, move, color):
    """
    Überpüft, ob ein Zug ein Blunder ist

    Args:
        accuracy: Die Qualität des Zuges in Prozent
        maxValue: Der grösste Wert von allen möglichen Zügen
        minValue: Der kleinste Wert von allen möglichen Zügen
        move: Repräsentiert den Wert des Zuges (Nicht in Prozent)

    Returns:
        0: Kein Blunder
        1: Blunder
    """
    spectrum = difference(maxValue, minValue)

    # Verpasster Gewinn (Gelb)
    if color == "y" and maxValue >= 9996 and move < 9996:
        return "Verpasster Gewinn (Gelb)"
    # Verpasster Gewinn (Rot)
    if color == "r" and minValue <= -9996 and move > -9996:
        return "Verpasster Gewinn (Rot)"
    # Gewinnchance für Rot
    if color == "y" and minValue <= -9996 and maxValue > -9996 and move <= -9996:
        return "Gewinnchance für Rot"
    # Gewinnchance für Gelb
    if color == "r" and maxValue >= 9996 and minValue < 9996 and move >= 9996:
        return "Gewinnchance für Gelb"
    # Verpasster Zug
    if accuracy < 10 and spectrum >= 200:
        return "Verpasster Zug"
    # Kein Blunder
    else:
        return "Kein Blunder"


def isValidDirection(next_index: int, end: int, direction: str):
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
        if getRow(end) + 1 == getRow(next_index):
            # Der nächste Index ist eine Zeile darunter
            return True
        elif getRow(end) - 1 == getRow(next_index):
            # Der nächste Index ist eine Zeile darüber
            return True
    elif direction == "horizontal":
        if getColumn(end) + 1 == getColumn(next_index):
            # Der nächste Index ist eine Spalte rechts
            return True
        elif getColumn(end) - 1 == getColumn(next_index):
            # Der nächste Index ist eine Spalte links
            return True
    elif direction == "diagonal":
        if getRow(end) + 1 == getRow(next_index) and getColumn(
            end
        ) + 1 == getColumn(next_index):
            # Der nächste Index ist diagonal unten rechts
            return True
        elif getRow(end) - 1 == getRow(next_index) and getColumn(
            end
        ) - 1 == getColumn(next_index):
            # Der nächste Index ist diagonal oben links
            return True
        elif getRow(end) + 1 == getRow(next_index) and getColumn(
            end
        ) - 1 == getColumn(next_index):
            # Der nächste Index ist diagonal unten links
            return True
        elif getRow(end) - 1 == getRow(next_index) and getColumn(
            end
        ) + 1 == getColumn(next_index):
            # Der nächste Index ist diagonal oben rechts
            return True
    # Der nächste Index ist in keiner der erlaubten Richtungen gültig.
    return False


def getRow(index: int):
    """
    Gibt die Zeile zurück, in der sich der gegebene Index befindet.

    Args:
        index: Der Index, dessen Zeile zurückgegeben werden soll.

    Returns:
        Die Zeile, in der sich der gegebene Index befindet.
    """
    return index // 7 + 1


def getColumn(index: int):
    """
    Gibt die Spalte zurück, in der sich der gegebene Index befindet.

    Args:
        index: Der Index, dessen Spalte zurückgegeben werden soll.

    Returns:
        Die Spalte, in der sich der gegebene Index befindet.
    """
    return index % 7 + 1


def getColor(index: int, board: list):
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

def getFreePositions(board: list):
    """
    Gibt eine Liste von Indexe zurück, die auf freie Plätze auf dem Spielbrett verweisen.

    Args:
        board: Eine Liste, die das Spielbrett repräsentiert.

    Returns:
        Eine Liste von Indexe, die auf freie Plätze auf dem Spielbrett verweisen.
    """
    free_positions = []
    for i in range(7):
        for k in range(6):
            # Berechnung des Index des Elements in der aktuellen Spalte und Zeile.
            v = i + ((5 - k) * 7)
            if board[v][0] == "n":
                free_positions.append(v)
                break
    return free_positions


def isMiddle(index: int):
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


def getDirection(start: int, end: int):
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
        if isValidDirection(next_index, end, direction) and 0 <= next_index <= 41:
            return next_index  # Der nächste Index wird zurückgegeben.
    # Wenn die Richtung ungültig ist oder der nächste Index außerhalb des Spielbretts liegt, wird False zurückgegeben.
    return False

def translateBoard(board):
    """
    Wandelt das Brett in ein neues Format um

    Args:
        board: Aktuelles Brett

    Returns:
        Umgewandltes Brett
    """
    rl = []
    for i in range(len(board)):
        rl.append(board[i][0])

    tl = []
    for i in range(6):
        v1 = 7*i
        v2 = 7*i+7
        tl.append(rl[v1:v2])
    
    return tl

def getScore(window: str):
    """
    Berechnet die Punkte

    Args:
        window: Viererreihe aus dem Board

    Returns:
        Punkte
    """
    countY = window.count("y")
    countR = window.count("r")
    countN = window.count("n")

    if countY + countN == 4 and countY > 0:
        if countY == 1:
            return 1
        elif countY == 2:
            return 10
        elif countY == 3:
            return 100
        else:
            return 10000
    if countR + countN == 4 and countR > 0:
        if countR == 1:
            return -1
        elif countR == 2:
            return -10
        elif countR == 3:
            return -100
        else:
            return -10000
    return 0

def evaluate(board):
    translatedBoard = translateBoard(board)

    # Wertung des Spielbretts
    score = 0

    # Horizontal
    for row in range(6):
        for col in range(4):
            window = translatedBoard[row][col : col + 4]
            window_string = "".join(window)
            score += getScore(window_string)

    # Vertikal
    for col in range(7):
        for row in range(3):
            window = [translatedBoard[row + i][col] for i in range(4)]
            window_string = "".join(window)
            score += getScore(window_string)

    # Diagonal (von links oben nach rechts unten)
    for row in range(3):
        for col in range(4):
            window = [translatedBoard[row + i][col + i] for i in range(4)]
            window_string = "".join(window)
            score += getScore(window_string)

    # Diagonal (von rechts oben nach links unten)
    for row in range(3):
        for col in range(3, 7):
            window = [translatedBoard[row + i][col - i] for i in range(4)]
            window_string = "".join(window)
            score += getScore(window_string)

    return score


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

    return None


def makeMove(board: list, move: int, color: str):
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


def getResults(board: list, depth: int, color: str, alpha: int, beta: int):
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
    for position in getFreePositions(board):
        # Führe den Spielzug aus und berechne den Bewertungswert des Spielbretts
        newBoard = makeMove(board, position, color)
        if color == "y":
            maxPlayer = False
            value = minimax(newBoard, depth - 1, maxPlayer, alpha, beta)
            # Füge einen Bonus hinzu, wenn der Spielzug in der Mitte der untersten Reihe erfolgt
            if isMiddle(position):
                value = value + 4
        elif color == "r":
            maxPlayer = True
            value = minimax(newBoard, depth - 1, maxPlayer, alpha, beta)
            # Ziehe einen Malus ab, wenn der Spielzug in der Mitte der untersten Reihe erfolgt
            if isMiddle(position):
                value = value - 4

        # Füge den Bewertungswert des Spielzugs und seine Position der Ergebnisliste hinzu
        results.append([value, position])

    # Gibt die Ergebnisliste zurück
    values = []
    for i in range(len(results)):
        values.append(results[i][0])
    positions = []
    for i in range(len(results)):
        positions.append(results[i][1])
    return values, positions


def minimax(
    board: list, depth: int, maxPlayer: bool, alpha: int, beta: int
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
    winner = checkWin(board)
    if depth == 0 or winner != None:
        # Falls Gelb gewonnen hat, gib 10000 zurück
        if winner == "yellow":
            return 10000
        # Falls Rot gewonnen hat, gib -10000 zurück
        elif winner == "red":
            return -10000
        # Falls die maximale Tiefe erreicht wurde, berechne den Wert des aktuellen Boards und gib ihn zurück
        return evaluate(board)

    # Wenn der maximierende Spieler am Zug ist
    if maxPlayer:
        bestValue = -1000000
        # Für jeden möglichen Zug
        for move in getFreePositions(board):
            # Mach den Zug auf dem Board
            newBoard = makeMove(board, move, "y")
            # Berechne den Wert des Zuges mit Hilfe des Minimax-Algorithmus
            value = minimax(newBoard, depth - 1, False, alpha, beta)
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
        for move in getFreePositions(board):
            # Mach den Zug auf dem Board
            newBoard = makeMove(board, move, "r")
            # Berechne den Wert des Zuges mit Hilfe des Minimax-Algorithmus
            value = minimax(newBoard, depth - 1, True, alpha, beta)
            # Wenn der berechnete Wert besser als der aktuelle beste Wert ist, aktualisiere den besten Wert
            bestValue = min(bestValue, value)
            # Aktualisiere den Beta-Wert
            beta = min(beta, bestValue)
            # Wenn der Beta-Wert kleiner als oder gleich dem Alpha-Wert ist, breche die Schleife ab
            if beta <= alpha:
                break
        # Gib den besten Wert zurück
        return bestValue


def moveSyntax(move: int):
    """
    Wandelt in ein gültiges Stringformat um

    Args:
        move: Repräsentiert den Zug

    Returns:
        Umgewandeltes Stringformat
    """
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
def drawBall(x, y, color):
    if color == None:
        if player:
            color = [255, 255, 0]
        else:
            color = [255, 0, 0]
    p.draw.circle(screen, color, [x, y], sizeOne / 2 - 5)

def putAll(board: list, move: int):
    drawGame()
    for i in range(move-1):
        if i % 2 == 0:
            index = board.index(f"y{moveSyntax(i)}")
            x = getColumn(index) * sizeOne - (sizeOne / 2)
            y = getRow(index) * sizeOne + (sizeOne / 2)
            drawBall(x, y, [255, 255, 0])
        else:
            index = board.index(f"r{moveSyntax(i)}")
            x = getColumn(index) * sizeOne - (sizeOne / 2)
            y = getRow(index) * sizeOne + (sizeOne / 2)
            drawBall(x, y, [255, 0, 0])


# Hier werden die Koordinaten geprüft und verarbeitet.
# Es wird nach dem nächst freien Feld ein einer Spalte gesucht.
# Schlussendlich werden die verarbeiteten Daten in den Listen occupied und board gespeichert.
def put(index: int, board: list, move: int):
    p.draw.rect(screen, [0, 0, 0], (width / 2 - 75, height // 20 - 20, 150, 40))
    font = p.font.Font("freesansbold.ttf", 32)
    wait = font.render("Warten!", True, (0, 255, 0), (0, 0, 255))
    waitRect = wait.get_rect()
    waitRect.center = (width / 2, 10 + waitRect.centery)
    screen.blit(wait, waitRect)
    p.display.update()

    if move % 2 == 0:
        values, positions = getResults(board, 7, "y", -1000000, 1000000)
        current = values[positions.index(index)]
        for i in range(6):
            print(board[i*7:i*7+7])
        print(f"V: {values}")
        print(f"P: {positions}")
        print(f"C: {current}")
        accuracy = getAccuracy(current, max(values), min(values), "y")
        blunder = isBlunder(accuracy, max(values), min(values), current, "y")
    else:
        values, positions = getResults(board, 7, "r", -1000000, 1000000)
        current = values[positions.index(index)]
        for i in range(6):
            print(board[i*7:i*7+7])
        print(f"V: {values}")
        print(f"P: {positions}")
        print(f"C: {current}")
        accuracy = getAccuracy(current, max(values), min(values), "r")
        blunder = isBlunder(accuracy, max(values), min(values), current, "r")

    x = getColumn(index) * sizeOne - (sizeOne / 2)
    y = getRow(index) * sizeOne + (sizeOne / 2)
    drawBall(x, y, None)
    screen.fill([0, 0, 0], waitRect)
    return accuracy, blunder


# Boolean: True = (Das Spiel ist am laufen) False = (Das Spiel ist nicht mehr am laufen)
online = True

# Boolean: True = (Gelber Spieler) False = (Roter Spieler)
player = True

accuracy = "None"

blunder = "Kein Blunder"

# Solange das Spiel online ist, sollte es dauernd das Feld überprüfen.
while online:
    for event in p.event.get():
        if event.type == p.QUIT:
            # Spiel wird beendet
            online = False

        font = p.font.Font("freesansbold.ttf", 32)

        text = font.render("Verlassen", True, (0, 255, 0), (0, 0, 255))
        textRect = text.get_rect()
        textRect.x = width - 2 * textRect.centerx - 10
        textRect.y = 10
        screen.blit(text, textRect)

        if move > 1:
            previous = font.render(" < ", True, (0, 255, 0), (0, 0, 255))
        else:
            previous = font.render(" X ", True, (0, 255, 0), (0, 0, 255))
        previousRect = previous.get_rect()
        previousRect.x = 10
        previousRect.y = 10
        screen.blit(previous, previousRect)

        if move <= maxMoves:
            next = font.render(" > ", True, (0, 255, 0), (0, 0, 255))
        else:
            next = font.render(" X ", True, (0, 255, 0), (0, 0, 255))
        nextRect = next.get_rect()
        nextRect.x = 50
        nextRect.y = 10
        screen.blit(next, nextRect)

        font = p.font.Font("freesansbold.ttf", 16)
        acc = font.render(
            f"Qualität des Zuges: {accuracy}%", True, (0, 255, 0), (0, 0, 255)
        )
        accRect = acc.get_rect()
        accRect.x = 10
        accRect.y = 75
        screen.blit(acc, accRect)

        if blunder[0:2] == "BL":
            print(blunder)
            blunder = "Blunder: Siehe Output!"
        blu = font.render(str(blunder), True, (0, 255, 0), (0, 0, 255))
        bluRect = blu.get_rect()
        bluRect.x = 250
        bluRect.y = 75
        screen.blit(blu, bluRect)

        if event.type == p.MOUSEBUTTONDOWN:
            position = p.mouse.get_pos()
            Next = False
            Previous = False
            # Es wird überprüft wo ob man auf "Neustarten" gedürckt hat
            if textRect.x <= position[0] <= textRect.x + textRect.size[0]:
                if textRect.y <= position[1] <= textRect.y + textRect.size[1]:
                    exit("Blundercheck beendet!")

            if nextRect.x <= position[0] <= nextRect.x + nextRect.size[0]:
                if nextRect.y <= position[1] <= nextRect.y + nextRect.size[1]:
                    Next = True

            if previousRect.x <= position[0] <= previousRect.x + previousRect.size[0]:
                if previousRect.y <= position[1] <= previousRect.y + previousRect.size[1]:
                    Previous = True

            if Next and move <= maxMoves:
                screen.fill([0, 0, 0])
                putAll(board, move+1)
                drawGame()
                # In played wird gespeichert ob jemand gesetzt hat.
                if move % 2 == 0:
                    index = board_from_excel.index(f"y{moveSyntax(move)}")
                else:
                    index = board_from_excel.index(f"r{moveSyntax(move)}")
                accuracy, blunder = put(index, board, move)
                
                if move % 2 == 0:
                    board[index] = f"y{moveSyntax(move)}"
                else:
                    board[index] = f"r{moveSyntax(move)}"

                # Spielzug wird um 1 erhöht
                move = move + 1
                screen.fill([0, 0, 0], accRect)
                screen.fill([0, 0, 0], bluRect)
                if player:
                    player = False
                else:
                    player = True
            if Previous and move > 1:
                screen.fill([0, 0, 0])
                move = move - 1
                # In played wird gespeichert ob jemand gesetzt hat.
                if move % 2 == 0:
                    index = board_from_excel.index(f"y{moveSyntax(move)}")
                    board[index] = "nnn"
                    index = board_from_excel.index(f"r{moveSyntax(move-1)}")
                    board[index] = "nnn"
                else:
                    index = board_from_excel.index(f"r{moveSyntax(move)}")
                    board[index] = "nnn"
                    index = board_from_excel.index(f"y{moveSyntax(move-1)}")
                    board[index] = "nnn"
                for i in range(6):
                    print(board[i*7:i*7+7])
                putAll(board, move)
                move = move - 1
                accuracy, blunder = put(index, board, move)
                
                if move % 2 == 0:
                    board[index] = f"y{moveSyntax(move)}"
                else:
                    board[index] = f"r{moveSyntax(move)}"
                
                move = move + 1
                # Spielzug wird um 1 erhöht
                screen.fill([0, 0, 0], accRect)
                screen.fill([0, 0, 0], bluRect)
                if player:
                    player = False
                else:
                    player = True

        # Das Fenster wird neugeladen
        p.display.update()
            

        # Das Feld wird gezeichnet
        drawGame()

p.quit()
