import message
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
    event_hander_map[itype].run(sock, parameters)