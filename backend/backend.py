import shutil
import uvicorn
import argparse as ap

from core.ServerManager import ServerManager



DB_PATH = 'database'
PORT = 54322
HOST = "0.0.0.0"

server_manager = ServerManager(DB_PATH, host=HOST, port=PORT)
server = server_manager.server



def Parsing():
    parser = ap.ArgumentParser()
    parser.add_argument('usage', type=str, help='run_dev, run, reset')
    return parser.parse_args() 



if __name__ == '__main__':
    try:
        args = Parsing()

        server_manager = ServerManager(DB_PATH, host=HOST, port=PORT)
        
        if args.usage == 'run_dev':
            uvicorn.run("backend:server", host=HOST, port=PORT, reload=True)

        elif args.usage == 'run':
            server_manager.run()

        elif args.usage == 'reset':
            shutil.rmtree(DB_PATH)

        else:
            raise Exception('Unknown type of usage for the backend')

    except Exception as error:
        print(f'Error: {error}')