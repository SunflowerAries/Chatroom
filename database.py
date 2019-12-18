import sqlite3
conn = sqlite3.connect('database.db', isolation_level=None, check_same_thread=False)

user_id_to_host = {}

def get_cursor():
    return conn.cursor()

def commit():
    return conn.commit()

def get_user(user_id):
    c = get_cursor()
    fields = ['ID', 'Username', 'Nickname']
    row = c.execute('SELECT ' + ','.join(fields) + ' from Users where ID=?', [user_id]).fetchall()
    if len(row) == 0:
        return
    else:
        user = dict(zip(fields, row[0]))
        user['online'] = user_id in user_id_to_host
        return user

def kickout_host(host):
    print("jo")

def get_pending_friend_request(user_id):
    c = get_cursor()
    rows = c.execute('SELECT Request_User_ID FROM Friends WHERE Receive_User_ID=? AND NOT Resolved', [user_id]).fetchall()
    return list(map(lambda x: get_user(x[0]), rows))

def get_friends(user_id):
    c = get_cursor()
    users = []
    rows = c.execute('SELECT Receive_User_ID FROM Friends WHERE Request_User_ID=? AND Accepted', [user_id]).fetchall()
    for row in rows:
        uid = row[0]
        users.append(get_user(uid))
    rows = c.execute('SELECT Request_User_ID FROM Friends WHERE Receive_User_ID=? AND Accepted', [user_id]).fetchall()
    for row in rows:
        uid = row[0]
        users.append(get_user(uid))
    return users

def get_user_room(user_id):
    c = get_cursor()
    rows = c.execute('SELECT Room_ID FROM Room_User WHERE User_ID=?', [user_id]).fetchall()
    return list(map(lambda x: get_room(x[0]), rows))

def get_room(room_id):
    c = get_cursor()
    fields = ['ID', 'Room_Name']
    row = c.execute('SELECT ' + ','.join(fields) + ' FROM Rooms WHERE ID=?', [room_id]).fetchall()
    if len(row) == 0:
        return
    else:
        room = dict(zip(fields, row[0]))
        return room

def add_to_room(user_id, room_id):
    c = get_cursor()
    c.execute('INSERT INTO Room_User (User_ID, Room_ID) VALUES (?,?) ',
                  [user_id, room_id])

def get_room_members_id(room_id):
    c = get_cursor()
    result = c.execute('SELECT User_ID FROM Room_User WHERE Room_ID=?', [room_id]).fetchall()
    return list(map(lambda x: x[0], result))

def get_room_members(room_id):
    # [id, nickname, online, username]
    c = get_cursor()
    result = c.execute('SELECT User_ID,Nickname,Username FROM Room_User LEFT JOIN Users ON Users.ID=User_ID WHERE Room_ID=?',
        [room_id]).fetchall()
    return list(map(lambda x: [x[0], x[1], x[0] in user_id_to_host, x[2]], result))

# TODO why only user_id?
def add_to_chat_history(user_id, target_id, target_type, data, sent):
    c = get_cursor()
    c.execute('INSERT INTO Chat_History (User_ID,Target_ID,Target_Type,Data,Sent) VALUES (?,?,?,?,?)',
              [user_id, target_id, target_type, data, sent])
    return c.lastrowid

# [[data:bytes,sent:int]]
# TODO sent means read?
def get_chat_history(user_id):
    c = get_cursor()
    result = c.execute('SELECT Data,Sent FROM Chat_History WHERE User_ID=?', [user_id]).fetchall()
    ret = list(map(lambda x: [x[0], x[1]], result))
    c.execute('UPDATE Chat_History SET Sent=1 WHERE User_ID=?', [user_id])
    return ret