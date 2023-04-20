import socket
import threading


# import sys
# import time
# from random import randint

def handler(c, a):
    while True:
        data = c.recv(1024)
        for connection in connections:
            connection.send(data)
        if not data:
            print(str(a[0]) + ':' + str(a[1]), "disconnected")
            connections.remove(c)
            peers.remove(a[0])
            c.close()
            sendPeers()
            break


def sendPeers():
    p = ""
    for peer in peers:
        p = p + peer + ","
    for connection in connections:
        connection.send(b'\x11' + bytes(p, "utf-8"))


connections = []
peers = []

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', 10000))
sock.listen(1)
print("Server running...")
while True:
    c, a = sock.accept()
    cThread = threading.Thread(target=handler, args=(c, a))
    cThread.daemon = True
    cThread.start()
    connections.append(c)
    peers.append(a[0])
    print(str(a[0]) + ':' + str(a[1]), "connected")
    sendPeers()

#  if (len(sys.argv) > 1):
#      Client = Client(sys.argv[1])
# else: server = Server()

# def is_server_up(ip_addr):
#     return os.system('ping -c 1 ' + ip_addr + ' > /dev/null') == 0
#
# if is_server_up('127.0.0.1') == False:
#     server = Server()
# else:
#     client = Client(p2p.peers[0])

#
# while True:
#     try:
#         print("Trying to connect...")
#         server = Server()
#         time.sleep(randint(1,5))
#         for peer in p2p.peers:
#             try:
#                 client = Client(p2p.peers[0])
#             except KeyboardInterrupt:
#                 sys.exit(0)
#             except:
#                 pass
#             if randint(1, 20) == 1:
#                 try:
#                     server = Server()
#                 except KeyboardInterrupt:
#                     sys.exit(0)
#                 except:
#                     print("Couldn't start the server...")
#     except KeyboardInterrupt:
#         sys.exit(0)
