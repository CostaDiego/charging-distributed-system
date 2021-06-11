__all__ = ['client']

from os import path
import sys

root = path.abspath('..')

if root not in sys.path:
    sys.path.append(root)

from client.client import run as run_client
from client.client import Client