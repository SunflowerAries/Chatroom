import enum
from pack import *

class MessageType(enum.IntEnum):
    login = 1
    register = 2
    add_friend = 3
    resolve_friend_request = 4
    send_message = 5
    join_room = 6
    create_room = 7
    query_room_users = 8
    query_friend = 9

    login_successful = 100
    register_successful = 101
    wrong_password = 102
    user_not_exist = 103
    username_taken = 104
    friend_found = 105
    friend_not_found = 106

    friend_online = 200
    friend_offline = 201
    room_mem_online = 202
    room_mem_offline = 203
    other_host_login = 204
    
    

have_datagram = [MessageType.send_message, MessageType.login_successful]

def login_parsing(parameters):
    print('login_parsing')
    header = {}
    header['Date'] = parameters[0]
    header['Username'] = parameters[1]
    header['Password'] = parameters[2]
    print(header)
    return header

def login_successful_parsing(parameters):
    print('login_successful_parsing')
    header = {}
    header['Date'] = parameters[0]
    header['ID'] = parameters[1]
    header['Username'] = parameters[2]
    header['Nickname'] = parameters[3]
    print(header)
    return header

def register_parsing(parameters):
    print('register_parsing')
    header = {}
    header['Date'] = parameters[0]
    header['Username'] = parameters[1]
    header['Password'] = parameters[2]
    header['Nickname'] = parameters[3]
    print(header)
    return header

def register_successful_parsing(parameters):
    print('register_successful_parsing')
    header = {}
    header['Date'] = parameters[0]
    header['ID'] = parameters[1]
    header['Username'] = parameters[2]
    header['Nickname'] = parameters[3]
    print(header)
    return header

def username_taken_parsing(parameters):
    print('username_taken_parsing')
    header = {}
    header['Date'] = parameters[0]
    print(header)
    return header

def user_not_exist_parsing(parameters):
    print('user_not_exist_parsing')
    header = {}
    header['Date'] = parameters[0]
    print(header)
    return header

def wrong_password_parsing(parameters):
    print('wrong_password_parsing')
    header = {}
    header['Date'] = parameters[0]
    print(header)
    return header

def other_host_login_parsing(parameters):
    print('other_host_login_parsing')
    header = {}
    header['Date'] = parameters[0]
    print(header)
    return header

def friend_online_parsing(parameters):
    print('friend_online_parsing')
    header = {}
    header['Date'] = parameters[0]
    header['User'] = parameters[1]
    print(header)
    return header

def room_mem_online_parsing(parameters):
    print('room_mem_online_parsing')
    header = {}
    header['Date'] = parameters[0]
    header['Room'] = parameters[1]
    header['User'] = parameters[2]
    print(header)
    return header

def message_parsing(host):
    header = {}
    parameters = host.conn.recv(32)
    header['Date'] = parameters[0].decode()
    header['User'] = parameters[1].decode()
    return header

def friend_found_parsing(parameters):
    print('friend_found_parsing')
    header = {}
    header['Date'] = parameters[0]
    return header

def friend_not_found_parsing(parameters):
    print('friend_not_found_parsing')
    header = {}
    header['Date'] = parameters[0]
    return header

def query_friend_parsing(parameters):
    print('query_friend_parsing')
    header = {}
    header['Date'] = parameters[0]
    header['Name'] = parameters[1]
    print(header)
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
    MessageType.query_friend: query_friend_parsing,
    MessageType.login_successful: login_successful_parsing,
    MessageType.register_successful: register_successful_parsing,
    MessageType.username_taken: username_taken_parsing,
    MessageType.user_not_exist: user_not_exist_parsing,
    MessageType.wrong_password: wrong_password_parsing,
    MessageType.other_host_login: other_host_login_parsing,
    MessageType.friend_online: friend_online_parsing,
    MessageType.room_mem_online: room_mem_online_parsing,
    MessageType.friend_found: friend_found_parsing,
    MessageType.friend_not_found: friend_not_found_parsing,
}

def convert(itype, host):
    parameters = serial_unpack(host)
    header = header_parsing[itype](parameters)
    return header
