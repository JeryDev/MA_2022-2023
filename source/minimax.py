#NOCH IN ARBEIT

def get_index(number: int, l: list):
  for i in range(len(l)):
    try:
      if int(l[i][1]) == number:
        return i
    except(ValueError):
      pass

def get_Color(index: int, l: list, c: str):
  if index == -1:
    if c == "r":
      return "y"
    else:
      return "r"
  if index < len(l):
    return l[index][0]
  else:
    return "n"

def get_free_spaces(l: list):
  free_spaces = []
  for i in range(7):
    for k in range(6):
      v = i + ((5 - k) * 7)
      if l[v] == "nn":
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
      return ("up", "left", end - 8)
  if start - 7 == end:
    if end - 7 >= 0:
      return ("up", "middle", end - 7)
  if start - 6 == end:
    if end - 6 >= 0:
      return ("up", "right", end - 6)
  if start - 1 == end:
    if end - 1 >= 0:
      return ("middle", "left", end - 1)
  if start + 1 == end:
    return ("middle", "right", end + 1)
  if start + 6 == end:
    if end + 6 <= 41:
      return ("down", "left", end + 6)
  if start + 7 == end:
    if end + 7 <= 41:
      return ("down", "middle", end + 7)
  if start + 8 == end:
    if end + 8 <= 41:
      return ("down", "right", end + 8)
  
  return (None, None, -1)

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


def analyse(l: list, c: str, free_spaces: list):
  evaluation = []
  for i in range(len(free_spaces)):
    count = 0
    all_neighbours = get_all_neighbours(free_spaces[i])
    for j in range(len(all_neighbours)):
      color = get_Color(all_neighbours[j], l, c)
      if color == c:
        count = count + 10
        next_index = get_direction(free_spaces[i], all_neighbours[j])[2]
        color = get_Color(next_index, l, c)
        if color == c:
          count = count + 100
          next_index = get_direction(all_neighbours[j], next_index)[2]
          color = get_Color(next_index, l, c)
          if color == c:
            count = count + 10000
          elif color == "n":
            next_index = get_direction(all_neighbours[j], free_spaces[i])[2]
            color = get_Color(next_index, l, c)
            if color == c:
              count = count + 10000
          else:
            next_index = get_direction(all_neighbours[j], free_spaces[i])[2]
            color = get_Color(next_index, l, c)
            if color == c:
              count = count + 10000
        elif color == "n":
          next_index = get_direction(all_neighbours[j], next_index)[2]
          color = get_Color(next_index, l, c)
          if color == c:
            count = count + 100
      elif color == "n":
        next_index = get_direction(free_spaces[i], all_neighbours[j])[2]
        color = get_Color(next_index, l, c)
        if color == c:
          count = count + 10
          next_index = get_direction(all_neighbours[j], next_index)[2]
          color = get_Color(next_index, l, c)
          if color == c:
            count = count + 100
        elif color == "n":
          next_index = get_direction(all_neighbours[j], next_index)[2]
          color = get_Color(next_index, l, c)
          if color == c:
            count = count + 10

    if check_middle_position(free_spaces[i]):
      count = count + 40
    evaluation.append([count, free_spaces[i]])
  return evaluation




def minimax(l: list, l2: list, c: str, depth: int):
  x = get_free_spaces(l)
  if c == "y":
    best_index_offense = get_best_index(l, l2, x, depth, "y")
    best_index_defense = get_best_index(l, l2, x, depth, "r")
  else:
    best_index_offense = get_best_index(l, l2, x, depth, "r")
    best_index_defense = get_best_index(l, l2, x, depth, "y")

  if best_index_offense[0] >= best_index_defense[0]:
    return f"Index: {best_index_offense[1]} Wert: {best_index_offense[0]} -> OFFENCE (+{best_index_offense[0]- best_index_defense[0]})"
  else:
    return f"Index: {best_index_defense[1]} Wert: {best_index_defense[0]} -> DEFENCE (-{best_index_defense[0]- best_index_offense[0]})"

def get_best_index(l: list, l2: list, x: list, depth: int, c: str):
  if depth == 0:
    max = [0, 0]
    results = analyse(l, c, get_free_spaces(l))
    for i in range(len(results)):
      if results[i][0] > max[0]:
        max = results[i]
    return max
  
  if depth == 1:
    #Alle anderen Tiefen werden noch bearbeitet
    pass
  

l_from_Excel = [
  "nn", "nn", "nn", "nn", "nn", "nn", "nn",
  "nn", "nn", "nn", "nn", "nn", "nn", "nn",
  "nn", "nn", "nn", "rr", "nn", "nn", "nn",
  "nn", "nn", "nn", "yy", "nn", "nn", "nn",
  "nn", "nn", "nn", "rr", "nn", "nn", "nn",
  "nn", "nn", "nn", "yy", "nn", "nn", "nn"
]

l = []

for i in range(len(l_from_Excel)):
  l.append(l_from_Excel[i])

print(minimax(l, l_from_Excel, "y", 0))
