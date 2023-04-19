import socket
import threading

port_arr = [1111, 2222, 3333, 4444, 5555]
while True:
    index = int(input('Please enter server number: [1, 2, 3, 4, 5]\n')) - 1
    if 0 <= index < 5: break
    else: print('Invalid input!')
mes_h, mes_w = 'Hello', 'World'


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


def connect_another(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.connect((ip, port))
        print('Start communicate with server: ', ip, port)
        sock.send(mes_h.encode())
        print('Sent: ', mes_h)
        data = sock.recv(1024)
        print('Received: ', data.decode())
    except ConnectionRefusedError:
        pass


def respond_to_other(conn, conn_address):
    print('Listening from: ', conn_address)
    while True:
        data = conn.recv(1024)
        if not data: break
        print('Received: ', data.decode())
        conn.send(mes_w.encode())
        print('Sent: ', mes_w)


print('Listening on:', sock.getsockname())

for i in port_arr:
    if i != port_arr[index]:
        threading.Thread(target=connect_another, args=('127.0.0.1', i)).start()

while True:
    conn_socket, client_address = sock.accept()
    print('New connection: ', client_address)
    threading.Thread(target=respond_to_other, args=(conn_socket, client_address)).start()
