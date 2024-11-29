import os
import pygame
import argparse
import time

from utils.logs import PrintError, PrintLog, PrintGameData, PrintQtable
from utils.game import GameEngin
from utils.agent import Agent


def Parsing():
    parser = argparse.ArgumentParser()
    parser.add_argument('-play', action='store_true', default=False, help='just play the game')
    parser.add_argument('-no-visual', action='store_true', default=False, help='to hide the graphicals running')
    parser.add_argument('-no-logs', action='store_true', default=False, help='to hide the logs')
    parser.add_argument('-sessions', type=int, default=1000, help="nb training sessions")
    parser.add_argument('-discount', type=float, default=0.9, help='discount factor')
    parser.add_argument('-alpha', type=float, default=0.5, help='learning rate')
    parser.add_argument('-epsi_max', type=float, default=1, help='start epsilon')
    parser.add_argument('-epsi_min', type=float, default=0.01, help='start epsilon')
    parser.add_argument('-epsi_decay', type=str, default='linear', help='epsilon decay strategy')
    parser.add_argument('-load', type=str, default=None, help='trained model config file to load')
    parser.add_argument('-save', type=str, default=None, help='trained model config file to load')
    parser.add_argument('-width', type=int, default=720, help='window width')
    parser.add_argument('-height', type=int, default=720, help='window height')
    parser.add_argument('-n_cells', type=int, default=10, help='map size')
    parser.add_argument('-actions', type=str, nargs='+', default=['up', 'down', 'left', 'right'], help='possible actions')
    parser.add_argument('-speed', type=float, default=0.1, help='speed')
    parser.add_argument('-train', default=True, action='store_true', help='no training')
    parser.add_argument('-no-train', action='store_true', help='no training')
    
    args = parser.parse_args()
    if args.no_train == True:
        args.train = False
    return args

def RunSession(args, game_engin, agent):
    while game_engin.game_state == 'running':
#        PrintGameData(game_engin)
#        PrintQtable(agent.q_table.table)
        move = agent.NextMove(game_engin, args.train)
#        move = input('move ==> ')
        game_engin.Update(move)

        if game_engin.speed != 0:
            time.sleep(game_engin.speed)
#        forward = input('')


if __name__ == '__main__':
    try: 
        args = Parsing()
        agent = Agent(arguments=args) if args.load is None else Agent.LoadConfig(args.load)
        game_engin = GameEngin(args)
        for session in range(args.sessions):
            PrintLog(f'session {session + 1} / {args.sessions}  |  epsilon = {agent.epsilon}')
            RunSession(args, game_engin, agent)
            
            if args.train == True:    
                agent.Update(session, args.sessions)
            game_engin.ResetEngin()

        if args.train == True:
            if args.load == None:
                agent.SaveConfig(args.save)
            else:
                agent.SaveConfig(args.load)


    except Exception as error:
        PrintError(error)