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