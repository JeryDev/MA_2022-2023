#NOCH IN ARBEIT
import math

def is_valid_direction(next_index: int, end: int):
  if get_row(end) + 1 <= 6 and get_row(end) + 1 == get_row(next_index):
    return True
  elif get_row(end) - 1 <= 1 and get_row(end) - 1 == get_row(next_index):
    return True
  elif get_column(end) + 1 <= 6 and get_column(end) + 1 == get_column(next_index):
    return True
  elif get_column(end) - 1 <= 1 and get_column(end) - 1 == get_column(next_index):
    return True
  else:
    return False

def get_row(index: int):
  return index // 7 + 1 

def get_column(index: int):
  return index % 7 + 1

def get_index(number: int, board: list):
  for i in range(len(board)):
    try:
      if int(board[i][1]) == number:
        return i
    except(ValueError):
      pass

def get_Color(index: int, board: list):
  try:
    if index < len(board):
      return board[index][0]
    else:
      return "n"
  except:
    print(f"Index is out of range! {index}")

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
  if index in (3, 10, 17, 24, 31, 38):
    return True
  else:
    return False

def get_direction(start: int, end: int):
  if start - 8 == end:
    if end - 8 >= 0:
      if is_valid_direction(end - 8, end):
        #up, left
        return end - 8
  if start - 7 == end:
    if end - 7 >= 0:
      if is_valid_direction(end - 7, end):
        #up, middle
        return end - 7
  if start - 6 == end:
    if end - 6 >= 0:
      if is_valid_direction(end - 6, end):
        #up, right
        return end - 6
  if start - 1 == end:
    if end - 1 >= 0:
      if is_valid_direction(end - 1, end):
        #middle, left
        return end - 1
  if start + 1 == end:
    if is_valid_direction(end + 1, end):
        #middle, right
        return end + 1
  if start + 6 == end:
    if end + 6 <= 41:
      if is_valid_direction(end + 6, end):
        #down, left
        return end + 6
  if start + 7 == end:
    if end + 7 <= 41:
      if is_valid_direction(end + 7, end):
        #down, middle
        return end + 7
  if start + 8 == end:
    if end + 8 <= 41:
      if is_valid_direction(end + 8, end):
        #down, right
        return end + 8
  
  return False

def get_all_neighbours(index: int):
  all_neighbours = []
  up = False
  right = False
  down = False
  left = False
  if (index - 7) // 7 >= 0:
    up = True
  if index // 7 == (index + 1) // 7:
    right = True
  if (index + 7) // 7 <= 5:
    down = True
  if index // 7 == (index - 1) // 7:
    left = True

  if up == True:
    all_neighbours.append(index - 7)
    if right == True:
      all_neighbours.append(index - 6)
    if left == True:
      all_neighbours.append(index - 8)
  if down == True:
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
      if neighbour:
        get_color_of_neighbour = get_Color(neighbour, board)
        if get_color_of_neighbour == color:
          value = value + 100
          neighbour = get_direction(all_neighbours[i], neighbour)
          if neighbour:
            get_color_of_neighbour = get_Color(neighbour, board)
            if get_color_of_neighbour == color:
              value = value + 10000
            else:
              neighbour = get_direction(all_neighbours[i], position)
              if neighbour:
                get_color_of_neighbour = get_Color(neighbour, board)
                if get_all_neighbours == color:
                  value = value + 10000
          else:
            neighbour = get_direction(all_neighbours[i], position)
            if neighbour:
              get_color_of_neighbour = get_Color(neighbour, board)
              if get_color_of_neighbour == color:
                value = value + 10000
        else:
          neighbour = get_direction(all_neighbours[i], position)
          if neighbour:
            get_color_of_neighbour = get_Color(neighbour, board)
            if get_color_of_neighbour == color:
              value = value + 100
              neighbour = get_direction(position, neighbour)
              if neighbour:
                get_color_of_neighbour = get_Color(neighbour, board)
                if get_color_of_neighbour == color:
                  value = value + 10000      
      else:
        neighbour = get_direction(all_neighbours[i], position)
        if neighbour:
          get_color_of_neighbour = get_Color(neighbour, board)
          if get_color_of_neighbour == color:
            value = value + 100
            neighbour = get_direction(position, neighbour)
            if neighbour:
              get_color_of_neighbour = get_Color(neighbour, board)
              if get_color_of_neighbour == color:
                value = value + 10000
  
  if check_middle_position(position):
    value = value + 4
  
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
  board[move] = f"{color}{board[move][1:]}"
  return board

def remove_move(board: list, move: int):
  board[move] = f"n{board[move][1:]}"
  return board


def minimax(board, position, depth, maxPlayer, color):
  if depth == 0 or check_win(board) != None:
    if depth == 0:
      return analyse(board, position, color), f"ERROR {color}"
    elif color == "y":
      return 10000, f"ERROR {color}"
    elif color == "r":
      return -10000, f"ERROR {color}"
  
  if maxPlayer:
    bestValue = -math.inf
    bestMove = -1
    for move in get_free_spaces(board):
      newBoard = make_move(board, move, "y")
      value = minimax(newBoard, move, depth - 1, False, "y")
      print(value[0])
      if bestValue < value[0]:
        bestMove = move
      bestValue = max(bestValue, value[0])
      newBoard = remove_move(newBoard, move)
    return bestValue, bestMove
  
  else:
    bestValue = math.inf
    for move in get_free_spaces(board):
      newBoard = make_move(board, move, "r")
      value = minimax(newBoard, move, depth - 1, True, "r")
      if bestValue > value[0]:
        bestMove = move
      bestValue = min(bestValue, value[0])
      newBoard = remove_move(newBoard, move)
    print("RETURN" + f"{bestValue}")
    return bestValue, bestMove


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
if color == "y":
  maxPlayer = True
else:
  maxPlayer = False

depth = 3

results = minimax(board_to_use, -1, depth, maxPlayer, "y")



print(f"Der Beste Zug ist bei Index: {results[1]}")
print(f"V: {results[0]}")
