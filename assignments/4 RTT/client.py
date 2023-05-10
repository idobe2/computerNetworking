import socket
import threading
import struct

port_arr = [1001, 1002, 1003, 1004, 1005]

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
    while True:
        sendto = input(f'{F} ')
        message = input(f'{G} ')
        message1 = sendto + ' ' + message
        msg_len = len(message1)
        conn.send(struct.pack('>bb hh', 3, 0, msg_len, len(sendto)))
        conn.send(message1.encode())


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
except ConnectionRefusedError:
    print(D)
