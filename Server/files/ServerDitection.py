    #-----------------------Imports-----------------------
import socket
import time
import subprocess
from uuid import getnode


#-----------------------Globals-----------------------
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP = s.getsockname()[0]
s.close()
MyMac = "-".join([hex(getnode()).split('0x')[1].split("L")[0][x:x+2] for x in range(0, 12, 2)]).upper()


#----------------------Functions----------------------
def subnet_calculator():
    global IP, MyMac
    stdout, stderr = subprocess.Popen(['ipconfig/all'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate()
    return '.'.join([str(int(''.join([''.join([bin(int(bin_ip))[2:].zfill(8) for bin_ip in IP.split('.')])[i] if int(''.join([bin(int(subnet))[2:].zfill(8) for subnet in [x for x in stdout.split("\r\n\r\n") if "Physical Address. . . . . . . . . : " + MyMac + "\r\n" in x][0].split("Subnet Mask")[1].split(". : ")[1].split("\r\n")[0].split('.')])[i]) else '1' for i in range(0, 32)])[final:final+8], 2)) for final in range(0, 32, 8)])


def server_emitter():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # Set a timeout so the socket does not block
    # indefinitely when trying to receive data.
    server.settimeout(0.2)
    server.bind(("", 44444))
    message = b"Here Be Server: " + IP
    subnet = subnet_calculator()
    while True:
        server.sendto(message, (subnet, 37020))
        time.sleep(1)


def server_scout():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.bind(("", 37020))
    while True:
        data, addr = client.recvfrom(1024)
        if data:
            if "Here Be Server: " in data and len(data.split("Here Be Server: ")) == 2:
                return data
