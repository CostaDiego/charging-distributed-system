from rpyc import Service
from rpyc.utils.server import ThreadedServer
from copy import deepcopy
import sys
from datetime import datetime

from constRPYC import DIR_SERVER_IP, DIR_SERVER_PORT

_SERVER = "SERVER"
_IP =  "IP"
_PORT = "PORT"

class Directory(Service):
    registry_server = dict()
    registry_users = dict()

    def exposed_register_server(self, ip_adress, port_number):
        print(f"[{datetime.now()}] - Registering Server")
        
        self.registry_server[_SERVER] = {
            _IP: ip_adress,
            _PORT: port_number
        }

        return True

    def exposed_retrieve_server(self):
        print(f"[{datetime.now()}] - Retrieving Server")

        if _SERVER in self.registry_server.keys():
            return self.registry_server[_SERVER]

        return None

    def exposed_register_user(self, username, ip_adress, port_number):
        print(f"[{datetime.now()}] - Registering new user")

        self.registry_users[username] = {
            _IP: ip_adress,
            _PORT: port_number
        }

        return True

    def exposed_retrieve_user(self, username):
        print(f"[{datetime.now()}] - Retrieving user")

        if username in self.registry_users.keys():
            return self.registry_users[username]
        
        return None

    def exposed_check_user(self, username):
        print(f"[{datetime.now()}] - Checking user")

        if username in self.registry_users.keys():
            return True
        
        return False

    def exposed_list_users(self):
        print(f"[{datetime.now()}] - Listing users")

        return deepcopy(list(self.registry_users.keys()))


def run():
    try:
        server_dir = ThreadedServer(Directory, port = DIR_SERVER_PORT )
        print ("Directory Server Started. Waiting Requests")
        server_dir.start()

    finally:
        print("Stoping Server.")
        sys.exit()