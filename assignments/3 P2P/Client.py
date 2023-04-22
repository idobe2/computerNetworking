import socket
import threading


# import sys
# import time
# from random import randint

class p2p:
    peers = ['127.0.0.1']
    port_arr = [1111, 2222, 3333, 4444, 5555]


def sendMsg(sock):
    while True:
        sock.send(bytes(input(""), 'utf-8'))


def updatePeers(peerData):
    p2p.peers = str(peerData, "utf-8").split(",")[:-1]

while True:
    index = int(input('Please select server to connect: [1, 2, 3, 4, 5]\n')) - 1
    if 0 <= index < 5: break
    else: print('Invalid input!')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.connect(('127.0.0.1', p2p.port_arr[index]))

iThread = threading.Thread(target=sendMsg, args=(sock,))
iThread.daemon = True
iThread.start()

while True:
    data = sock.recv(1024)
    if not data:
        break
    if data[0:1] == b'\x11':
        updatePeers(data[1:])
    else:
        print(str(data, 'utf-8'))
