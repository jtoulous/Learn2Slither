import pygame
import random

#def InitGame():
#    game_data = {'running': True}
#    InitMap(game_data)
#    return game_data

def InitMap(game_data):
    game_data['map'] = [
        ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
        ['W', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'W'],
        ['W', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'W'],
        ['W', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'W'],
        ['W', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'W'],
        ['W', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'W'],
        ['W', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'W'],
        ['W', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'W'],
        ['W', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'W'],
        ['W', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'W'],
        ['W', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'W'],
        ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
    ]
    NewApple(game_data, 'G')
    NewApple(game_data, 'G')
    NewApple(game_data, 'R')
    NewSnake(game_data)



def NewApple(game_data, apple_type):
    apple_placed = False
    while apple_placed != True:
        x = random.randint(1, 10)
        y = random.randint(1, 10)
        if game_data['map'][x][y] == '0':
            game_data['map'][x][y] = apple_type
            apple_placed = True


def NewSnake(game_data):
    snake_placed = False
    while snake_placed != True:
        x1 = random.randint(1, 10)
        y1 = random.randint(1, 10)
        if game_data['map'][x1][y1] == '0':
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

            if game_data['map'][x2][y2] == '0':
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

                if game_data['map'][x3][y3] == '0' and (x3 != x1 or y3 != y1):
                    game_data['map'][x1][y1] = 'H' 
                    game_data['map'][x2][y2] = 'S' 
                    game_data['map'][x3][y3] = 'S'
                    snake_placed = True
    game_data['snake_head'] = (x1, y1)
    game_data['snake_body'] = [(x2, y2), (x3, y3)]


def LoadMap(screen, map, cell_width, cell_height):
    color = (0, 0, 0)
    for y, row in enumerate(map):
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

            pygame.draw.rect(screen, color, (x * cell_width, y * cell_height, cell_width, cell_height))
            pygame.draw.line(screen, (0, 0, 0), (x * cell_width, 0), (x * cell_width, 720), 2)
            pygame.draw.line(screen, (0, 0, 0), (0, y * cell_height), (720, y * cell_height), 2)
    pygame.display.flip()