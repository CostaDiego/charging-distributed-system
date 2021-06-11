from rpyc import Service, connect
from rpyc.utils.server import ThreadedServer
from datetime import datetime
from copy import deepcopy
import socket
import sys

from constRPYC import DIR_SERVER_IP, DIR_SERVER_PORT

_IP =  'IP'
_PORT = 'PORT'

_NAME = 'NAME'
_BANK = 'BANK'
_ACCOUNT_NUMBER = 'ACCOUNT_NUMBER'
_AGENCY_NUMBER = 'AGENCY_NUMBER'
_CREDIT_CARD = 'CREDIT_CARD'
_PASSWORD = 'PASSWORD'
_BALANCE = 'BALANCE'
_VALUE = 'VALUE'

_NOTIFY_TRANFERENCE = 'NOTIFY_TRANFERENCE'
_CHARGE_USER = 'CHARGE_USER'


class TransactionServer(Service):
    fields = [
        _NAME,
        _BANK,
        _ACCOUNT_NUMBER,
        _AGENCY_NUMBER,
        _CREDIT_CARD,
        _PASSWORD,
        _BALANCE
    ]

    user_database = dict()

    def exposed_get_fields(self):
        print(f"[{datetime.now()}] - Returning fields")
        return deepcopy(list(self.fields))

    def exposed_create_user(self, username, fields):
        print(f"[{datetime.now()}] - Creating new user")

        if (len(fields) == len(self.fields) and isinstance(fields, dict)):

            self.user_database[username] = fields

            return True

        else:
            return False

    def perform_charge_user(self, orig_username, target_username, value):
        if self.user_database[orig_username][_BALANCE] - value >= 0:
            self.user_database[orig_username][_BALANCE] -= value
            self.user_database[target_username][_BALANCE] += value

            return True

        return False

    def exposed_charge_user(self, orig_username, target_username, value):
        print(f"[{datetime.now()}] - Charging user")
        if (orig_username in self.user_database.keys() and
            target_username in self.user_database.keys()):

            try:
                conn_dir = connect(
                    DIR_SERVER_IP,
                    DIR_SERVER_PORT
                )
                target_ip_port = conn_dir.root.exposed_retrieve_user(target_username)

                conn_clt = connect(
                    target_ip_port[_IP],
                    target_ip_port[_PORT]
                )
                response = conn_clt.root.exposed_callbacks(
                    _CHARGE_USER,
                    {
                        _NAME: self.user_database[orig_username][_NAME],
                        _VALUE: value
                    }
                )

                if (isinstance(response, str) and 
                    response == self.user_database[target_username][_PASSWORD]):

                    return self.perform_charge_user(
                            orig_username,
                            target_username,
                            value)


            except Exception as e:
                print(f"[{datetime.now()}] - ERROR: {e}")

            finally:
                conn_dir.close()
                conn_clt.close()

        return False

    def exposed_add_cash(self, username, value):
        print(f"[{datetime.now()}] - Adding cash")
        if username in self.user_database.keys():
            self.user_database[username][_BALANCE] += value

            return True
        
        return False

    def perform_notify(self, orig_username, target_username, value):
        try:
            conn_dir = connect(
                DIR_SERVER_IP,
                DIR_SERVER_PORT
            )
            target_ip_port = conn_dir.root.exposed_retrieve_user(target_username)

            conn_clt = connect(
                target_ip_port[_IP],
                target_ip_port[_PORT]
            )
            conn_clt.root.exposed_callbacks(
                _NOTIFY_TRANFERENCE,
                {
                    _NAME: self.user_database[orig_username][_NAME],
                    _VALUE: value
                }
            )

        except Exception as e:
            print(f"[{datetime.now()}] - ERROR: {e}")

        finally:
            conn_dir.close()
            conn_clt.close()

    def exposed_send_cash(self, orig_username, target_username, value):
        print(f"[{datetime.now()}] - Sending cash to user")
        if (orig_username in self.user_database.keys() and
            target_username in self.user_database.keys()):

            if self.user_database[orig_username][_BALANCE] - value >= 0:
                self.user_database[orig_username][_BALANCE] -= value
                self.user_database[target_username][_BALANCE] += value

                self.perform_notify(orig_username, target_username, value)

                return True

            return False

        return False


def run(port, directory_ip = DIR_SERVER_IP, directory_port = DIR_SERVER_PORT):
    try:
        op_server = ThreadedServer(TransactionServer, port = port)
        conn_dir = connect(directory_ip, directory_port)
        my_address = socket.gethostbyname(socket.gethostname())

        if conn_dir.root.exposed_register_server(my_address, port):
            print("Operation Server Started. Waiting Requests")
            conn_dir.close()
            op_server.start()

    finally:
        print("Stoping Server.")
        sys.exit()
