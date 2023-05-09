import socket
import threading
import struct

servers_db = {}
clients_db = {}
connected_servers = {}
connected_clients = {}
A = '[NEW CONNECTION]'
B = '[LOST CONNECTION]'
C = f'[{socket.gethostname()}]'
W = '[WELCOME]'


def string_handler():
    result = ""
    for key in servers_db:
        result += f"{key}" + ':' + f"{servers_db[key]}" + "'/0'"
    return result


def msg_handler(server_socket, server_address):
    while True:
        data = server_socket.recv(6)
        if len(data) != 0:
            typeof, subtype, length, sub_len = struct.unpack('>bb hh', data)
            if typeof == 0:
                if typeof == 0:
                    server_socket.send(struct.pack('>bb hh', 1, 0, len(string_handler()), 0))
                    server_socket.send(string_handler().encode())
                if subtype == 1:
                    server_socket.send(struct.pack('>p', string_handler()))
            if typeof == 2:
                print(server_socket.getpeername())
                if subtype == 0:
                    a = server_socket.getpeername()
                    connected_servers[a] = server_socket
                    servers_db[server_address[1]] = server_address[0]
                    print(servers_db)
                if subtype == 1:
                    a = server_socket.getpeername()
                    connected_clients[a] = server_socket
                    name = server_socket.recv(length).decode()
                    clients_db[name] = server_address
            if typeof == 3:
                if subtype == 0:
                    sender = ' '
                    msg = (server_socket.recv(length)).decode()
                    msg1 = msg.split()
                    receiver = msg1[0]
                    client_address = server_socket.getpeername()
                    for name, value in clients_db.items():
                        if value == client_address:
                            sender = name
                            break
                    new_msg = msg + ' ' + sender
                    count = 0
                    for name, value in clients_db.items():
                        if name == receiver:
                            print(clients_db[name])
                            print(value)
                            connected_clients[value].send(struct.pack('>bb hh', 3, 0, len(new_msg), len(receiver)))
                            connected_clients[value].send(new_msg.encode())
                            count = 1
                            break
                    if count == 0:
                        for name1, value1 in connected_servers.items():
                            print(connected_servers[name1])
                            value1.send(struct.pack('>bb hh', 3, 1, len(new_msg), len(receiver)))
                            value1.send(new_msg.encode())
                if subtype == 1:
                    print('msg')
                    msg = server_socket.recv(length).decode()
                    msg1 = msg.split()
                    receiver = msg1[0]
                    for name, value in clients_db.items():
                        if name == receiver:
                            connected_clients[value].send(struct.pack('>bb hh', 3, 0, len(msg), len(receiver)))
                            connected_clients[value].send(msg.encode())
                            break


def connect_to_other(address, server_port):
    for keys, values in servers_db.items():
        if keys != address[1]:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_sock.bind(("127.0.0.1", server_port))
            server_sock.connect((values, keys))
            connected_servers[(values, keys)] = server_sock
            server_sock.send(struct.pack('>bb hh', 2, 0, 0, 0))
            threading.Thread(target=msg_handler, args=(server_sock, (values, keys),)).start()


def set_connection(server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('127.0.0.1', server_port))
    sock.listen(1)

    while True:
        server_socket, server_address = sock.accept()
        print(f'{A} --> {server_address[1]}\n')
        threading.Thread(target=msg_handler, args=(server_socket, server_address,)).start()


def main():
    ports = [1001, 1002, 1003, 1004, 1005]
    serverip = '127.0.0.1'
    servers = [(serverip, 1001), (serverip, 1002), (serverip, 1003), (serverip, 1004), (serverip, 1005)]
    while True:
        option = int(input(f'{C} : {serverip} \n1.\t1001\n2.\t1002\n3.\t1003\n4.\t1004\n5.\t1005\n[INPUT] -->\t')) - 1
        if 0 <= option < 5:
            break
        else:
            print('Invalid input!')
    server_port = ports[option]

    for i in range(len(ports)):
        if i != option:
            try:
                server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
                server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server_sock.bind(('127.0.0.1', server_port))
                server_sock.connect(servers[i])
                a = (servers[i])
                connected_servers[a] = server_sock
                print(f'{A} --> {ports[i]}')
                server_sock.send(struct.pack('>bb hh', 2, 0, 0, 0))
                servers_db[ports[i]] = servers[i][0]
                server_sock.send(struct.pack('>bb hh', 0, 0, 0, 0))
                data = server_sock.recv(6)
                typeof, subtype, length, sub_len = struct.unpack('>bb hh', data)
                if typeof == 1:
                    msg = server_sock.recv(length).decode()
                    if msg != 0:
                        ip_port_list = msg.split("'")
                        for ip_port_str in ip_port_list:
                            if ip_port_str != "" and ip_port_str != "/0":
                                ip, port = ip_port_str.split(":")
                                ip1 = int(ip)
                                if int(ip) != server_port:
                                    servers_db[ip1] = port
                    if len(servers_db) > 1:
                        connect_to_other(servers[i], server_port)
                threading.Thread(target=msg_handler, args=(server_sock, servers[i],)).start()
                break
            except ConnectionRefusedError:
                print(f'{B} --> {ports[i]}')

    threading.Thread(target=set_connection, args=(server_port,)).start()


if __name__ == '__main__':
    print(W)
    main()
