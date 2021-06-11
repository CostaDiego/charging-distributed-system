__all__ = ['directory_server']

from os import path
import sys

root = path.abspath('..')

if root not in sys.path:
    sys.path.append(root)

from directory.directory_server import run as run_directory
from directory.directory_server import Directory