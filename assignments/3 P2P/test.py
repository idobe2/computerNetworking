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


try:
    sock.bind(('0.0.0.0', port_arr[index]))
    sock.listen(1)
except OSError:
    print("Server is busy!")
    exit(0)


def add_to_array(data, conn, conn_address):
    ip, port = data.decode().split(":")
    connected_servers.update({int(port): '0.0.0.0'})
    print(f'test array: {connected_servers}')


def connect_another(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((ip, port))
        print('Start communicate with server: ', ip, port)
        connected_servers.update({port: '0.0.0.0'})
        msg_type, msg_subtype, msg_len, msg_sublen = 0, 1, 0, 0
        data = str(ip) + ":" + str(port_arr[index])
        sock.send(data.encode())
        print('test DATA: ', len(data))
        info = struct.pack('>bbhh', msg_type, msg_subtype, msg_len, msg_sublen)
        print("test INFO:", struct.unpack('>bbhh', info), len(info))
        sock.send(info)
        data = sock.recv(1024)
        msg_handler(data, sock, sock.getsockname()[0])
        print('Received: here3 ', struct.unpack('>bbhh', data))
    except ConnectionRefusedError:
        pass


def msg_handler(data, conn, conn_address):
    print("test", struct.unpack('>bbhh', data))
    msg_type, msg_subtype, msg_len, msg_sublen = struct.unpack('>bbhh', data)
    print("TEST DATA:", msg_type, " ", msg_subtype, " ", msg_len, " ", msg_sublen)
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
            connected_clients.update({msg.decode(): conn_address})

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
    while True:
        data = conn.recv(1024)
        if data.decode() in port_arr:
            connected_servers.update({data.decode(): '0.0.0.0'})
        # msg: 0 0 0 0 , 0 1 0 0
        elif not data: break
        else:
            print("test len(data)", len(data))
            if len(data) == 6:
                msg_handler(data, conn, conn_address)
            else:
                add_to_array(data, conn, conn_address)


print('Listening on:', sock.getsockname())
print(f'conn1: {port_arr[index]}')
connected_servers.update({port_arr[index]: '0.0.0.0'})


for i in port_arr:
    if i != port_arr[index]:
        threading.Thread(target=connect_another, args=('127.0.0.1', i)).start()



while True:
    conn_socket, client_address = sock.accept()
    print('New connection: ', client_address)
    threading.Thread(target=respond_to_other, args=(conn_socket, client_address)).start()

