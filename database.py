import sqlite3
conn = sqlite3.connect('database.db', isolation_level=None)

cursor = conn.cursor()
user_id = 1
fields = ['id', 'username', 'nickname']
row = cursor.execute('SELECT ' + ','.join(fields) + ' FROM users WHERE id=?', [user_id]).fetchall()
print(len(row))