import pygame
import argparse
import time

from utils.logs import PrintError, PrintLog, PrintGameData
from utils.game import GameEngin
from utils.agent import Agent

width = 720
height = 720


def Parsing():
    parser = argparse.ArgumentParser()
    parser.add_argument('-play', action='store_true', default=False, help='just play the game')
    parser.add_argument('-no-visual', action='store_true', default=False, help='to hide the graphicals running')
    parser.add_argument('-no-logs', action='store_true', default=False, help='to hide the logs')
    parser.add_argument('-sessions', type=int, default=1, help="nb training sessions")
    parser.add_argument('-discount', type=float, default=0.9, help='discount factor')
    parser.add_argument('-alpha', type=float, default=0.1, help='learning rate')
    parser.add_argument('-epsi', type=float, default=1, help='start epsilon')
    parser.add_argument('-epsi_decay', type=str, default='linear', help='epsilon decay strategy')
    parser.add_argument('-n_action', type=int, default=4, help='nb possible actions')
    parser.add_argument('-load', type=str, default=None, help='trained model config file to load')
    parser.add_argument('-save', type=str, default=None, help='trained model config file to load')
    parser.add_argument('-width', type=int, default=720, help='window width')
    parser.add_argument('-height', type=int, default=720, help='window height')
    parser.add_argument('-n_cells', type=int, default=10, help='map size')
    return parser.parse_args()


def RunSession(args, game_engin, agent):
    while game_engin.game_state == 'running':
        move = agent.NextMove(game_engin)
        game_engin.Update(move)


if __name__ == '__main__':
    try: 
        args = Parsing()    
        agent = Agent(args=args) if args.load == None else agent = Agent(config=args.load)

        for session in range(args.sessions):
            game_engin = GameEngin(args)
            RunSession(args, game_engin, agent)


    except Exception as error:
        PrintError(error)