import socket, select, sys, threading
import struct, traceback
from pprint import pprint
from event_handler import *
from message import *
# import secure

MAX_ONLINE = 5

# class ChatServer(threading.Thread):
#     def __init__(self, conn, addr):
#         super(ChatServer, self).__init__()
#         self.conn = conn
#         self.addr = addr
    
#     def run(self):
#         while True:
#             try:
#                 ready_to_read, ready_to_write, in_error = select.select([self.conn], [], [])
#                 header = 
#             except:

def main(max_online):
    port = 12345
    socket_list = []
    users = {}
    bytes_to_receive = {}
    bytes_received = {}
    data_buffer = {}
    itype = 0
    parameters = []

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', port))
    server_socket.listen(max_online)
    socket_list.append(server_socket)
    while True:
        ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])
        for sock in ready_to_read:
            if sock == server_socket:
                # create_secure_channel(sock)
                print(sock)
                connect, addr = server_socket.accept()
                print(connect)
                # print("New connection from", addr)
                socket_list.append(connect)
                bytes_received[connect] = 0
                bytes_to_receive[connect] = 0
                reply = "You are connected from: " + str(addr)
                connect.send(reply.encode())
                continue
                # server = ChatServer(connect, addr)
                # server.start()
            if bytes_to_receive[sock] == 0 and bytes_received[sock] == 0:
                conn_state = True
                header = ''
                try:
                    header = sock.recv(32) # TODO have to determine the size of header
                    print(header)
                except ConnectionError:
                    conn_state = False
                if len(header) < 32:
                    conn_state = False
                if not conn_state:
                    sock.close()
                else:
                    parameters = struct.unpack('!I24sI', header)
                    header = convert(parameters)
                    bytes_to_receive[sock] = header['Length']

            buffer = sock.recv(bytes_to_receive[sock] - bytes_received[sock])
            data_buffer[sock] += buffer
            bytes_received[sock] += len(buffer)
            
            if bytes_received[sock] == bytes_to_receive[sock] and bytes_received[sock] != 0:
                bytes_received[sock] = 0
                bytes_to_receive[sock] = 0
                try:
                    handler(sock, itype, parameters)
                except:
                    pprint(sys.exc_info())
                    traceback.print_exc(file=sys.stdout)
                    pass
                # if data.startswith("#"):
                #     users[data[1:].lower()]=connect
                #     print("User " + data[1:] + " added.")
                #     reply = "Your user detail saved as: " + str(data[1:])
                #     connect.send(reply.encode())
                # elif data.startswith("@"):
                #     users[data[1:data.index(':')].lower()].send(data[data.index(':') + 1:].encode())
            
    server_socket.close()

if __name__ == '__main__':
    try:
        max_online = int(sys.args[1])
    except:
        max_online = MAX_ONLINE
    try:
        print("Server started with at most %d users online" % max_online)
        main(max_online)
    except:
        print("Server terminated.")