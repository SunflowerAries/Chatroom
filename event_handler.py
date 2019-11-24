from message import *

def login(sock, parameters):
    print('in login')

def register(sock, parameters):
    print('in register')

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
}

def handler(sock, itype, parameters):
    print('in handler')
    event_hander_map[itype](sock, parameters)