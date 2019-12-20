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
    # 通知群成员自己上线
    for room in room_list:
        mems_id = database.get_room_members_id(room['ID'])
        for mem_id in mems_id:
            if mem_id in database.user_id_to_host and mem_id != user['ID']:
                iheader = serial_header_pack(MessageType.room_mem_online, [room['ID'], user['ID']])
                database.user_id_to_host[mem_id].conn.send(iheader)

    friend_list = database.get_friends(user['ID'])
    print(friend_list)
    # 通知好友自己上线
    for friend in friend_list:
        if friend['ID'] in database.user_id_to_host:
            iheader = serial_header_pack(MessageType.friend_online, [user['ID']])
            database.user_id_to_host[friend['ID']].conn.send(iheader)

    sorted(friend_list, key=lambda x: x['Nickname'])
    print('friend_list:', friend_list)
    related['Friend'] = friend_list
    related['Message'] = database.get_chat_history(user['ID'])
    data = serial_data_pack([related])
    tmp.append(len(data))
    header = serial_header_pack(MessageType.login_successful, tmp)
    sock.conn.send(header + data)

    # 发送好友请求
    # TODO: serial_header_pack have to deal with [[]]
    friend_list = database.get_pending_friend_request(user['ID'])
    for friend in friend_list:
        # if friend:
        iheader = serial_header_pack(MessageType.resolve_friend_request, [friend])
        sock.conn.send(iheader)
        
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
    database.user_id_to_host[c.lastrowid] = sock
    header = serial_header_pack(MessageType.register_successful, [c.lastrowid, parameters['Username'], parameters['Nickname']])
    sock.conn.send(header)

def add_friend(sock, parameters):
    print('in add_friend')
    print(parameters)
    receiver = parameters['Receiver']
    sender = parameters['Sender']
    # parameters = username
    c = database.get_cursor()
    r = c.execute('select * from Friends where Request_User_ID=? and Receive_User_ID=? and Accepted=0', [sender['ID'], receiver['ID']]).fetchall()
    if len(r) > 0:
        c.execute('update Friends set Resolved=0 where Request_User_ID=? and Receive_User_ID=?', [sender['ID'], receiver['ID']])
    else:
        c.execute('insert into Friends (Request_User_ID,Receive_User_ID,Accepted,Resolved) values (?,?,0,0)', [sender['ID'], receiver['ID']])
    if receiver['ID'] in database.user_id_to_host:
        header = serial_header_pack(MessageType.resolve_friend_request, [sender])
        database.user_id_to_host[receiver['ID']].conn.send(header)

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

def add_friend_successful_server(sock, parameters):
    print('in add_friend_successful_server')
    print(parameters)
    receiver = parameters['Receiver']
    sender = parameters['Sender']
    if sender['ID'] in database.user_id_to_host:
        header = serial_header_pack(MessageType.add_friend_successful, [receiver])
        database.user_id_to_host[sender['ID']].conn.send(header)

event_hander_map = {
    MessageType.login: login,
    MessageType.register: register,
    MessageType.add_friend: add_friend,
    MessageType.send_message: send_message,
    MessageType.join_room: join_room,
    MessageType.create_room: create_room,
    MessageType.query_room_users: query_room_users,
    MessageType.query_friend: query_friend,
    MessageType.other_host_login: other_host_login,
    MessageType.friend_online: friend_online,
    MessageType.room_mem_online: room_mem_online,
    MessageType.add_friend_successful_server: add_friend_successful_server,
}

def handler(sock, itype, parameters):
    event_hander_map[itype](sock, parameters)