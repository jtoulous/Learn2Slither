from colorama import Fore, Style

def PrintQtable(q_table):
    for key, value in q_table.items():
        PrintLog(f'{key}: {value}')

def PrintLog(log):
    print(f'{Fore.GREEN}{log}{Style.RESET_ALL}')

def PrintError(error):
    print(f'{Fore.RED}{error}{Style.RESET_ALL}')

def PrintInfo(info):
    print(f'{Fore.BLUE}{info}{Style.RESET_ALL}')

def PrintGameData(game_engin):
    PrintLog('\n\n===================================')
    PrintLog('==            STATS              ==')
    PrintLog('===================================')
    PrintLog(f'map ==>')
    for row in game_engin.map:
        PrintLog(row)

    PrintLog(f'\nsnake_head ==> {game_engin.snake_head}')
    PrintLog(f'snake_body ==> {game_engin.snake_body}')
    PrintLog(f'snake_size ==> {game_engin.snake_size}')
    PrintLog(f'last_move ==> {game_engin.last_move}')