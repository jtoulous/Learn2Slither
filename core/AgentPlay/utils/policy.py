from utils.tools import GetState

def InstantReward(game_engine, move):
    reward = 0
    map = game_engin.map
    x_head, y_head = game_engin.snake_head
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
    
#    if DodgeRed(game_engine, move) == True:
#        reward +=  

#    if CloserToGreen(map, snake_head, new_x_head, new_y_head) == True:
#        reward += 5
#
#    if SnakeBlocked(map, snake_head, snake_tail) == True:
#        reward -= 40
#
#    if SnakeNotBlocked(map, snake_head, snake_tail) == True:
#        reward += 40

    return reward


def FutureReward(game_engin, move):
    q_table = self.q_table.table
    scores = None
    x_head, y_head = game_engine.snake_head
    new_x_head = x_head + 1 if move == 'down' else x_head - 1 if move == 'up' else x_head
    new_y_head = y_head + 1 if move == 'right' else y_head - 1 if move == 'left' else y_head

    new_state = GetState(game_engin.map, (new_x_head, new_y_head), game_engine.n_cells)
    if new_state in q_table:
        scores = q_table[new_state]
        return max(scores['up'], scores['down'], scores['right'], scores['left'])
    else:
        return 0


#def CloserToGreen(map, x_head, y_head):
#    snake_head = 



#def SnakeBlocked(map, snake_head, snake_tail):