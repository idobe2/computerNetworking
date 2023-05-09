import socket
import threading
import struct

serv_ip = "127.0.0.1"
port_arr = [1111, 2222, 3333, 4444, 5555]
servers = [(serv_ip, 1111), (serv_ip,2222), (serv_ip,3333), (serv_ip,4444), (serv_ip,5555)]
connected_servers = {}
connected_clients = {}
serv_sock = {}
client_sock = {}
# msg_type, msg_subtype, msg_len, msg_sublen = 0, 0, 0, 0
# mes_h, mes_w = 'Hello', 'World'

while True:
    index = int(input('Please enter server number: [1, 2, 3, 4, 5]\n')) - 1
    if 0 <= index < 5:
        break
    else:
        print('Invalid input!')
port_option = port_arr[index]

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
    sock.bind(("127.0.0.1", port_option))
    sock.listen(1)
except OSError:
    print("Server is busy!")
    exit(0)


def add_to_array(data, conn, conn_address):
    ip, port = data.decode().split(":")
    connected_servers.update({int(port): '0.0.0.0'})
    print(f'test array: {connected_servers}')


def connect_another(ip, port):
    for i in range(len(port_arr)):
        if(port_arr[i] != port_option):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind(("127.0.0.1", port_option))
                sock.connect(servers[i])
                a = servers[i]
                serv_sock[a] = serv_sock
                print("Connected")
                print('Start communicate with server: ', ip, port)
                #connected_servers.update({port: '0.0.0.0'})

                msg_type, msg_subtype, msg_len, msg_sublen = 2, 0, 0, 0 # identify
                send = struct.pack('>bbhh', msg_type, msg_subtype, msg_len, msg_sublen)
                sock.send(send)

                msg_type, msg_subtype, msg_len, msg_sublen = 0, 0, 0, 0
                # data = str(ip) + ":" + str(port_arr[index])
                # sock.send(data.encode())
                # print('test DATA: ', len(data))
                info = struct.pack('>bbhh', msg_type, msg_subtype, msg_len, msg_sublen)
                print("test INFO:", struct.unpack('>bbhh', info), len(info))
                sock.send(info)
                data = sock.recv(6)
                #msg_handler(sock, sock.getsockname()[0])
                print('Received: here3 ', struct.unpack('>bbhh', data))


                threading.Thread(target=msg_handler, args=('127.0.0.1', port_arr[index]),).start() # 1

            except ConnectionRefusedError:
                print("Connection failed")

def msg_handler(conn, conn_address):
    while True:
        data = conn.recv(6)
        if len(data) != 0:
            msg_type, msg_subtype, msg_len, msg_sublen = struct.unpack('>bbhh', data)
            if msg_type ==0:
                if msg_subtype == 0:
                    conn.send(struct.pack('>bbhh', 1, 0, len(convert()), 0))
                    conn.send(convert().encode())
                if msg_subtype == 1:
                    conn.send(struct.pack('>p', convert()))
            if msg_type == 2:
                if msg_subtype == 0:
                    print("Enter to 2")
                    a = conn.getpeername()
                    serv_sock[a] = conn
                    connected_servers[conn_address[1]] = conn_address[0]
                if msg_subtype == 1:
                    a = conn.getpeername()
                    client_sock[a] = conn
                    name = conn.recv(msg_len)
                    nname = name.decode()
                    connected_clients[nname] = conn_address





# def msg_handler(conn, conn_address):
#     data = conn.recv(1024)
#     print("msg data len: ", len(data))
#     print("test", struct.unpack('>bbhh', data))
#     msg_type, msg_subtype, msg_len, msg_sublen = struct.unpack('>bbhh', data)
#     print("TEST DATA:", msg_type, " ", msg_subtype, " ", msg_len, " ", msg_sublen)
#     if msg_type == 0:
#         print(f'resconn: {connected_servers}')
#         res = f'{connected_servers}'.replace("'", "")
#         res = res.replace("{", "").replace(" ", "").replace("}", "").replace(",", "\0")
#         msg_type, msg_subtype, msg_len, msg_sublen = 1, 0, len(res), 0
#         data = struct.pack('>bbhh', msg_type, msg_subtype, msg_len, msg_sublen)
#         conn.send(data)
#         print(f'res:{res}')
#         conn.send(res.encode())
#         print('sent2')
#
#     elif msg_type == 2:
#         if msg_subtype == 1:
#             msg = conn.recv(msg_len)
#             connected_clients.update({msg.decode(): conn_address})
#
#     elif msg_type == 1:
#         msg = conn.recv(msg_len)
#         my_list = msg.decode().split('\0')
#         for item in my_list:
#             key, value = item.split(':')
#             connected_servers[key] = value
#         print(f'ze ze{connected_servers}')
#         print('Received: here ', msg.decode())

def convert ():
    result = ''
    for key in connected_servers:
        result +=f"{key}" + ":" + f"{connected_servers[key]}"+"'/0'"
    return result
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
                msg_handler(conn, conn_address)
            else:
                add_to_array(data, conn, conn_address)


def wait_for_connection(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('127.0.0.1', port))
    sock.listen(1)
    while True:
        server_socket, server_address = sock.accept()
        threading.Thread(target=msg_handler, args=(server_socket, server_address,)).start()






print('Listening on:', sock.getsockname())
print(f'conn1: {port_arr[index]}')
connected_servers.update({port_arr[index]: '0.0.0.0'})


# for i in port_arr:
#     if i != port_arr[index]:
#         #threading.Thread(target=connect_another, args=('127.0.0.1', i)).start()
#         connect_another('127.0.0.1', i)
#         break

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((serv_ip, port_option))
connect_another('127.0.0.1', port_option)

threading.Thread(target=wait_for_connection, args=(port_arr[index],)).start()


# while True:
#     conn_socket, client_address = sock.accept()
#     print('New connection: ', client_address)
#     threading.Thread(target=respond_to_other, args=(conn_socket, client_address)).start()

