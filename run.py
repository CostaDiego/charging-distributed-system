from argparse import ArgumentParser
from directory.directory_server import run
from directory import run_directory
from server import run_server
from client import run_client

_DIRECTORY = 'DIRECTORY'
_SERVER = 'SERVER'
_CLIENT = 'CLIENT'

if __name__ == '__main__':
    parser = ArgumentParser(description='Run the Directory Server, Transaction Server or Client')
    parser.add_argument('mode', type=str)
    parser.add_argument('-p', '--port', type=int)

    args = parser.parse_args()

    if args.mode.upper() == _DIRECTORY:
        run_directory()
    if args.mode.upper() == _SERVER:
        run_server(args.port)
    if args.mode.upper() == _CLIENT:
        run_client(args.port)