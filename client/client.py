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
_STANDBY = 'STANDBY'
_CHARGE = 'CHARGE'

_USERNAME = 'USERNAME'
_NAME = 'NAME'
_VALUE = 'VALUE'
_BALANCE = 'BALANCE'

_YES = 'YES'
_Y = 'Y'


class Client(Service):
    username = None
    
    def exposed_callbacks(self, callback, params = None):
        if callback == _NOTIFY_TRANFERENCE:
            return self.perform_notify(params)

        if callback == _CHARGE_USER:
            return self.perform_charge(params)

    def perform_charge(self, params):
        print(f"ALERT:\n {params[_NAME].title()} charged you R$ {params[_VALUE]}!")
        resp = input("Accept?[Y/N]: ")
        resp = resp.upper()

        if resp == _YES or resp == _Y:
            password = input("Input the password:\t")
            return password

        return False
    
    def perform_notify(self, params):
        print(f"ALERT:\n {params[_NAME].title()} has sent you R$ {params[_VALUE]}!")


def _initialize_client(server, client_port):
    fields = server.root.exposed_get_fields()

    if isinstance(fields, list) and len(fields) > 0:
        infos = dict()

        print("\n=== Please provide the following information ===\n")
        username = input(_USERNAME.title()+":\t")
        Client.username = username

        for field in fields:
            text_input = " ".join(field.split("_")).title() + ":\t"
            if field == _BALANCE:
                infos[field] = float(input(text_input))
            else:
                infos[field] = input(text_input)
        
        return server.root.exposed_create_user(
            username,
            socket.gethostbyname(socket.gethostname()),
            client_port,
            infos
        )
            
def _flow_control(dir_server, trans_server, port):
    while(True):
        mode_text = ('Choose the next action:\n' +
                    '\t StandBy: STANDBY or [0]\n' +
                    '\t Charge: CHARGE or [1]\n'+
                    '\t Exit: EXIT\n')

        mode = input(mode_text)

        if mode == "0" or mode.upper() == _STANDBY:
            try:
                print("\t=== Client in Standby, press CTRL+C to go main menu ===\n")
                client = ThreadedServer(Client, port = port)
                client.start()

            except Exception as err:
                print(f"[{datetime.now()}] - ERROR: {err}")

        elif mode == "1" or mode.upper() == _CHARGE:
            try:
                list_users = dir_server.root.exposed_list_users()
                user_text= "Type the username to be charged:\n\t" + "\n\t".join(list_users) + "\n"
                user_to_charge = input(user_text)
                value = input("The value to be charged: \t")

                result = trans_server.root.exposed_charge_user(
                    Client.username,
                    user_to_charge,
                    value
                )

                if result:
                    print(f"The user {user_to_charge} has accept the charging")
                else:
                    print(f"The user {user_to_charge} has failed to accept the charging")
                    
            except Exception as err:
                print(f"[{datetime.now()}] - ERROR: {err}")

        else:
            break

def run(port, directory_ip = DIR_SERVER_IP, directory_port = DIR_SERVER_PORT):
    try:
        conn_dir = connect(directory_ip, directory_port)
        server_ip_port = conn_dir.root.exposed_retrieve_server()

        conn_srv = connect(server_ip_port[_IP], server_ip_port[_PORT])

        if not _initialize_client(conn_srv, port):
            print("Failed to create user. Exiting!")
            sys.exit()

        print("\n=== Successful Action! ===\n")

        _flow_control(conn_dir, conn_srv, port)

    except Exception as e:
        print(f"[{datetime.now()}] - ERROR: {e}")

    finally:
        print("Stoping Client.")
        conn_dir.close()
        conn_srv.close()
        sys.exit()


    