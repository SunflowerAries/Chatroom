import sqlite3
conn = sqlite3.connect('database.db', isolation_level=None, check_same_thread=False)

user_id_to_host = {}

def get_cursor():
    return conn.cursor()

def commit():
    return conn.commit()

def kickout_host(host):
    print("jo")

cursor = conn.cursor()
user_id = 1
fields = ['id', 'username', 'nickname']
row = cursor.execute('SELECT ' + ','.join(fields) + ' FROM users WHERE id=?', [user_id]).fetchall()
print(len(row))