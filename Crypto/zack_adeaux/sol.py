from sage.all import *
import math
import json
import zlib
import base64
import random
from more_itertools import sliced

def findgoodvect(m):
    for v in m:
        if v[-1] == 0:
            good = True
            for i in range(len(v) - 1):
                vi = 1 - (v[i] + (1 / 2))
                if vi != 1 and vi != 0:
                    good = False
                    break
        if good:
            return v
    return None

def decrypt(pub, enc, n):

    P = Matrix(ZZ, pub).transpose()
    I = Matrix.identity(ZZ, n)
    H = Matrix(QQ,[1/2 for _ in range(n)])
    E = Matrix(ZZ,[enc])

    # Build block matrix
    # Use the CJLOSS algorithm (small variant to the LO algo)
    # See https://eprint.iacr.org/2023/032.pdf for instance
    # |   I=I(n)  | N*P |
    # |-----------|-----|
    # | H=[1/2]*n | N*E |
    N = ceil(sqrt(n) / 2)
    M = block_matrix([[I, N*P], [H, N*E]])

    # Note:
    # With standard LO algo: v=(e1,e2,...,en,-1) gives short vector v'=vM=(e1,e2,...,en,0)
    # While for CJLOSS algo: v=(e1,e2,...,en,-1) gives short vector v'=vM=(e1-1/2,e2-1/2,...,en-1/2,0)

    # Reduce the matrix
    R = M.LLL()
    print('[*] matrix reduced')

    # Find good vector
    e = findgoodvect(R)

    # Recover message
    msg = ''
    for i in range(len(e) - 1):
        ei = 1 - (e[i] + (1 / 2)) # Because CJLOSS is used
        msg += str(int(ei))

    print('[*] binary:', msg)
    msg = '00' + msg[:-2] # hack to make it work, not sure why ??
    flag = ''.join([ chr(int(c, 2)) for c in list(sliced(msg, 8)) ])
    return flag

# Load example blob
with open('tmp', 'r') as f:
    data = f.read()

# Decode blob, recover public key and encrypted message
j = json.loads(zlib.decompress(base64.b64decode(data)))
pub, enc = j['public_key'], j['encrypted']
print('[*] enc', enc)

# Decrypt
flag = decrypt(pub, enc, len(pub))
print('[*] flag', flag)
