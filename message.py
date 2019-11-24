import enum
class MessageType(enum.IntEnum):
    login = 1
    register = 2
    add_friend = 3
    resolve_friend_request = 4
    send_message = 5
    join_room = 6
    create_room = 7
    query_room_users = 8
    
def convert(parameters):
    header = {}
    header['Type'] = parameters[0]
    header['Date'] = parameters[1].decode()
    header['Length'] = parameters[2]
    print(header)
    return header