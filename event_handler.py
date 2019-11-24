import socket, time
from message import *
import database

def login(sock, parameters):
    c = database.get_cursor()
    fields = ['ID', 'Username', 'Nickname']
    # print(','.join(fields), parameters['Username'])
    # print('SELECT ' + ','.join(fields) + ',Password' + ' from Users where Username=%s' % (parameters['Username']))
    result = c.execute('SELECT ' + ','.join(fields) + ',Password' + ' from Users where Username=?', (parameters['Username'], ))
    rows = result.fetchall()

    if len(rows) == 0:
        header = struct.pack('!I', MessageType.user_not_exist)
        date = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
        header += serial_pack([date, 0])
        sock.conn.send(header)
        return
    
    match = False
    cnt = 0
    for i in range(len(rows)):
        if rows[i][3] == parameters['Password']:
            match = True
            cnt = i
            user = dict(zip(fields, rows[i]))
            date = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
            break
    
    if not match:
        header = struct.pack('!I', MessageType.wrong_password)
        date = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
        header += serial_pack([date, 0])
        sock.conn.send(header)
        return
    
    if user['ID'] in database.user_id_to_host:
        old_host = database.user_id_to_host[user['ID']]
        header = struct.pack('!I', MessageType.other_host_login)
        date = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
        header += serial_pack([date, 0])
        old_host.conn.send(header)
        old_host.close()
        database.kickout_host(old_host)
    
    database.user_id_to_host[user['ID']] = sock
    header = struct.pack('!I', MessageType.login_successful)
    tmp = list(rows[cnt][0:3])
    tmp.append(date)
    tmp.append(0)
    header += serial_pack(tmp)
    # print(header)
    # print(sock.conn)
    sock.conn.send(header)

def login_successful(sock, parameters):
    print(parameters)

def register(sock, parameters):
    c = database.get_cursor()
    r = c.execute('SELECT * from Users where Username=?', [parameters['Username']])
    rows = r.fetchall()
    if len(rows) > 0:
        header = struct.pack('!I', MessageType.username_taken)
        date = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
        header += serial_pack([date, 0])
        sock.conn.send(header)
        return
    c.execute('INSERT into Users (Username,Password,Nickname) values (?,?,?)',
              [parameters['Username'], parameters['Password'], parameters['Nickname']])
    date = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
    header = struct.pack('!I', MessageType.register_successful)
    header += serial_pack([c.lastrowid, date, 0])
    # print(sock)
    sock.conn.send(header)

def register_successful(sock, parameters):
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
    MessageType.login_successful: login_successful,
    MessageType.register_successful: register_successful,
}

def handler(sock, itype, parameters):
    print('in handler')
    event_hander_map[itype](sock, parameters)