import struct, time

type_mapping = {
    'int': 1,
    'str': 2,
    'bool': 3,
    'dict': 4,
    'list': 5,
    'none': 6,
}
# type + lengthof(str) + str
def pack_str(topack):
    body = topack.encode()
    return bytes([type_mapping['str']]) + struct.pack('!I', len(body)) + body

# type + int
def pack_int(topack):
    return bytes([type_mapping['int']]) + struct.pack('!I', topack)

def pack_bool(topack):
    return bytes([type_mapping['bool']]) + struct.pack('!?', topack)

# type + lenthof(dict)
# - items
def pack_dict(topack):
    num = len(topack)
    body = bytes([type_mapping['dict']]) + struct.pack('!B', num)
    for key in topack.keys():
        value = topack.get(key)
        body += pack_by_type(key)
        if value is None:
            body += pack_by_type([])
        else:
            body += pack_by_type(value)
    return body

# type + lenthof(list)
# - items
def pack_list(topack):
    num = len(topack)
    body = bytes([type_mapping['list']]) + struct.pack('!B', num)
    for i in range(num):
        body += pack_by_type(topack[i])
    # print(body)
    return body

pack_map = {
    'str': pack_str,
    'int': pack_int,
    'bool': pack_bool,
    'dict': pack_dict,
    'list': pack_list,
}

def pack_by_type(topack):
    # print(topack, type(topack).__name__, type_mapping[type(topack).__name__])
    result = pack_map[type(topack).__name__](topack)
    return result

def serial_header_pack(type, parameters=None):
    # body = bytearray()
    # print(parameters)
    body = struct.pack('!I', type)
    date = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()).encode()
    body += struct.pack('!24s', date)
    if parameters is None:
        num = 0
    else:
        num = len(parameters)
    body += struct.pack('!B', num)
    for i in range(num):
        body += pack_by_type(parameters[i])
    # print(body)
    return body

def serial_data_pack(parameters=None):
    body = bytearray()
    # print(parameters)
    body = struct.pack('!B', len(parameters))
    for i in range(len(parameters)):
        # print(parameters[i])
        body += pack_by_type(parameters[i])
    return body

def unpack_str(host):
    strlen = struct.unpack('!I', host.conn.recv(4))[0]
    return host.conn.recv(strlen).decode()

def unpack_int(host):
    return struct.unpack('!I', host.conn.recv(4))[0]

def unpack_bool(host):
    return struct.unpack('!?', host.conn.recv(1))[0]

def unpack_dict(host):
    body = {}
    cnt = struct.unpack('!B', host.conn.recv(1))[0]
    for i in range(cnt):
        key = unpack_by_type(host)
        value = unpack_by_type(host)
        body[key] = value
    return body

def unpack_list(host):
    body = []
    cnt = struct.unpack('!B', host.conn.recv(1))[0]
    for i in range(cnt):
        tmp = unpack_by_type(host)
        body.append(tmp)
    return body

unpack_map = {
    'str': unpack_str,
    'int': unpack_int,
    'bool': unpack_bool,
    'dict': unpack_dict,
    'list': unpack_list,
}

def unpack_by_type(host):
    # print(topack, type(topack).__name__, type_mapping[type(topack).__name__])
    itype = ord(host.conn.recv(1))
    # print(itype)
    func = [k for k, v in type_mapping.items() if v == itype][0]
    result = unpack_map[func](host)
    return result

def serial_unpack(host):
    header = []
    header.append(host.conn.recv(24).decode())
    cnt = struct.unpack('!B', host.conn.recv(1))[0]
    for i in range(cnt):
        tmp = unpack_by_type(host)
        header.append(tmp)
    return header

def serial_data_unpack(host):
    data = []
    cnt = struct.unpack('!B', host.conn.recv(1))[0]
    for i in range(cnt):
        tmp = unpack_by_type(host)
        data.append(tmp)
    return data
