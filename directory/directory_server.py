from rpyc import Service
from rpyc.utils.server import ThreadedServer
import sys

_SERVER = "SERVER"
_IP =  "IP"
_PORT = "PORT"

class Directory(Service):
    registry = dict()
    response = "Worked!"

    def exposed_register_server(self, ip_adress, port_number):
        
        registry[_SERVER] = {
            _IP: ip_adress,
            _PORT, port_number
        }

    def exposed_retrieve_server(self):

        if _SERVER self.registry.keys():
            return self.registry[_SERVER]

        return None
        

def run(port):
    try:
        server_dir = ThreadedServer(Directory, port = port )
        print ("Server Started. Waiting Requests")
        server_dir.start()

    finally:
        print("Stoping Server.")
        sys.exit()