from utils.tools import GetState

def InstantReward(game_engin, move):
    reward = CellType(game_engin, move)

#    if DodgeRed(game_engin, move) == True:
#        reward +=  

    if CloserToGreen(game_engin, move) == True:
        reward += 5
#
#    if SnakeBlocked(map, snake_head, snake_tail) == True:
#        reward -= 40
#
#    if SnakeNotBlocked(map, snake_head, snake_tail) == True:
#        reward += 40

    return reward


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


def CellType(game_engin, move):
    map = game_engin.map
    x_head, y_head = game_engin.snake_head
    new_x_head = x_head + 1 if move == 'down' else x_head - 1 if move == 'up' else x_head
    new_y_head = y_head + 1 if move == 'right' else y_head - 1 if move == 'left' else y_head

    if map[new_x_head][new_y_head] == 'G':
        return 20
    elif map[new_x_head][new_y_head] == 'R':
        return -20
    elif map[new_x_head][new_y_head] == '0':
        return -1
    elif map[new_x_head][new_y_head] == 'W' or map[new_x_head][new_y_head] == 'S':
        return -50
    return 0



def CloserToGreen(game_engin, move):
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
            if map[c][y_head] == 'G':
                return True

    if move == 'right':
        for c in range(y_head + 1, game_engin.n_cells, 1):
            if map[c][y_head] == 'G':
                return True
    return False




#def SnakeBlocked(map, snake_head, snake_tail):