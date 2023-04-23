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


def connect_another(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((ip, port))
        print('Start communicate with server: ', ip, port)
        msg_type, msg_subtype, msg_len, msg_sublen, msg = 0, 0, 0, 0, 0
        opt = int(input("For servers information press 0:\nFor clients information press 1:\nYour option:\t"))
        if opt == 0:
            msg_subtype = 1
            info = struct.pack('>bbhh', msg_type, msg_subtype, msg_len, msg_sublen)
            msg = sock.getsockname()[0], sock.getsockname()[1]
            print("testets: ", msg)
            sock.send(info)
        else:
            info = struct.pack('>bbhh', msg_type, msg_subtype, msg_len, msg_sublen)
            sock.send(info)

        # sock.send(mes_h.encode())
        # print('Sent: ', mes_h)
        data = sock.recv(1024)
        print('Received: ', data.decode())
    except ConnectionRefusedError:
        pass

def msg_handler(data, conn, conn_address):
    print("test", struct.unpack('>bbhh', data))
    msg_type, msg_subtype, msg_len, msg_sublen = struct.unpack('>bbhh', data)
    print(msg_type, " ", msg_subtype, " ", msg_len,  " ", msg_sublen)
    if msg_type == 0:
        res = f'{connected_servers}'.replace("'", "")
        res = res.replace("{", "").replace(" ", "").replace("}", "\0")
        conn.send(res.encode())
        print(res)
    elif msg_type == 2:
        if msg_subtype == 1:
            msg = conn.recv(msg_len)
            #print('Received: ', msg.decode())
            connected_clients.update({msg.decode(): conn_address})
            #print(f'test: {connected_clients}')
    elif msg_type == 1:
        msg = conn.recv(msg_len)
        print('Received: ', msg.decode())

def respond_to_other(conn, conn_address):
    print('Listening from: ', conn_address)
    connected_servers.update({conn_address[0]: conn_address[1]})
   # print(f'{connected_servers}')
    while True:
        data = conn.recv(1024)

        # msg: 0 0 0 0 , 0 1 0 0
        if not data: break

        print('Received: ', struct.unpack('>bbhh', data))
        # if recv_msg == '0 0 0 0':
        #     for server in connected_servers:
        #         serv = f'{server[0]}:{server[1]}'
        #         conn.send(serv.encode())

        msg_handler(data, conn, conn_address)
        # conn.send(mes_w.encode())
        # print('Sent: ', mes_w)


print('Listening on:', sock.getsockname())
# connected_servers.append(sock.getsockname())
connected_servers.update({sock.getsockname()[0]: sock.getsockname()[1]})
#print(f'test: {connected_servers}')

for i in port_arr:
    if i != port_arr[index]:
        threading.Thread(target=connect_another, args=('127.0.0.1', i)).start()

while True:
    conn_socket, client_address = sock.accept()
    print('New connection: ', client_address)
    threading.Thread(target=respond_to_other, args=(conn_socket, client_address)).start()
