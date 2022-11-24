#Vier-Gewinnt Python-Programm (pygame) von Jery:

#Wichtig:
#In diesem Programm kann pro Start nur eine Partie gespielt werden.
#Dieses Programm dient zur Veranschaulichung wie ein normales Vier-Gewinnt Programm funktioniert.
#Dies ist die Basis für die nächsten Programme.
#Dies ist die unkommentierte Version.

import pygame as p

p.init()

size = 1050
width = size
height = size
screen = p.display.set_mode((width, height))
p.display.set_caption("4-Gewinnt")

occupied = []
field = []

for n in range(42):
    field.append(" ")


def drawGame():
    for i in range(8):
        p.draw.line(screen, [255, 255, 255], [0, i * 150 + 147.5], [size, i * 150 + 147.5], 5)
        p.draw.line(screen, [255, 255, 255], [i * 150, 150], [i * 150, size], 5)


def drawBall(x, y):
    if player:
        color = [255, 255, 0]
    else:
        color = [255, 0, 0]
    p.draw.circle(screen, color, [x, y], 70)


def put():
    column = p.mouse.get_pos()[0] // 150
    i = 35
    inColumn = False
    while i >= 0:
        if i + column not in occupied:
            occupied.append(i + column)
            if player:
                field[i + column] = "y"
            else:
                field[i + column] = "r"
            inColumn = True
            x = column * 150 + 75
            y = i // 7 * 150 + 225
            drawBall(x, y)
            break
        else:
            i = i - 7

    return inColumn


def checkWin():
    redInRow = 0
    yellowInRow = 0
    won = False
    for row in range(6):
        for column in range(7):
            if field[column + row * 7] == "r":
                redInRow = redInRow + 1
                yellowInRow = 0
            elif field[column + row * 7] == "y":
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

    for column in range(7):
        for row in range(6):
            if field[column + row * 7] == "r":
                redInRow = redInRow + 1
                yellowInRow = 0
            elif field[column + row * 7] == "y":
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

    for row in range(3):
        for column in range(4):
            for diagonal in range(4):
                if field[column + row * 7 + diagonal * 8] == "r":
                    redInRow = redInRow + 1
                    yellowInRow = 0
                elif field[column + row * 7 + diagonal * 8] == "y":
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

    for row in range(3):
        for column in range(4):
            for diagonal in range(4):
                if field[column + 3 + row * 7 + diagonal * 6] == "r":
                    redInRow = redInRow + 1
                    yellowInRow = 0
                elif field[column + 3 + row * 7 + diagonal * 6] == "y":
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


online = True

player = True

while online:
    for event in p.event.get():
        if event.type == p.QUIT:
            online = False

        p.display.update()
        drawGame()
        if event.type == p.MOUSEBUTTONDOWN:
            if player is not None:
                played = put()
                status = checkWin()

            if played and player is not None:
                if not status:
                    if player:
                        player = False
                    else:
                        player = True
                else:
                    if player:
                        print("Gelb hat gewonnen!")
                    else:
                        print("Rot hat gewonnen!")

                    player = None
                    print("Spiel ist vorbei!")

p.quit()
