import socket, select, sys, threading
import struct, traceback
from pprint import pprint
from listen import *
# import secure

MAX_ONLINE = 5

users = {}

class ChatServer(threading.Thread):
    def __init__(self, conn):
        super(ChatServer, self).__init__()
        self.conn = conn
        self.bytes_to_receive = 0
        self.bytes_received = 0
        self.data_buffer = bytes()
    
    def run(self):
        listener(self, True)

def main(max_online):
    port = 12345
    socket_list = []

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
                # print(sock)
                connect, addr = server_socket.accept()
                # print(connect)
                # reply = "You are connected from: " + str(addr)
                # connect.send(reply.encode())
                server = ChatServer(connect)
                server.start()
            
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