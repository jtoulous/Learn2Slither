import random

def XplorationOrXplotation(epsilon):
    random_nb = random.random()
    if random_nb <= epsilon:
        return 'Xploration'
    else:
        return 'Xplotation'

def GetState(map, snake_head, n_cells):
    x_head = snake_head[0]
    y_head = snake_head[1]
    horizontal_view = ''
    vertical_view = ''
    
    for y in range(0, n_cells + 2):
        horizontal_view += map[x_head][y]
    for x in range(0, n_cells + 2):
        vertical_view += map[x][y_head]
    return (horizontal_view, vertical_view)


def InstantReward(map, move, snake_head):
    reward = 0
    x_head, y_head = snake_head
    new_x_head = x_head + 1 if move == 'down' else x_head - 1 if move == 'up' else x_head
    new_y_head = y_head + 1 if move == 'right' else y_head - 1 if move == 'left' else y_head

    if map[new_x_head][new_y_head] == 'G':
        reward += 20
    elif map[new_x_head][new_y_head] == 'R':
        reward -= 20
    elif map[new_x_head][new_y_head] == '0':
        reward -= 1
    elif map[new_x_head][new_y_head] == 'W' or map[new_x_head][new_y_head] == 'S':
        reward -= 50
    return reward


def FutureReward(map, q_table, move, snake_head, n_cells):
    scores = None
    x_head, y_head = snake_head
    new_x_head = x_head + 1 if move == 'down' else x_head - 1 if move == 'up' else x_head
    new_y_head = y_head + 1 if move == 'right' else y_head - 1 if move == 'left' else y_head

    new_state = GetState(map, (new_x_head, new_y_head), n_cells)
    if new_state in q_table:
        scores = q_table[new_state]
        return max(scores['up'], scores['down'], scores['right'], scores['left'])
    else:
        return 0


def GenerateMap(n_cells):
    map = []
    first_row = []
    middle_row = ['W']

    for i in range(n_cells + 2):
        first_row.append('W')

    for i in range(n_cells):
        middle_row.append('0')
    middle_row.append('W')

    map.append(first_row.copy())
    for i in range(n_cells):
        map.append(middle_row.copy())
    map.append(first_row.copy())
    return map