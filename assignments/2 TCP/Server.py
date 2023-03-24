import socket
import threading

port_arr = [1111, 2222, 3333, 4444, 5555]
index = int(input('Please select index number between 0 to 4\n'))
print(index)

def respond_to_client(conn_socket, client_address):
    print('start listening from', client_address)
    while True:
        data = conn_socket.recv(1024)
        if not data:
            break
        print('received from', client_address, 'text:', data.decode())
        conn_socket.sendall(b'Echo: ' + data)

    conn_socket.close()
    print('connection closed from', client_address)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
#sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', port_arr[index]))
sock.listen(1)

def try_to_connect_other_server(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.connect((ip, port))
        print('Start talking with server ~~ ', ip, port)
        sock.send(b"Hello")
        print('Sent Hello')
        data = sock.recv(1024)
        print('Received  ', data.decode())
    except ConnectionRefusedError:
        print("ConnectionRefusedError")

def respond_to_other(conn, conn_address):
    print('start listening from', conn_address)
    while True:
        data = conn.recv(1024)
        if not data: break
        print('Received  ', data.decode())
        conn.send('world'.encode())
        print('Sent - World')

print('listening on', sock.getsockname())

for i in port_arr:
    if i != port_arr[index]:
        print('test: ', i)
        threading.Thread(target=try_to_connect_other_server, args=('127.0.0.1', i)).start()

while True:
    conn_socket, client_address = sock.accept()
    print('new connection from', client_address)
    threading.Thread(target=respond_to_other, args=(conn_socket, client_address)).start()
