import random
import pygame

from utils.tools import GenerateMap
from utils.logs import PrintLog


class   GameEngin():
    def __init__(self, args):
        self.visual = True if args.no_visual == False else False
        self.width = args.width
        self.height = args.height
        self.game_state = 'running'
        self.map = []
        self.snake_head = ()
        self.snake_body = []
        self.snake_size = 2
        self.last_move = None
        self.n_cells = args.n_cells
        self.speed = args.speed

        self.InitMap()

        x_head, y_head = self.snake_head
        x_body, y_body = self.snake_body[0]
        if x_body == x_head - 1:
            self.last_move = 'down'
        elif x_body == x_head + 1:
            self.last_move = 'up'
        elif y_body == y_head - 1:
            self.last_move = 'right'
        elif y_body == y_head + 1:
            self.last_move = 'left'

        if self.visual == True:
            pygame.mixer.quit()
            pygame.init()
            self.window = pygame.display.set_mode((self.width, self.height), pygame.SWSURFACE)
            self.UpdateWindow()

    def ResetEngin(self):
        self.game_state = 'running'
        self.map = []
        self.snake_head = ()
        self.snake_body = []
        self.snake_size = 2
        self.last_move = None

        self.InitMap()

        x_head, y_head = self.snake_head
        x_body, y_body = self.snake_body[0]
        if x_body == x_head - 1:
            self.last_move = 'down'
        elif x_body == x_head + 1:
            self.last_move = 'up'
        elif y_body == y_head - 1:
            self.last_move = 'right'
        elif y_body == y_head + 1:
            self.last_move = 'left'

        if self.visual == True:
            self.UpdateWindow()


    def InitMap(self):
        self.map = GenerateMap(self.n_cells)
        self.NewApple('G')
        self.NewApple('G')
        self.NewApple('R')
        self.NewSnake()
        

    def NewApple(self, apple_type):
        apple_placed = False
        while apple_placed != True:
            x = random.randint(1, self.n_cells)
            y = random.randint(1, self.n_cells)
            if self.map[x][y] == '0':
                self.map[x][y] = apple_type
                apple_placed = True


    def NewSnake(self):
        snake_placed = False
        while snake_placed != True:
            x1 = random.randint(1, self.n_cells)
            y1 = random.randint(1, self.n_cells)
            if self.map[x1][y1] == '0':
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

                if self.map[x2][y2] == '0' and (x2 != x1 or y2 != y1):
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

                    if self.map[x3][y3] == '0' and (x3 != x1 or y3 != y1):
                        self.map[x1][y1] = 'H' 
                        self.map[x2][y2] = 'S' 
                        self.map[x3][y3] = 'S'
                        snake_placed = True
        self.snake_head = (x1, y1)
        self.snake_body = [(x2, y2), (x3, y3)]


    def Update(self, move):
        x_head, y_head = self.snake_head
        nxt_x = x_head - 1 if move == 'up' else x_head + 1 if move == 'down' else x_head
        nxt_y = y_head - 1 if move == 'left' else y_head + 1 if move == 'right' else y_head

        if self.map[nxt_x][nxt_y] == '0':
            x_tail, y_tail = self.snake_body.pop()
            self.map[nxt_x][nxt_y] = 'H'
            self.map[x_head][y_head] = 'S'
            self.map[x_tail][y_tail] = '0'
            self.snake_body.insert(0, (x_head, y_head))
            self.snake_head = (nxt_x, nxt_y)

        elif self.map[nxt_x][nxt_y] == 'G':
            self.EatGreenApple(nxt_x, nxt_y)

        elif self.map[nxt_x][nxt_y] == 'R':
            self.EatRedApple(nxt_x, nxt_y)

        elif self.map[nxt_x][nxt_y] == 'S' or self.map[nxt_x][nxt_y] == 'W':
            self.GameOver()
        self.last_move = move
        if self.visual == True:
            self.UpdateWindow()


    def EatGreenApple(self, nxt_x, nxt_y):
        x_head, y_head = self.snake_head
        self.map[nxt_x][nxt_y] = 'H'
        self.map[x_head][y_head] = 'S'
        self.snake_body.insert(0, (x_head, y_head))
        self.snake_head = (nxt_x, nxt_y)
        self.snake_size = len(self.snake_body)
        self.NewApple('G')


    def EatRedApple(self, nxt_x, nxt_y):
        if self.snake_size == 1:
            self.GameOver()
            return
        x_head, y_head = self.snake_head
        x_tail, y_tail = self.snake_body.pop()
        x_erase, y_erase = self.snake_body.pop()

        self.map[nxt_x][nxt_y] = 'H'
        self.map[x_head][y_head] = 'S'
        self.map[x_tail][y_tail] = '0'
        self.map[x_erase][y_erase] = '0'
        self.snake_body.insert(0, (x_head, y_head))
        self.snake_head = (nxt_x, nxt_y)
        self.snake_size = len(self.snake_body)
        self.NewApple('R')


    def GameOver(self):
        self.game_state = 'done'


    def UpdateWindow(self):
        cell_width = self.width / (self.n_cells + 2)
        cell_height = self.height / (self.n_cells + 2)
        color = (0, 0, 0)
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if cell == 'W':
                   color = (0, 0, 0) 
                elif cell == '0':
                   color = (255, 255, 255) 
                elif cell == 'G':
                   color = (0, 255, 0) 
                elif cell == 'R':
                   color = (255, 0, 0) 
                elif cell == 'H':
                   color = (0, 0, 139) 
                elif cell == 'S':
                   color = (0, 191, 255) 

                pygame.draw.rect(self.window, color, (x * cell_width, y * cell_height, cell_width, cell_height))
                pygame.draw.line(self.window, (0, 0, 0), (x * cell_width, 0), (x * cell_width, self.height), 2)
                pygame.draw.line(self.window, (0, 0, 0), (0, y * cell_height), (self.width, y * cell_height), 2)
        pygame.display.flip()