import crypt, hashlib

def get_shared_secret(secret):
    return hashlib.sha256(long_to_bytes())

def create_secure_channel(socket):
    conn, addr = socket.accept()
    data = conn.recv(1024)
    secret = int.from_bytes(data, byteorder='big')

    conn.send(long_to_bytes())
    shared_secret = crypt.
    return 