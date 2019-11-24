import socket, select, struct, threading
from pprint import pprint
import time, sys, traceback
from message import *
from listen import *

class ChatClient(threading.Thread):
    def __init__(self, conn):
        super(ChatClient, self).__init__()
        self.conn = conn
        self.bytes_to_receive = 0
        self.bytes_received = 0
        self.data_buffer = bytes()
    
    def run(self):
        listener(self, False)

def startup(sock):
    choice = input('login(0), register(1):')
    username = input('username:')
    password = input('password:')
    date = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
    if int(choice) == 0:
        itype = MessageType.login
        header = struct.pack('!I', itype)
        header += serial_pack([date, username, password, 0])
    else:
        itype = MessageType.register
        header = struct.pack('!I', itype)
        nickname = input('nickname:')
        header += serial_pack([date, username, password, nickname, 0])
    
    # print(header)
    sock.conn.send(header)

def main(dst, port):
    client_socket = socket.socket()
    client_socket.connect((dst, port))
    # reply = client_socket.recv(1024).decode()
    # print(reply)
    client = ChatClient(client_socket)
    client.start()
    startup(client)

    # client_socket.close()

if __name__ == '__main__':
    try:
        dst = int(sys.args[1])
    except:
        dst = '127.0.0.1'
    try:
        port = int(sys.argv[2])
    except:
        port = 12345
    try:
        print("in main")
        main(dst, port)
    except:
        print("Client terminated.")