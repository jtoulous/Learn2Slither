from utils.map import InitMap, NewApple
from utils.logs import PrintLog

def InitGame(game_data):
    game_data['running'] = True
    InitMap(game_data)
    
    game_data['snake_size'] = len(game_data['snake_body'])
    x_head, y_head = game_data['snake_head']
    x_body, y_body = game_data['snake_body'][0]
    if x_body == x_head - 1:
        game_data['last_move'] = 'down'
    elif x_body == x_head + 1:
        game_data['last_move'] = 'up'
    elif y_body == y_head - 1:
        game_data['last_move'] = 'right'
    elif y_body == y_head + 1:
        game_data['last_move'] = 'left'
    



def MoveSnake(game_data, move):
    x_head, y_head = game_data['snake_head']
    nxt_x = x_head - 1 if move == 'up' else x_head + 1 if move == 'down' else x_head
    nxt_y = y_head - 1 if move == 'left' else y_head + 1 if move == 'right' else y_head

    if game_data['map'][nxt_x][nxt_y] == '0':
        x_tail, y_tail = game_data['snake_body'].pop()
        game_data['map'][nxt_x][nxt_y] = 'H'
        game_data['map'][x_head][y_head] = 'S'
        game_data['map'][x_tail][y_tail] = '0'
        game_data['snake_body'].insert(0, (x_head, y_head))
        game_data['snake_head'] = (nxt_x, nxt_y)

    elif game_data['map'][nxt_x][nxt_y] == 'G':
        EatGreenApple(game_data, nxt_x, nxt_y)

    elif game_data['map'][nxt_x][nxt_y] == 'R':
        EatRedApple(game_data, nxt_x, nxt_y)

    elif game_data['map'][nxt_x][nxt_y] == 'S' or game_data['map'][nxt_x][nxt_y] == 'W':
        GameOver()

    game_data['last_move'] = move

def EatGreenApple(game_data, nxt_x, nxt_y):
    x_head, y_head = game_data['snake_head']
    game_data['map'][nxt_x][nxt_y] = 'H'
    game_data['map'][x_head][y_head] = 'S'
    game_data['snake_body'].insert(0, (x_head, y_head))
    game_data['snake_head'] = (nxt_x, nxt_y)
    game_data['snake_size'] = len(game_data['snake_body'])
    NewApple(game_data, 'G')



def EatRedApple(game_data, nxt_x, nxt_y):
    if game_data['snake_size'] == 1:
        GameOver()
    x_head, y_head = game_data['snake_head']
    x_tail, y_tail = game_data['snake_body'].pop()
    x_erase, y_erase = game_data['snake_body'].pop()

    game_data['map'][nxt_x][nxt_y] = 'H'
    game_data['map'][x_head][y_head] = 'S'
    game_data['map'][x_tail][y_tail] = '0'
    game_data['map'][x_erase][y_erase] = '0'
    game_data['snake_body'].insert(0, (x_head, y_head))
    game_data['snake_head'] = (nxt_x, nxt_y)
    game_data['snake_size'] = len(game_data['snake_body'])
    NewApple(game_data, 'R')

def GameOver():
    PrintLog('\n\n       GAME OVER BIACH   ')
    exit(0)