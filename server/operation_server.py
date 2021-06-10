from rpyc import Service, connect
from rpyc.utils.server import ThreadedServer
from datetime import datetime
import socket
import sys

from constRPYC import DIR_SERVER_IP, DIR_SERVER_PORT

_IP =  "IP"
_PORT = "PORT"
_NAME = 'NAME'
_BANK = 'BANK',
_ACCOUNT_NUMBER = 'ACCOUNT_NUMBER'
_AGENCY_NUMBER = 'AGENCY_NUMBER'
_CREDIT_CARD = 'CREDIT_CARD'
_PASSWORD = 'PASSWORD'
_BALANCE = 'BALANCE'

class OperationServer(Service):
    fields = [
        _NAME,
        _BANK,
        _ACCOUNT_NUMBER,
        _AGENCY_NUMBER,
        _CREDIT_CARD,
        _CREDIT_CARD,
        _BALANCE
    ]

    user_database = dict()

    def exposed_get_fields(self):
        return self.fields

    def exposed_create_user(self, username, fields):
        print(f"[{datetime.now()}] - Creating new user")

        if (len(fields) == len(self.fields) and
            isinstance(fields, dict)):
            self.user_database[username] = fields

            return True

        else:
            return False

def run(port, directory_ip = DIR_SERVER_IP, directory_port = DIR_SERVER_PORT):
    try:
        op_server = ThreadedServer(OperationServer, port = port)
        conn_dir = connect(directory_ip, directory_port)
        my_address = socket.gethostbyname(socket.gethostname())

        if conn_dir.root.exposed_register_server(my_address, port):
            print("Operation Server Started. Waiting Requests")
            op_server.start()

    finally:
        print("Stoping Server.")
        sys.exit()
