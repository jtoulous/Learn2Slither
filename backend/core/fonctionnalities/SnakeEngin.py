import random
import numpy as np


class SnakeEngin:
    def __init__(self):
        self.map = None

        self.status = 'inactive'
        self.prev_move = None
        self.score = 3
        self.green_score = 0
        self.red_score = 0
        self.nb_moves = 0


    def new_game(self, n_cells=10):
        self.map = Map(n_cells)
        prev_move = self.map.reset()

        self.status = 'active'
        self.prev_move = prev_move
        self.score = 3
        self.green_score = 0
        self.red_score = 0
        self.nb_moves = 0



    def get_snake_view(self, rtn='str'):
        x_head = self.map.snake_head[0]
        y_head = self.map.snake_head[1]

        horizontal_view = self.map.grid[x_head, :]
        vertical_view = self.map.grid[:, y_head]

        if rtn == 'str':
            combined_view = ''.join(horizontal_view) + ''.join(vertical_view)
            return combined_view
        else:
            return horizontal_view, vertical_view
        

    def game_state(self):
        game_state = {}
        game_state['status'] = self.status
        game_state['n_cells'] = self.map.n_cells
        game_state['snake_head'] = self.map.snake_head
        game_state['snake_body'] = self.map.snake_body
        game_state['green_apples'] = self.map.green_apples
        game_state['red_apple'] = self.map.red_apple
        game_state['score'] = self.score
        game_state['green_score'] = self.green_score
        game_state['red_score'] = self.red_score
        game_state['nb_moves'] = self.nb_moves

        return game_state

    
    @staticmethod
    def load_game(game_state):
        loaded_engin = SnakeEngin()
        loaded_engin.status = game_state['status']
        loaded_engin.map = Map.load(game_state)
        
        return loaded_engin


    def execute_move(self, move):
        if (move == 'up' and self.prev_move == 'down') or \
           (move == 'down' and self.prev_move == 'up') or \
           (move == 'left' and self.prev_move == 'right') or \
           (move == 'right' and self.prev_move == 'left'):
            return
        
        grid = self.map.grid
        x_head = self.map.snake_head[0]
        y_head = self.map.snake_head[1]
        
        nxt_x_head = x_head - 1 if move == 'up' else x_head + 1 if move == 'down' else x_head 
        nxt_y_head = y_head - 1 if move == 'left' else y_head + 1 if move == 'right' else y_head

        cell = grid[nxt_x_head, nxt_y_head]

        if cell == 'W' or cell == 'S':
            self.status = 'end'
                
        elif cell == 'G':
            self.map.move_snake(nxt_x_head, nxt_y_head)
            self.green_score += 1
            self.score += 1

        elif cell == 'R':
            self.map.move_snake(nxt_x_head, nxt_y_head)
            self.red_score += 1
            self.score -= 1

        else:
            self.map.move_snake(nxt_x_head, nxt_y_head)

        self.prev_move = move
        self.nb_moves += 1







class Map:
    def __init__(self, n_cells):
        self.n_cells = n_cells

        self.grid = self.init_grid()
        self.snake_head = ()
        self.snake_body = []
        self.green_apples = []
        self.red_apple = ()


    @staticmethod
    def load(game_state):
        loaded_map = Map(game_state['n_cells'])
        loaded_map.snake_head = game_state['snake_head']
        loaded_map.snake_body = game_state['snake_body']
        loaded_map.green_apples = game_state['green_apples']
        loaded_map.red_apple = game_state['red_apple']

        return loaded_map


    def reset(self):
        self.grid = self.init_grid()
        self.snake_head = ()
        self.snake_body = []
        self.green_apples = []
        self.red_apple = () 

        self.new_snake()
        self.new_apple('G')
        self.new_apple('G')
        self.new_apple('R')

        x_head, y_head = self.snake_head
        x_body, y_body = self.snake_body[0]
        
        prev_move = (
            'up' if x_head == x_body - 1
            else 'down' if x_head == x_body + 1
            else 'left' if y_body == y_head + 1
            else 'right' if y_body == y_head - 1
            else None
        )
        return prev_move



    def init_grid(self):
        grid = np.zeros((self.n_cells + 2, self.n_cells + 2), dtype=str)
        grid[:, :] = '0'
        
        grid[0, :] = 'W'
        grid[-1, :] = 'W'
        grid[1:-1, 0] = 'W'
        grid[1:-1, -1] = 'W'

        return grid


    def new_apple(self, apple_type):
        while True:
            x = random.randint(1, self.n_cells)
            y = random.randint(1, self.n_cells)
        
            if self.grid[x, y] == '0':
                self.grid[x, y] = apple_type

                if apple_type == 'G':
                    self.green_apples.append((x, y))
                else:
                    self.red_apple = (x, y)

                break


    def new_snake(self):
        snake_placed = False
        while snake_placed != True:
            x1 = random.randint(1, self.n_cells)
            y1 = random.randint(1, self.n_cells)
            if self.grid[x1, y1] == '0':
                next_pos = random.randint(1, 4)
                if next_pos == 1:
                    x2 = x1 - 1
                    y2 = y1

                elif next_pos == 2:
                    x2 = x1 + 1
                    y2 = y1

                elif next_pos == 3:
                    x2 = x1
                    y2 = y1 - 1

                elif next_pos == 4:
                    x2 = x1
                    y2 = y1 + 1

                if self.grid[x2, y2] == '0':
                    next_pos = random.randint(1, 4)
                    if next_pos == 1:
                        x3 = x2 - 1
                        y3 = y2

                    elif next_pos == 2:
                        x3 = x2 + 1
                        y3 = y2

                    elif next_pos == 3:
                        x3 = x2
                        y3 = y2 - 1

                    elif next_pos == 4:
                        x3 = x2
                        y3 = y2 + 1

                    if self.grid[x3, y3] == '0' and (x3 != x1 or y3 != y1):
                        self.grid[x1, y1] = 'H' 
                        self.grid[x2, y2] = 'S' 
                        self.grid[x3, y3] = 'S'
                        snake_placed = True
        self.snake_head = (x1, y1)
        self.snake_body = [(x2, y2), (x3, y3)]


    def move_snake(self, nxt_x_head, nxt_y_head):
        nxt_head = (nxt_x_head, nxt_y_head)
        nxt_cell = self.grid[nxt_head]
        head = self.snake_head
            
        self.grid[head] = 'S'
        self.grid[nxt_head] = 'H'

        self.snake_head = nxt_head
        self.snake_body.insert(0, head)

        if nxt_cell == 'G':
            self.green_apples.remove(nxt_head)
            self.new_apple('G')

        elif nxt_cell == 'R':
            self.new_apple('R')
            for i in range(2):
                tail = self.snake_body.pop()
                self.grid[tail] = '0'

        elif nxt_cell == '0':
            tail = self.snake_body.pop()
            self.grid[tail] = '0'
