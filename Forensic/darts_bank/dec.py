import sys
from base64 import b64decode
from byte_array import get_bytearray

L = get_bytearray()
size = len(L)

def xor(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

filename = sys.argv[1]
with open(filename, 'rb') as f:
    data = f.read()

data = b64decode(data)

dec = b''
for i in range(len(data)):
    #print(i, L[i % size], int.to_bytes(L[i % size], 1, 'big'), data[i])
    dec += xor(int.to_bytes(data[i], 1, 'big'), int.to_bytes(L[i % size], 1, 'big'))


filename += '.dec'
with open(filename, 'wb') as f:
    f.write(dec)
