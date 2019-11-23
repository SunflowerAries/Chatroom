import socket, select, struct, sys, traceback
from message import *
from pprint import pprint
import time
# class ChatServer(threading.Thread):
#     def __init__(self, conn, addr):
#         super(ChatServer, self).__init__()
#         self.conn = conn
#         self.addr = addr
    
#     def run(self):
#         while True:
#             try:
#                 ready_to_read, ready_to_write, in_error = select.select([self.conn], [], [])
#             except:

def main(dst, port):
    client_socket = socket.socket()
    client_socket.connect((dst, port))

    bytes_to_receive = 0
    bytes_received = 0
    data_buffer = ''

    # recv_msg = client_socket.recv(1024)
    # print(recv_msg)
    # send_msg = input("Enter your user name(prefix with #):")
    # client_socket.send(send_msg.encode())

    while True:
        ready_to_read, ready_to_write, in_error = select.select([client_socket], [], [])
        if bytes_to_receive == 0 and bytes_received == 0:
            conn_state = True
            header = ''
            try:
                header = client_socket.recv(32)
            except ConnectionError:
                conn_state = False
            if len(header) < 32:
                conn_state = False
            if not conn_state:
                print('服务器已关闭')
            else:
                parameters = struct.unpack('!I24sI', header)
                header = convert(parameters)
                bytes_to_receive = header['Length']
        buffer = client_socket.recv(bytes_to_receive - bytes_received)
        data_buffer += buffer
        bytes_received += len(buffer)
        if bytes_received == bytes_to_receive:
            bytes_to_receive = 0
            bytes_received = 0

            try:
                if header['Type'] == MessageType.send_message:
                    print(data_buffer)
                    message = input()
                    date = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
                    length = len(message)
                    itype = MessageType.send_message
                    header = struct.pack('!I24sI', itype, date, length)
                    client_socket.send(header, message)
            except:
                pprint(sys.exc_info())
                traceback.print_exc(file=sys.stdout)
                pass

        # recv_msg = client_socket.recv(1024).decode()
        # print(recv_msg)
        # send_msg = input("Send your message in format [@user:message]")
        # if send_msg == 'exit':
        #     break
        # else:
        #     client_socket.send(send_msg.encode())
    client_socket.close()

if __name__ == '__main__':
    dst = 0
    port = 0
    try:
        dst = int(sys.args[1])
        port = int(sys.argv[2])
    except:
        dst = '127.0.0.1'
        port = 12345
    try:
        main(dst, port)
    except:
        print("Client terminated.")