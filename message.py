import enum, struct
class MessageType(enum.IntEnum):
    login = 1
    register = 2
    add_friend = 3
    resolve_friend_request = 4
    send_message = 5
    join_room = 6
    create_room = 7
    query_room_users = 8

    login_successful = 100
    register_successful = 101

    wrong_password = 201
    user_not_exist = 202
    other_host_login = 203
    username_taken = 204

type_mapping = {
    'int': 1,
    'str': 2,
}

def pack_str(topack):
    body = topack.encode()
    return bytes([type_mapping['str']]) + struct.pack('!I', len(body)) + body

def pack_int(topack):
    return bytes([type_mapping['int']]) + struct.pack('!I', topack)

pack_map = {
    'str': pack_str,
    'int': pack_int,
}

def pack_by_type(topack):
    # print(topack, type(topack).__name__, type_mapping[type(topack).__name__])
    result = pack_map[type(topack).__name__](topack)
    
    return result

def serial_pack(parameters):
    body = bytearray()
    # print(parameters)
    body += struct.pack('!I', len(parameters))
    for i in range(len(parameters)):
        body += pack_by_type(parameters[i])
    return body

def serial_unpack(host):
    header = []
    cnt = struct.unpack('!I', host.conn.recv(4))[0]
    for i in range(cnt):
        itype = host.conn.recv(1)
        if len(itype) == 0:
            break
        itype = ord(itype)
        if itype == 1:
            num = struct.unpack('!I', host.conn.recv(4))[0]
            header.append(num)
        elif itype == 2:
            strlen = struct.unpack('!I', host.conn.recv(4))[0]
            stri = host.conn.recv(strlen).decode()
            header.append(stri)
    return header 

def login_parsing(parameters):
    print('in login_parsing')
    header = {}
    header['Date'] = parameters[0]
    header['Username'] = parameters[1]
    header['Password'] = parameters[2]
    header['Length'] = parameters[3]
    print(header)
    return header

def login_successful_parsing(parameters):
    print('login_successful_parsing')
    header = {}
    header['ID'] = parameters[0]
    header['Username'] = parameters[1]
    header['Nickname'] = parameters[2]
    header['Date'] = parameters[3]
    header['Length'] = parameters[4]
    print(header)
    return header

def register_parsing(parameters):
    print('in register_parsing')
    header = {}
    header['Date'] = parameters[0]
    header['Username'] = parameters[1]
    header['Password'] = parameters[2]
    header['Nickname'] = parameters[3]
    header['Length'] = parameters[4]
    print(header)
    return header

def register_successful_parsing(parameters):
    print('register_successful_parsing')
    header = {}
    header['ID'] = parameters[0]
    header['Date'] = parameters[1]
    header['Length'] = parameters[2]
    print(header)
    return header

def username_taken_parsing(parameters):
    print('username_taken_parsing')
    header = {}
    header['Date'] = parameters[0]
    header['Length'] = parameters[1]
    print(header)
    return header

def message_parsing(host):
    header = {}
    parameters = host.conn.recv(32)
    header['Date'] = parameters[0].decode()
    header['User'] = parameters[1].decode()
    header['Length'] = parameters[2].decode()
    return header

header_parsing = {
    MessageType.login: login_parsing,
    MessageType.register: register_parsing,
    # MessageType.add_friend: add_friend,
    # MessageType.resolve_friend_request: resolve_friend_request,
    MessageType.send_message: message_parsing,
    # MessageType.join_room: join_room,
    # MessageType.create_room: create_room,
    # MessageType.query_room_users: query_room_users,
    MessageType.login_successful: login_successful_parsing,
    MessageType.register_successful: register_successful_parsing,
    MessageType.username_taken: username_taken_parsing,
}

def convert(itype, host):
    parameters = serial_unpack(host)
    header = header_parsing[itype](parameters)
    return header
