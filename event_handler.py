import socket, time
from message import *
from pack import *
import database

callback_func = []

def add_listener(func):
    callback_func.append(func)

def login(sock, parameters):
    print('in login')
    c = database.get_cursor()
    fields = ['ID', 'Username', 'Nickname', 'Password']
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
    data = serial_data_pack([related])
    print(data)
    tmp.append(len(data))
    header = serial_header_pack(MessageType.login_successful, tmp)
    sock.conn.send(header + data)

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
    header = serial_header_pack(MessageType.register_successful, [c.lastrowid, parameters['Username'], parameters['Nickname']])
    sock.conn.send(header)

def add_friend(sock, parameters):
    print('in add_friend')
    user_id = sc_to_user_id[sc]
    # parameters = username
    c = database.get_cursor()
    username = parameters.strip().lower()
    r = c.execute('SELECT id from users where username=?', [username]).fetchall()
    if len(r) == 0:
        sc.send(MessageType.add_friend_result, [False, '用户名不存在'])
        return
    uid = r[0][0]
    if uid == user_id:
        sc.send(MessageType.add_friend_result, [False, '不能加自己为好友'])
        return
    c = database.get_cursor()
    r = c.execute('SELECT 1 from friends where from_user_id=? and to_user_id=?', [user_id, uid]).fetchall()
    if len(r) != 0:
        sc.send(MessageType.add_friend_result, [False, '已经是好友/已经发送过好友请求'])
        return
    c = database.get_cursor()
    c.execute('insert into friends (from_user_id,to_user_id,accepted) values (?,?,0)', [user_id, uid]).fetchall()
    sc.send(MessageType.add_friend_result, [True, ''])
    if uid in user_id_to_sc:
        user_id_to_sc[uid].send(MessageType.incoming_friend_request, database.get_user(user_id))

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

def query_friend(sock, parameters):
    c = database.get_cursor()
    print('%' + parameters['Name'] + '%')
    fields = ['ID', 'Username', 'Nickname']
    result = c.execute('SELECT ' + ','.join(fields) + ' from Users where Username like ? or Nickname like ?', ('%' + parameters['Name'] + '%', '%' + parameters['Name'] + '%'))
    rows = result.fetchall()
    print(rows)
    friend = []
    if len(rows) > 0:
        for i in range(len(rows)):
            tmp = {}
            tmp['ID'] = rows[i][0]
            tmp['Username'] = rows[i][1]
            tmp['Nickname'] = rows[i][2]
            print(tmp)
            friend.append(tmp)
        data = serial_data_pack(friend)
        header = serial_header_pack(MessageType.friend_found)
        sock.conn.send(header + data)
        return
    else:
        header = serial_header_pack(MessageType.friend_not_found)
        sock.conn.send(header)

event_hander_map = {
    MessageType.login: login,
    MessageType.register: register,
    MessageType.add_friend: add_friend,
    MessageType.resolve_friend_request: resolve_friend_request,
    MessageType.send_message: send_message,
    MessageType.join_room: join_room,
    MessageType.create_room: create_room,
    MessageType.query_room_users: query_room_users,
    MessageType.query_friend: query_friend,
    MessageType.other_host_login: other_host_login,
    MessageType.friend_online: friend_online,
    MessageType.room_mem_online: room_mem_online,
}

def handler(sock, itype, parameters):
    event_hander_map[itype](sock, parameters)