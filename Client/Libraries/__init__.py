import os
import sys
sys.path.insert(0, os.getcwd()+'/files')
import ServerDitection
import socket

sys.dont_write_bytecode = True

IP = None
my_socket = None

IP = ServerDitection.server_scout().split("Here Be Server: ")[1]
my_socket = socket.socket()
my_socket.connect((IP, 23))