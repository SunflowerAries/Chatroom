import socket, time
from message import *
from pack import *
import database
from try1 import Window

callback_func = []

def add_listener(func):
    callback_func.append(func)

def login(sock, parameters):
    print('in login')
    c = database.get_cursor()
    fields = ['ID', 'Username', 'Nickname', 'Password']
    # print(','.join(fields), parameters['Username'])
    # print('SELECT ' + ','.join(fields) + ',Password' + ' from Users where Username=%s' % (parameters['Username']))
    result = c.execute('SELECT ' + ','.join(fields) + ' from Users where Username=?', (parameters['Username'], ))
    rows = result.fetchall()

    if len(rows) == 0:
        header = serial_header_pack(MessageType.user_not_exist)
        sock.conn.send(header)
        return
    
    match = False
    cnt = 0
    for i in range(len(rows)):
        if rows[i][3] == parameters['Password']:
            match = True
            cnt = i
            user = dict(zip(fields, rows[i]))
            break
    
    if not match:
        header = serial_header_pack(MessageType.wrong_password)
        sock.conn.send(header)
        return
    
    if user['ID'] in database.user_id_to_host:
        old_host = database.user_id_to_host[user['ID']]
        header = serial_header_pack(MessageType.other_host_login)
        old_host.conn.send(header)
        old_host.close()
        database.kickout_host(old_host)
    
    database.user_id_to_host[user['ID']] = sock
    # ID Username Nickname
    tmp = list(rows[cnt][0:3])
    
    # print(header)
    # print(sock.conn)
    
    related = {}
    room_list = database.get_user_room(user['ID'])
    related['Room'] = room_list
    # 发送好友请求
    # TODO: serial_header_pack have to deal with [[]]
    friend_list = database.get_pending_friend_request(user['ID'])
    for friend in friend_list:
        iheader = serial_header_pack(MessageType.add_friend, friend)
        sock.conn.send(iheader)
    
    # 通知好友自己上线
    friend_list = database.get_friends(user['ID'])
    related['Friend'] = friend_list
    for friend in friend_list:
        if friend['ID'] in database.user_id_to_host:
            iheader = serial_header_pack(MessageType.friend_online, [user['ID']])
            database.user_id_to_host[friend['ID']].conn.send(iheader)
    
    # 通知群成员自己上线
    for room in room_list:
        mems_id = database.get_room_members_id(room['ID'])
        for mem_id in mems_id:
            if mem_id in database.user_id_to_host and mem_id != user['ID']:
                iheader = serial_header_pack(MessageType.room_mem_online, [room['ID'], user['ID']])
                database.user_id_to_host[mem_id].conn.send(iheader)
    
    # TODO: login_successful need length field
    
    related['Message'] = database.get_chat_history(user['ID'])
    # print(related)
    data = serial_data_pack([related])
    print(data)
    tmp.append(len(data))
    header = serial_header_pack(MessageType.login_successful, tmp)
    sock.conn.send(header + data)

def login_successful(self, parameters):
    print('login_successful')
    # print(parameters)
    self.clearField()
    if self.handler_for_login_logup in callback_func:
        callback_func.remove(self.handler_for_login_logup)
    Window1 = Window()
    Window1.show()
    data = serial_data_unpack(self.sock)
    print(data)
    self.close()
    

def user_not_exist(self, parameters):
    print('user_not_exist')
    self.prompt(self.UsernameInput, 1)
    print(parameters)

def wrong_password(self, parameters):
    print('wrong_password')
    self.prompt(self.PasswordInput, 1)
    print(parameters)

def other_host_login(sock, parameters):
    print('other_host_login')
    print(parameters)

def friend_online(sock, parameters):
    print('friend_online')
    print(parameters)

def room_mem_online(sock, parameters):
    print('room_mem_online')
    print(parameters)

def register(sock, parameters):
    print('register')
    c = database.get_cursor()
    r = c.execute('SELECT * from Users where Username=?', [parameters['Username']])
    rows = r.fetchall()
    if len(rows) > 0:
        header = serial_header_pack(MessageType.username_taken)
        sock.conn.send(header)
        return
    c.execute('INSERT into Users (Username,Password,Nickname) values (?,?,?)',
              [parameters['Username'], parameters['Password'], parameters['Nickname']])
    header = serial_header_pack(MessageType.register_successful, [c.lastrowid])
    # print(sock)
    sock.conn.send(header)

def register_successful(self, parameters):
    print('register_successful')
    self.clearField()
    if self.handler_for_login_logup in callback_func:
            callback_func.remove(self.handler_for_login_logup)
    self.close()
    # print(parameters)

def username_taken(self, parameters):
    print('username_taken')
    self.prompt(self.UsernameInput, 1)
    print(parameters)

def add_friend(sock, parameters):
    print('in add_friend')

def resolve_friend_request(sock, parameters):
    print('in resolve_friend_request')

def send_message(sock, parameters):
    print('in send_message')

def join_room(sock, parameters):
    print('in join_room')

def create_room(sock, parameters):
    print('in create_room')

def query_room_users(sock, parameters):
    print('in query_room_users')

event_hander_map = {
    MessageType.login: login,
    MessageType.register: register,
    MessageType.add_friend: add_friend,
    MessageType.resolve_friend_request: resolve_friend_request,
    MessageType.send_message: send_message,
    MessageType.join_room: join_room,
    MessageType.create_room: create_room,
    MessageType.query_room_users: query_room_users,
    # MessageType.login_successful: login_successful,
    # MessageType.register_successful: register_successful,
    # MessageType.username_taken: username_taken,
    # MessageType.user_not_exist: user_not_exist,
    # MessageType.wrong_password: wrong_password,
    MessageType.other_host_login: other_host_login,
    MessageType.friend_online: friend_online,
    MessageType.room_mem_online: room_mem_online,
}

def handler(sock, itype, parameters):
    event_hander_map[itype](sock, parameters)