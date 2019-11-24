import struct, traceback, select, sys
from pprint import pprint
from message import *
from event_handler import *

def listener(host, isserve):
    while True:
        if isserve:
            ready_to_read, ready_to_write, in_error = select.select([host.conn], [], [])
        else:
            ready_to_read, ready_to_write, in_error = select.select([host.conn], [host.conn], [])
        if host.bytes_to_receive == 0 and host.bytes_received == 0:
            conn_state = True
            try:
                itype = host.conn.recv(4) # TODO have to determine the size of header
                # print(itype)
            except ConnectionError:
                conn_state = False
            if len(itype) < 4:
                conn_state = False
            if not conn_state:
                host.conn.close()
            else:
                itype = struct.unpack('!I', itype)[0]
                print('type: ', itype)
                header = convert(itype, host)
                
                host.bytes_to_receive = header['Length']

        buffer = host.conn.recv(host.bytes_to_receive - host.bytes_received)
        # print(buffer, host.data_buffer)
        host.data_buffer += buffer
        print(host.data_buffer)
        host.bytes_received += len(buffer)
        
        if host.bytes_received == host.bytes_to_receive and (itype in [MessageType.login, MessageType.register] or host.bytes_received != 0):
            host.bytes_received = 0
            host.bytes_to_receive = 0
            try:
                handler(host, itype, header)
            except:
                pprint(sys.exc_info())
                traceback.print_exc(file=sys.stdout)
                pass