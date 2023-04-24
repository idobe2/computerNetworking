import socket
import threading
import struct

port_arr = [1111, 2222, 3333, 4444, 5555]
connected_servers = {}
connected_clients = {}
# msg_type, msg_subtype, msg_len, msg_sublen = 0, 0, 0, 0
# mes_h, mes_w = 'Hello', 'World'

while True:
    index = int(input('Please enter server number: [1, 2, 3, 4, 5]\n')) - 1
    if 0 <= index < 5:
        break
    else:
        print('Invalid input!')


def transmit_to_client(conn_socket, client_address):
    print('Start listening from: ', client_address)
    while True:
        data = conn_socket.recv(1024)
        if not data:
            break
        print('Received from: ', client_address, 'text:', data.decode())
        conn_socket.sendall(b'Echo: ' + data)

    conn_socket.close()
    print('Connection closed: ', client_address)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
# sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    sock.bind(('0.0.0.0', port_arr[index]))
    sock.listen(1)
except OSError:
    print("Server is busy!")
    exit(0)

def add_to_array(ip, port):
    pass


def connect_another(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((ip, port))
        print('Start communicate with server: ', ip, port)
        connected_servers.update({port: '0.0.0.0'})
        msg_type, msg_subtype, msg_len, msg_sublen, msg = 0, 0, 0, 0, 0
        opt = int(input("For servers information press 0:\nFor clients information press 1:\nYour option:\t"))
        if opt == 0:
            msg_subtype = 1
            info = struct.pack('>bbhh', msg_type, msg_subtype, msg_len, msg_sublen)
            print("testets: ", msg)
            sock.send(info)
        else:
            info = struct.pack('>bbhh', msg_type, msg_subtype, msg_len, msg_sublen)
            sock.send(info)

        # sock.send(mes_h.encode())
        # print('Sent: ', mes_h)
        data = sock.recv(1024)
        msg_handler(data, sock, sock.getsockname()[0])
        print('Received: here3 ', struct.unpack('>bbhh', data))
    except ConnectionRefusedError:
        pass


def msg_handler(data, conn, conn_address):
    print("test", struct.unpack('>bbhh', data))
    msg_type, msg_subtype, msg_len, msg_sublen = struct.unpack('>bbhh', data)
    print(msg_type, " ", msg_subtype, " ", msg_len, " ", msg_sublen)
    if msg_type == 0:
        print(f'resconn: {connected_servers}')
        res = f'{connected_servers}'.replace("'", "")
        res = res.replace("{", "").replace(" ", "").replace("}", "").replace(",", "\0")
        msg_type, msg_subtype, msg_len, msg_sublen = 1, 0, len(res), 0
        data = struct.pack('>bbhh', msg_type, msg_subtype, msg_len, msg_sublen)
        conn.send(data)
        print(f'res:{res}')
        conn.send(res.encode())
        print('sent2')
    elif msg_type == 2:
        if msg_subtype == 1:
            msg = conn.recv(msg_len)
            # print('Received: ', msg.decode())
            connected_clients.update({msg.decode(): conn_address})
            # print(f'test: {connected_clients}')
    elif msg_type == 1:
        msg = conn.recv(msg_len)
        my_list = msg.decode().split('\0')
        for item in my_list:
            key, value = item.split(':')
            connected_servers[key] = value
        print(f'ze ze{connected_servers}')
        print('Received: here ', msg.decode())


def respond_to_other(conn, conn_address):
    print('Listening from: ', conn_address)
    # print(f'conn2: {conn.getsockname()[1]}')
    # connected_servers.update({port_arr[index]: '0.0.0.0'})
    # print(f'array{connected_servers}')
    while True:
        data = conn.recv(1024)
        if data.decode() in port_arr:
            connected_servers.update({data.decode(): '0.0.0.0'})
        # msg: 0 0 0 0 , 0 1 0 0
        elif not data: break
        else:


            print('Received: here2', struct.unpack('>bbhh', data))
            # if recv_msg == '0 0 0 0':
            #     for server in connected_servers:
            #         serv = f'{server[0]}:{server[1]}'
            #         conn.send(serv.encode())

            msg_handler(data, conn, conn_address)
            # conn.send(mes_w.encode())
            # print('Sent: ', mes_w)


print('Listening on:', sock.getsockname())
# connected_servers.append(sock.getsockname())
print(f'conn1: {port_arr[index]}')
connected_servers.update({port_arr[index]: '0.0.0.0'})
# print(f'test: {connected_servers}')

for i in port_arr:
    if i != port_arr[index]:
        threading.Thread(target=connect_another, args=('127.0.0.1', i)).start()
        break


while True:
    conn_socket, client_address = sock.accept()
    print('New connection: ', client_address)
    threading.Thread(target=respond_to_other, args=(conn_socket, client_address)).start()
