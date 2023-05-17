import socket
import threading
import time
import struct

port_arr = [1001, 1002, 1003, 1004, 1005]
servers_db = {}
rtt_values = {}
connected_servers = {}
connected_ports = []
rtt_array = []
connection_sockets = []
typeof, subtype, length, sub_len, msg = 0, 0, 0, 0, 0
serverip = '127.0.0.1'
servers = [(serverip, 1001), (serverip, 1002), (serverip, 1003), (serverip, 1004), (serverip, 1005)]
A = '[SEND]'
B = '[RECEIVED]'
C = '[FROM]'
D = '[SERVER UNAVAILABLE]'
E = 'Enter your name:'
F = 'Enter a username to send a message to:'
G = 'Enter your message:'
H = '[CONNECTION CLOSED]'


def build_connections():
    """
    Build connection with all the connected server from the received dictionary
    """
    for item in connected_servers:
        if item.split("'")[0] not in connected_ports:
            connected_ports.append(item.split("'")[0])
    for i in range(len(connected_ports)):
        conn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        conn_sock.connect(('127.0.0.1', int(connected_ports[i])))
        if conn_sock not in connection_sockets:
            connection_sockets.append(conn_sock)
        iThread = threading.Thread(target=CheckRTT, args=(conn_sock, connected_ports[i]))
        iThread.start()
        iThread.join()


def CheckRTT(sock, port):
    """
    Calculates the RTT and saves it in a dictionary
    :param sock: The socket we opened a connection to
    :param port: The port of this connection
    """
    start = time.time()
    sock.send(struct.pack('>bb hh', 4, 0, 0, 0))
    sock.recv(6)
    done = time.time()
    elapsed = done - start
    rtt_values.update({str(port): elapsed})


def send_msg(conn):
    """
    Sends a message to client user by name
    :param conn: The server we are connected to
    """
    while True:
        time.sleep(1)
        sendto = input(f'{F}\n')
        message = input(f'{G} ')
        message1 = sendto + ' ' + message
        msg_len = len(message1)
        conn.send(struct.pack('>bb hh', 3, 0, msg_len, len(sendto)))
        conn.send(message1.encode())


def main():
    """
    Build the first connection with the server we pick, received the messages by type and handle them.
    """
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
        connected_servers.update({str(port_arr[index]): '127.0.0.1'})
        name = input(f'{A}\n{E} ')
        sock.send(struct.pack('>bb hh', 0, 0, 0, 0))

        while True:
            data = sock.recv(6)
            if len(data) != 0:
                typeof, subtype, length, sub_len = struct.unpack('>bb hh', data)
                if typeof == 3:
                    msg = sock.recv(length)
                    message = msg.decode().split()
                    print(B, end=' ')
                    for i in range(1, len(message) - 1):
                        print(message[i], end=' ')
                    print('\n')
                    print(f'{C} {message[len(message)-1]}')
                    print(f'{F} ')
                if typeof == 1:
                    msg = sock.recv(length).decode()
                    if msg != 0:
                        ip_port_list = msg.split("'")
                        for ip_port_str in ip_port_list:
                            if ip_port_str != '' and ip_port_str != '/0':
                                ip, port = ip_port_str.split(':')
                                ip1 = int(ip)
                                servers_db[ip1] = port
                                connected_servers[ip] = port
                        build_connections()
                        rtt_array = list(rtt_values.values())
                        print(f'RTT: {rtt_values}')
                        min_rdt = 1000.0
                        position_rdt = -1
                        for i in range(len(rtt_array)):
                            if float(rtt_array[i]) < min_rdt:
                                min_rdt = float(rtt_array[i])
                                position_rdt = i
                        for i in range(len(connection_sockets)):
                            if i != position_rdt:
                                connection_sockets[i].send(struct.pack('>bb hh', 4, 1, 0, 0))
                                connection_sockets[i].close()
                            else:
                                sock = connection_sockets[i]

                        for i in range(len(connected_ports)):
                            if i != position_rdt:
                                print(f'{H} --> {connected_ports[i]}')
                        sock.send(struct.pack('>bb hh', 2, 1, len(name), 0))
                        sock.send(name.encode())
                        threading.Thread(target=send_msg, args=(sock,)).start()

    except ConnectionRefusedError:
        print(D)
    except ConnectionResetError:
        print(H)


if __name__ == '__main__':
    main()
