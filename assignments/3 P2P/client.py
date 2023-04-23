import socket
import threading
import struct


# import sys
# import time
# from random import randint

class p2p:
    peers = ['127.0.0.1']
    port_arr = [1111, 2222, 3333, 4444, 5555]


msg_type, msg_subtype, msg_len, msg_sublen, msg = 0, 0, 0, 0, 0


def sendMsg(sock):
    while True:
        opt = int(input("For configuring your user name press 2:\nFor sending massege press 3:\nYour option:\t"))
        if opt == 2:
            msg_type = 2
            msg_sublen = 0
            msg_subtype = 1
            msg = (socket.gethostname()).encode()
            msg_len = msg_sublen + len(msg)
        elif opt == 3:
            msg_type = 3
            msg_sublen = len(socket.gethostname())
            msg = (socket.gethostname()).encode()
            msg_len = msg_sublen + len(msg)

        # send = bytes(input(""), 'utf-8')
        data = struct.pack('>bbhh', msg_type, msg_subtype, msg_len, msg_sublen)
        sock.send(data)
        sock.send(msg)
        msg = 0
        # sock.send(bytes(input(""), 'utf-8'))


def updatePeers(peerData):
    p2p.peers = str(peerData, "utf-8").split(",")[:-1]


while True:
    index = int(input('Please select server to connect: [1, 2, 3, 4, 5]\n')) - 1
    if 0 <= index < 5:
        break
    else:
        print('Invalid input!')

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
