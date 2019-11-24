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
    data_buffer = bytes()
    # print('in main ok')
    # recv_msg = client_socket.recv(1024)
    # print(recv_msg)
    # send_msg = input("Enter your user name(prefix with #):")
    # client_socket.send(send_msg.encode())

    while True:
        ready_to_read, ready_to_write, in_error = select.select([client_socket], [], [])

        if bytes_to_receive == 0 and bytes_received == 0:
            conn_state = True
            print('receive server')
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
                print(header)
                tmp = header.decode()
                print(tmp, tmp.startswith("Y"))
                if not tmp.startswith("Y"):
                    print('in unpack')
                    parameters = struct.unpack('!I24sI', header)
                    header = convert(parameters)
                    bytes_to_receive = header['Length']
        buffer = client_socket.recv(bytes_to_receive - bytes_received)
        print('before data_buffer', buffer)
        data_buffer += buffer
        print('after data_buffer')
        bytes_received += len(buffer)
        print('before send')
        if bytes_received == bytes_to_receive:
            bytes_to_receive = 0
            bytes_received = 0
            print('in send')
            try:
                # if header['Type'] == MessageType.send_message:
                #     print(data_buffer)
                message = input('input:').encode()
                date = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()).encode()
                length = len(message)
                itype = MessageType.send_message
                header = struct.pack('!I24sI', itype, date, length)
                client_socket.send(header + message)
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