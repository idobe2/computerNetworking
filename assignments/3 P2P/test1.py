import socket
import threading
import time
import struct

serverd = {}
clientd = {}
serversock = {}
clientsock = {}

def converttostringd():
    result = ""
    for key in serverd:
        result += f"{key}" + ':'+f"{serverd[key]}" + "'/0'"
    return result

def serverconnection(subtype, portop):
    arrlist=[]
    if subtype != 0:
        ip_port_list = subtype.split("'")
        for ip_port_str in ip_port_list:
            if ip_port_str != "":
                if ip_port_str != "/0":
                    print("TEST: ", f'{ip_port_str}')
                    ip, port = ip_port_str.split(":")
                    ip2 = int(ip)
                    if int(ip) != portop:
                        serverd[ip2] = port


def connecttoservers(address, portop):
    for keys, values in serverd.items():
        print(values)
        if keys != address[1]:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_sock.bind(("127.0.0.1", portop))
            server_sock.connect((values, keys))
            serversock[(values, keys)] = server_sock
            server_sock.send(struct.pack('>bbhh', 2, 0, 0, 0))
            threading.Thread(target=types, args=(server_sock,(values,keys),)).start()


def types(server_socket, server_address):
    while True:
        data = server_socket.recv(6)
        if len(data) != 0:
            typeh, subtype, lenh, sublen = struct.unpack('>bbhh', data)
            if typeh ==0:
                if typeh == 0:
                    server_socket.send(struct.pack('>bbhh', 1, 0, len(converttostringd()), 0))
                    server_socket.send(converttostringd().encode())
                if subtype == 1:
                    server_socket.send(struct.pack('>p', converttostringd()))
            if typeh == 2:
                print(server_socket.getpeername())
                if subtype == 0:
                    a = server_socket.getpeername()
                    serversock[a] = server_socket
                    serverd[server_address[1]] = server_address[0]
                    print(serverd)
                if subtype == 1:
                    a = server_socket.getpeername()
                    clientsock[a] = server_socket
                    name = server_socket.recv(lenh)
                    nname = name.decode()
                    clientd[nname] = server_address
            if typeh == 3:
                if subtype == 0:
                    sender = ' '
                    msg = server_socket.recv(lenh)
                    msg = msg.decode()
                    msg1 = msg.split
                    reciver = msg1[0]
                    clientadd = server_socket.getpeername()
                    for name, value in clientd.items:
                        if value == clientadd:
                            sender = name
                            break
                    newmsg = msg + ' ' + sender
                    count = 0
                    for name, value in clientd.items:
                        if name == reciver:
                            print(clientd[name])
                            print(value)
                            clientsock[value].send(struct.pack('>bbhh', 3, 0, len(newmsg), len(reciver)))
                            clientsock[value].send(newmsg.encode())
                            count = 1
                            break
                    if count == 0:
                        for name1, value1 in serversock.items:
                            print(serversock[1])
                            value1.send(struct.pack('>bbhh', 3, 1, len(newmsg), len(reciver)))
                            clientsock[value1].send(newmsg.encode())
                if subtype == 1:
                    print('msg')
                    msg  = server_socket.recv(lenh)
                    msg = msg.decode()
                    msg1 = msg.split
                    reciver = msg1[0]
                    for name, value in clientd.items:
                        if name == reciver:
                            clientsock[value].send(struct.pack('>bbhh', 3, 0, len(msg), len(reciver)))
                            clientsock[value].send(msg.encode())
                            break


def buildconnection(portop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('127.0.0.1', portop))
    sock.listen(1)

    while True:
        server_socket, server_address = sock.accept()
        print(server_socket)
        print(server_address)
        print(f'Connection from {server_address} accepted')
        threading.Thread(target=types, args=(server_socket, server_address,)).start()


def main():
    ports = [1111, 2222, 3333, 4444, 5555]
    serverip = '127.0.0.1'
    servers = [(serverip, 1111), (serverip, 2222), (serverip, 3333), (serverip, 4444), (serverip, 5555)]
    option = int(input(f'Select port number to connect server: {serverip} \n1-1111\n2-2222\n3-3333\n4-4444\n5-5555\n')) - 1
    portop = ports[option]

    for i in range(len(ports)):
        if i != option:
            try:
                server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
                server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server_sock.bind(("127.0.0.1", portop))
                server_sock.connect(servers[i])
                a = (servers[i])
                serversock[a] = server_sock
                print(f"Connected to {ports[i]}")
                server_sock.send(struct.pack('>bbhh', 2, 0, 0, 0))
                serverd[ports[i]] = servers[i][0]
                server_sock.send(struct.pack('>bbhh', 0, 0, 0, 0))
                data = server_sock.recv(6)
                typeh, subtype, lenh, sublen = struct.unpack('>bbhh', data)
                if typeh == 1:
                    msg = server_sock.recv(lenh)
                    msg1 = msg.decode()
                    serverconnection(msg1, portop)
                    if len(serverd) > 1:
                        connecttoservers(servers[i], portop)
                threading.Thread(target=types, args=(server_sock, servers[i],)).start()
                break
            except ConnectionRefusedError:
                print(f'Failed to connect to {ports[i]}')

    threading.Thread(target=buildconnection, args=(portop,)).start()


# while True:
#     server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
#     server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     conn_socket, client_address = server_sock.accept()
#     print('New connection: ', client_address)
#     threading.Thread(target=connecttoservers(), args=(conn_socket, client_address)).start()

if __name__ == '__main__':
    main()

