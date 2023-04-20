import socket
import threading
# import sys
# import time
# from random import randint

class p2p:
    peers = ['127.0.0.1']

def sendMsg(sock):
    while True:
        sock.send(bytes(input(""), 'utf-8'))

def updatePeers(peerData):
    p2p.peers = str(peerData, "utf-8").split(",")[:-1]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.connect(('127.0.0.1', 10000))

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



