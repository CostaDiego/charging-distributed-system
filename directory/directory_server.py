from rpyc import Service
from rpyc.utils.server import ThreadedServer
import sys

_SERVER = "SERVER"
_IP =  "IP"
_PORT = "PORT"

class Directory(Service):
    registry = dict()

    def exposed_register_server(self, ip_adress, port_number):
        
        self.registry[_SERVER] = {
            _IP: ip_adress,
            _PORT: port_number
        }

        return True

    def exposed_retrieve_server(self):

        if _SERVER in self.registry.keys():
            return self.registry[_SERVER]

        return None

    def exposed_register_user(self, username, ip_adress, port_number):
        self.registry[username] = {
            _IP: ip_adress,
            _PORT: port_number
        }

        return True

    def exposed_retrieve_user(self, username):
        if username in self.registry.keys():
            return self.registry[username]
        
        return None

    def exposed_check_user(self, username):
        if username in self.registry.keys():
            return True
        
        return False
        

def run(port):
    try:
        server_dir = ThreadedServer(Directory, port = port )
        print ("Server Started. Waiting Requests")
        server_dir.start()

    finally:
        print("Stoping Server.")
        sys.exit()