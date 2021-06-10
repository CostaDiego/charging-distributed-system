__all__ = ['operation_server']

from os import path
import sys

root = path.abspath('..')

if root not in sys.path:
    sys.path.append(root)

from server.operation_server import run as run_server
from server.operation_server import OperationServer