import time

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
              value = 10000
            else:
              neighbour = get_direction(all_neighbours[i], position)
              if neighbour:
                get_color_of_neighbour = get_Color(neighbour, board)
                if get_all_neighbours == color:
                  value = 10000
          else:
            neighbour = get_direction(all_neighbours[i], position)
            if neighbour:
              get_color_of_neighbour = get_Color(neighbour, board)
              if get_color_of_neighbour == color:
                value = 10000
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
                  value = 10000     
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



def minimax(board: list, position: int, depth: int, maxPlayer: bool, color: str, depth_safe: int):
  if depth == 0 or check_win(board) != None:
    if check_win(board):
      if color == "y":
        return 10000
      elif color == "r":
        return -10000
    if depth == 0:
      return analyse(board, position, color)
  
  if maxPlayer:
    bestValue = -100000
    bestMove = None
    for move in get_free_spaces(board):
      newBoard = make_move(board, move, "y")
      value = minimax(newBoard, move, depth - 1, False, "y", depth_safe)
      if bestValue <= value:
        if check_middle_position(move) and depth == depth_safe:
          value = value + 4
        bestMove = move
      bestValue = max(bestValue, value)
      
    if depth == depth_safe:
      return bestValue, bestMove
    else:
      return bestValue
  
  else:
    bestValue = 100000
    bestMove = None
    for move in get_free_spaces(board):
      newBoard = make_move(board, move, "r")
      value = minimax(newBoard, move, depth - 1, True, "r", depth_safe)
      if bestValue >= value:
        if check_middle_position(move) and depth == depth_safe:
          value = value - 4
        bestMove = move
      bestValue = min(bestValue, value)
    if depth == depth_safe:
      return bestValue, bestMove
    else:
      return bestValue


board_from_Excel = [
   "n00", "n01", "n02", "n03", "n04", "n05", "n06",
   "n07", "n08", "n09", "n10", "n11", "n12", "n13",
   "n14", "n15", "n16", "n17", "n18", "n19", "n20",
   "n21", "n22", "n23", "n24", "n25", "n26", "n27",
   "n28", "n29", "n30", "n31", "n32", "n33", "n34",
   "n35", "n36", "n37", "y38", "n39", "n40", "n41"
   ]

board_to_use = []

for i in range(len(board_from_Excel)):
  board_to_use.append(board_from_Excel[i])


color = "y"
if color == "y":
  maxPlayer = True
else:
  maxPlayer = False

depth = 4
depth_safe = depth

StartTime = time.time()
results = minimax(board_to_use, 38, depth, maxPlayer, color, depth_safe)

EndTime = time.time()
print(f"Best Index: {results[1]}")
print(f"Value: {results[0]}")
print(f"Time: {round(EndTime - StartTime, 2)} Seconds")
