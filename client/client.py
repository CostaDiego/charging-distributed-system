from rpyc import Service, connect
from rpyc.utils.server import ThreadedServer
from datetime import datetime
from copy import deepcopy
import socket
import sys

from constRPYC import DIR_SERVER_IP, DIR_SERVER_PORT

class Client(Service):
    pass

def run(port, directory_ip = DIR_SERVER_IP, directory_port = DIR_SERVER_PORT):
    pass