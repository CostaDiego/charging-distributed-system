from logging import info
from directory.directory_server import _IP
from rpyc import Service, connect
from rpyc.utils.server import ThreadedServer
from datetime import datetime
from copy import deepcopy
import socket
import sys

from constRPYC import DIR_SERVER_IP, DIR_SERVER_PORT

_IP = 'IP'
_PORT = 'PORT'

_NOTIFY_TRANFERENCE = 'NOTIFY_TRANFERENCE'
_CHARGE_USER = 'CHARGE_USER'

_USERNAME = 'USERNAME'
_NAME = 'NAME'
_VALUE = 'VALUE'

_YES = 'YES'
_Y = 'Y'


class Client(Service):

    def exposed_callbacks(self, callback, params = None):
        if callback == _NOTIFY_TRANFERENCE:
            self.perform_notify(params)

        if callback == _CHARGE_USER:
            self.perform_charge(params)

    def perform_charge(self, params):
        print(f"ALERT:\n {params[_NAME].title()} charged you R$ {params[_VALUE]}!")
        resp = input("Accept?[Y/N]: ").upper()

        if resp == _YES or resp == _Y:
            return input("Input the password:\n")

        return False
    
    def perform_notify(self, params):
        print(f"ALERT:\n {params[_NAME].title()} has sent you R$ {params[_VALUE]}!")


def _initialize_client(server, client_port):
    fields = server.root.exposed_get_fields()

    if isinstance(fields, list) and len(fields) > 0:
        infos = dict()

        print("Please provide the following information:\n")
        username = input(_USERNAME.title())

        for field in fields:
            infos[field] = input(" ".join(field.split("_")).title())
        
        return server.root.exposed_create_user(
            username,
            socket.gethostbyname(socket.gethostname()),
            client_port,
            infos
        )
            
def _flow_control(dir_server, trans_server):
    pass

def run(port, directory_ip = DIR_SERVER_IP, directory_port = DIR_SERVER_PORT):
    try:
        conn_dir = connect(directory_ip, directory_port)
        server_ip_port = conn_dir.exposed_retrieve_server()

        conn_srv = connect(server_ip_port[_IP], server_ip_port[_PORT])

        if not _initialize_client(conn_srv, port):
            print("Failed to create user. Exiting!")
            sys.exit()

        _flow_control(conn_dir, conn_srv)

    except Exception as e:
        print(f"[{datetime.now()}] - ERROR: {e}")

    finally:
        print("Stoping Client.")
        conn_dir.close()
        conn_srv.close()
        sys.exit()


    