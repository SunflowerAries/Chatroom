import struct
head = struct.pack('!I', 100)
print(head)
head += struct.pack('4s', 'abcd')
print(head)
print(struct.unpack('!I4s', head))
abc = 'abc'.encode()
print(len(abc))
a = bytes(1)
print(a, type(a), len(a), int(a))
x = b''
print(len(x))