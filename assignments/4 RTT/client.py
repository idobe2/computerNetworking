import socket
import threading
import time
import struct

port_arr = [1001, 1002, 1003, 1004, 1005]
servers_db = {}
rtt_values = {}
typeof, subtype, length, sub_len, msg = 0, 0, 0, 0, 0
A = '[SEND]'
B = '[RECEIVED]'
C = '[FROM]'
D = '[SERVER UNAVAILABLE]'
E = 'Enter your name:'
F = 'Enter a username to send a message to:'
G = 'Enter your message:'


def send_msg(conn):
    name = input(f'{A}\n{E} ')
    conn.send(struct.pack('>bb hh', 2, 1, len(name), 0))
    conn.send(name.encode())
    conn.send(struct.pack('>bb hh', 0, 0, 0, 0))
    data = conn.recv(6)
    typeof, subtype, length, sub_len = struct.unpack('>bb hh', data)
    while True:
        sendto = input(f'{F} ')
        message = input(f'{G} ')
        message1 = sendto + ' ' + message
        msg_len = len(message1)
        conn.send(struct.pack('>bb hh', 3, 0, msg_len, len(sendto)))
        conn.send(message1.encode())


def CheckRTT(address, server_port):
    for keys, values in servers_db.items():
        if keys != address[1]:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_sock.bind(('127.0.0.1', server_port))
            server_sock.connect((values, keys))
            connected_servers[(values, keys)] = server_soc
            threading.Thread(target=msg_handler, args=(server_sock, (values, keys),)).start()

def main():
    while True:
        index = int(input('Please select server to connect: [1, 2, 3, 4, 5]\n')) - 1
        if 0 <= index < 5:
            break
        else:
            print('Invalid input!')

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect(('127.0.0.1', port_arr[index]))

        iThread = threading.Thread(target=send_msg, args=(sock,))
        iThread.daemon = True
        iThread.start()

        while True:
            data = sock.recv(6)
            if len(data) != 0:
                typeof, subtype, length, sub_len = struct.unpack('>bb hh', data)
                if typeof == 3:
                    msg = sock.recv(length)
                    message = msg.decode().split()
                    print(f'\n{B} {message[1]}')
                    print(f'{C} {message[2]}')
                    print(f'{F} ')
                if typeof == 1:
                    msg = sock.recv(length).decode()
                    if msg != 0:
                        ip_port_list = msg.split("'")
                        for ip_port_str in ip_port_list:
                            if ip_port_str != '' and ip_port_str != '/0':
                                print(f'Check: {ip_port_str}')
                                ip, port = ip_port_str.split(':')
                                ip1 = int(ip)
                                servers_db[ip1] = port
                    if len(servers_db) > 1:
                        CheckRTT(servers[i], server_port)
    except ConnectionRefusedError:
        print(D)

if __name__ == '__main__':
    main()