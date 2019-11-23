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
    header['Type'] = 
    header['Date'] = parameters
    header['Length'] = 
    header[]
    return header