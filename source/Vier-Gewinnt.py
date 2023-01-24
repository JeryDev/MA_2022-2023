# Vier-Gewinnt Python-Programm (pygame) von Jery:

# Wichtig:
# In diesem Programm kann pro Start nur eine Partie gespielt werden.
# Dieses Programm dient zur Veranschaulichung wie ein normales Vier-Gewinnt Programm funktioniert.
# Dies ist die Basis für die nächsten Programme.

# pygame Import
import pygame as p

p.init()

# Size definiert die grösse des ganzen Feldes bzw. des Fensters.
size = 1050

# Grösse von einem Feld
sizeOne = int(size / 7)

width = size
height = size

# Hier werden die Grössen eingetragen.
screen = p.display.set_mode((width, height))

# Fensterbeschriftung
p.display.set_caption("4-Gewinnt")

# Liste, welche die besetzten Felder speichert
occupied = []

# Liste, welche das aktuelle Feld speichert
field = []

# Leeres Feld wird generiert
for n in range(42):
    field.append("nnn")

#Aktueller Spielzug
move = 0

#Int wird in einen gültigen String umgewandelt
def moveSyntax(move):
    if move < 10:
        move = "0" + str(move)
        return move
    else:
        return str(move)

# Die Spielfläche wird gezeichnet
def drawGame():
    for i in range(8):
        p.draw.line(screen, [255, 255, 255], [0, i * sizeOne + sizeOne - 2.5], [size, i * sizeOne + sizeOne - 2.5], 5)
        p.draw.line(screen, [255, 255, 255], [i * sizeOne, sizeOne], [i * sizeOne, size], 5)


# Ein gelder oder roter Kreis wird gezeichnet
def drawBall(x, y):
    if player:
        color = [255, 255, 0]
    else:
        color = [255, 0, 0]
    p.draw.circle(screen, color, [x, y], sizeOne / 2 - 5)


# Hier werden die Koordinaten geprüft und verarbeitet.
# Es wird nach dem nächst freien Feld ein einer Spalte gesucht.
# Schlussendlich werden die verarbeiteten Daten in den Listen occupied und field gespeichert.
def put():
    column = p.mouse.get_pos()[0] // sizeOne
    i = 35
    inColumn = False
    while i >= 0:
        if (i + column) not in occupied:
            occupied.append(i + column)
            if player:
                field[i + column] = "y" + moveSyntax(move)
            else:
                field[i + column] = "r" + moveSyntax(move)
            inColumn = True
            x = column * sizeOne + (sizeOne / 2)
            y = (i // 7) * sizeOne + (sizeOne * 1.5)
            drawBall(x, y)
            break
        else:
            i = i - 7

    return inColumn


# Hier wird überprüft ob es bereits 4 gleiche Kreise in einer Reihe hat.
def checkWin():

    # Boolean: True = (Jemand hat gewonnen) False = (Niemand hat gewonnen)
    won = False

    # Überprüfung: Horizontal (rechts, links)
    for row in range(6):
        yellowInRow = 0
        redInRow = 0
        for column in range(7):
            if field[column + row * 7][0] == "r":
                redInRow = redInRow + 1
                yellowInRow = 0
            elif field[column + row * 7][0] == "y":
                yellowInRow = yellowInRow + 1
                redInRow = 0
            else:
                yellowInRow = 0
                redInRow = 0
            if redInRow == 4:
                won = True
                break
            if yellowInRow == 4:
                won = True
                break

    # Überprüfung: Vertikal (oben / unten)
    for column in range(7):
        yellowInRow = 0
        redInRow = 0
        for row in range(6):
            if field[column + row * 7][0] == "r":
                redInRow = redInRow + 1
                yellowInRow = 0
            elif field[column + row * 7][0] == "y":
                yellowInRow = yellowInRow + 1
                redInRow = 0
            else:
                yellowInRow = 0
                redInRow = 0
            if redInRow == 4:
                won = True
                break
            if yellowInRow == 4:
                won = True
                break

    # Überprüfung: Diagonal (rechts unten / links oben)
    for row in range(3):
        for column in range(4):
            yellowInRow = 0
            redInRow = 0
            for diagonal in range(4):
                if field[column + row * 7 + diagonal * 8][0] == "r":
                    redInRow = redInRow + 1
                    yellowInRow = 0
                elif field[column + row * 7 + diagonal * 8][0] == "y":
                    yellowInRow = yellowInRow + 1
                    redInRow = 0
                else:
                    yellowInRow = 0
                    redInRow = 0
                if redInRow == 4:
                    won = True
                    break
                if yellowInRow == 4:
                    won = True
                    break

    # Überprüfung: Diagonal (rechts oben / links unten)
    for row in range(3):
        for column in range(4):
            yellowInRow = 0
            redInRow = 0
            for diagonal in range(4):
                if field[column + 3 + row * 7 + diagonal * 6][0] == "r":
                    redInRow = redInRow + 1
                    yellowInRow = 0
                elif field[column + 3 + row * 7 + diagonal * 6][0] == "y":
                    yellowInRow = yellowInRow + 1
                    redInRow = 0
                else:
                    yellowInRow = 0
                    redInRow = 0
                if redInRow == 4:
                    won = True
                    break
                if yellowInRow == 4:
                    won = True
                    break
    return won


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
        if event.type == p.MOUSEBUTTONDOWN:
            if player is not None:
                # In played wird gespeichert ob jemand gesetzt hat.
                played = put()
                #Spielzug wird um 1 erhöht
                move = move + 1
                # In status wird gespeichert ob jemand gewonnen hat.
                status = checkWin()

            if played and player is not None:
                if not status:
                    if player:
                        # Spieler wird gewechselt
                        player = False
                    else:
                        # Spieler wird gewechselt
                        player = True

                # Jemand hat gewonnen
                else:
                    # Erster Parameter bestimmt die Schriftart
                    # Zweiter Parameter bestimmt die Schriftgrösse
                    font = p.font.Font('freesansbold.ttf', 32)

                    if player:
                        # Text und koordinaten werden bestimmt
                        text = font.render('Gelb hat gewonnen!', True, (0, 255, 0), (0, 0, 255))
                        textRect = text.get_rect()
                        textRect.center = (180, height // 20)
                    else:
                        # Text und koordinaten werden bestimmt
                        text = font.render('Rot hat gewonnen!', True, (0, 255, 0), (0, 0, 255))
                        textRect = text.get_rect()
                        textRect.center = (160, height // 20)

                    # player wird auf None gesetzt, damit man nicht mehr setzen kann.
                    player = None
                    # Text wird gesetzt
                    screen.blit(text, textRect)

                    text = font.render('Neustarten', True, (0, 255, 0), (0, 0, 255))
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
                        field = []
                        for n in range(42):
                            field.append("nnn")
                        move = 0
                        screen.fill(p.Color(0, 0, 0))
                        player = True

        # Das Feld wird gezeichnet
        drawGame()

p.quit()
