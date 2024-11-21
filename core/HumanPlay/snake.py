import pygame
import argparse
import time

from utils.logs import PrintError, PrintLog, PrintGameData
from utils.map import LoadMap
from utils.game import InitNewGame, MoveSnake


width = 720
height = 720


def Events(game_data):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_data['running'] = False
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_w or event.key == pygame.K_UP) and game_data['last_move'] != 'down':
                MoveSnake(game_data, 'up')
            elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and game_data['last_move'] != 'right':
                MoveSnake(game_data, 'left')
            elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and game_data['last_move'] != 'left':
                MoveSnake(game_data, 'right')
            elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and game_data['last_move'] != 'up':
                MoveSnake(game_data, 'down')
        PrintGameData(game_data)


if __name__ == '__main__':
    try: 
        pygame.init()
        screen = pygame.display.set_mode((720, 720))

        game_data = {}
        InitNewGame(game_data)
        while game_data['running'] == True:
            Events(game_data)
            LoadMap(screen, game_data['map'], width / 12, height / 12)
        

    except Exception as error:
        PrintError(error) 