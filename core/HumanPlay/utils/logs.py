from colorama import Fore, Style

def PrintLog(log):
    print(f'{Fore.GREEN}{log}{Style.RESET_ALL}')

def PrintError(error):
    print(f'{Fore.RED}{error}{Style.RESET_ALL}')

def PrintInfo(info):
    print(f'{Fore.BLUE}{info}{Style.RESET_ALL}')

def PrintGameData(game_data):
    PrintLog('\n\n===================================')
    PrintLog('==            STATS              ==')
    PrintLog('===================================')
    PrintLog(f'map ==>')
    for row in game_data['map']:
        PrintLog(row)

    PrintLog(f'\nsnake_head ==> {game_data["snake_head"]}')
    PrintLog(f'snake_body ==> {game_data["snake_body"]}')
    PrintLog(f'snake_size ==> {game_data["snake_size"]}')
    PrintLog(f'last_move ===> {game_data["last_move"]}')