from utils.tools import GetState


def FutureReward(game_engin, move, q_table):
    table = q_table.table
    scores = None
    x_head, y_head = game_engin.snake_head
    new_x_head = x_head + 1 if move == 'down' else x_head - 1 if move == 'up' else x_head
    new_y_head = y_head + 1 if move == 'right' else y_head - 1 if move == 'left' else y_head

    new_state = GetState(game_engin.map, (new_x_head, new_y_head), game_engin.n_cells)
    if new_state in table:
        scores = table[new_state]
        return max(scores['up'], scores['down'], scores['right'], scores['left'])
    else:
        return 0


def InstantReward(game_engin, move):
    reward = CellType(game_engin, move)
#    if DodgeRed(game_engin, move) == True:
#        reward +=  

    if AppleInDirection(game_engin, move) == True:
        reward += 50

    if AvoidingGreen(game_engin, move) == True:
        reward -= 100

    if NextToWall(game_engin, move) == True:
        reward -= 20
#
    if InMapCorner(game_engin, move) == True:
        reward -= 30

#    if DiscoverGreen(game_engin, move) == True:
#        reward += 10
#
#    if SnakeBlocked(map, snake_head, snake_tail) == True:
#        reward -= 40
#
#    if SnakeNotBlocked(map, snake_head, snake_tail) == True:
#        reward += 40
    return reward


def CellType(game_engin, move):
    map = game_engin.map
    x_head, y_head = game_engin.snake_head
    new_x_head = x_head + 1 if move == 'down' else x_head - 1 if move == 'up' else x_head
    new_y_head = y_head + 1 if move == 'right' else y_head - 1 if move == 'left' else y_head

    if map[new_x_head][new_y_head] == 'G':
        return 100
    elif map[new_x_head][new_y_head] == 'R':
        return -50
    elif map[new_x_head][new_y_head] == '0':
        return -2
    elif map[new_x_head][new_y_head] == 'W' or map[new_x_head][new_y_head] == 'S':
        return -1000
    return 0



def AppleInDirection(game_engin, move):
    map = game_engin.map
    x_head, y_head = game_engin.snake_head

    if move == 'up':
        for c in range(x_head - 1, 0, -1):
            if map[c][y_head] == 'G':
                return True

    if move == 'down':
        for c in range(x_head + 1, game_engin.n_cells + 2, 1):
            if map[c][y_head] == 'G':
                return True

    if move == 'left':
        for c in range(y_head - 1, 0, -1):
            if map[x_head][c] == 'G':
                return True

    if move == 'right':
        for c in range(y_head + 1, game_engin.n_cells + 2, 1):
            if map[x_head][c] == 'G':
                return True
    return False



def AvoidingGreen(game_engin, move):
    map = game_engin.map
    x_snake, y_snake = game_engin.snake_head

    if AppleInDirection(game_engin, move) == False:
        if move == 'up':
            if AppleInDirection(game_engin, 'left') == True or AppleInDirection(game_engin, 'right') == True or AppleInDirection(game_engin, 'down') == True:
                return True

        if move == 'down':
            if AppleInDirection(game_engin, 'up') == True or AppleInDirection(game_engin, 'right') == True or AppleInDirection(game_engin, 'left') == True:
                return True

        if move == 'right':
            if AppleInDirection(game_engin, 'up') == True or AppleInDirection(game_engin, 'down') == True or AppleInDirection(game_engin, 'left') == True:
                return True

        if move == 'left':
            if AppleInDirection(game_engin, 'up') == True or AppleInDirection(game_engin, 'right') == True or AppleInDirection(game_engin, 'down') == True:
                return True
    return False


def NextToWall(game_engin, move):
    map = game_engin.map
    x_head, y_head = game_engin.snake_head
    new_x_head = x_head + 1 if move == 'down' else x_head - 1 if move == 'up' else x_head
    new_y_head = y_head + 1 if move == 'right' else y_head - 1 if move == 'left' else y_head
    if map[new_x_head][new_y_head] != 'W':
        if (
            map[new_x_head + 1][new_y_head] == 'W'
            or map[new_x_head - 1][new_y_head] == 'W'
            or map[new_x_head][new_y_head + 1] == 'W'
            or map[new_x_head][new_y_head - 1] == 'W'
        ):
                return True
    return False


def InMapCorner(game_engin, move):
    map = game_engin.map
    x_head, y_head = game_engin.snake_head
    new_x_head = x_head + 1 if move == 'down' else x_head - 1 if move == 'up' else x_head
    new_y_head = y_head + 1 if move == 'right' else y_head - 1 if move == 'left' else y_head
    nb_walls = 0

    if map[new_x_head][new_y_head] != 'W':
        if map[new_x_head + 1][new_y_head] == 'W':
            nb_walls += 1

        if map[new_x_head - 1][new_y_head] == 'W':
            nb_walls += 1

        if map[new_x_head][new_y_head + 1] == 'W':
            nb_walls += 1

        if map[new_x_head][new_y_head - 1] == 'W':
            nb_walls += 1

        if nb_walls == 2:
            return True
    return False

#def SnakeBlocked(map, snake_head, snake_tail):