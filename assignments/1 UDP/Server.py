import socket

UDP_IP = '0.0.0.0'
UDP_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
sock.bind((UDP_IP, UDP_PORT))

clients = {}

while True:
    data, addr = sock.recvfrom(1024)
    cname = data.decode().rsplit(' ')[0]
    pack = data.decode().split()
    if(cname not in clients.keys() and len(pack)==1):
        print("Welcome", cname)
        clients[cname] = addr
        print(clients)
        clients[data.decode()] = addr
        my_message = 'Enter your message: <reciever> <text>'
        sock.sendto(my_message.encode(), addr)
    else:
        name = data.decode().rsplit(' ')[0]
        if name not in clients.keys():
            sock.sendto('Client not exist'.encode(), addr)
        else:
            sock.sendto(data, clients.get(name))