from pwn import *
from string import printable
from binascii import unhexlify
from time import sleep
import os
import struct

alph = string.printable
gdbfile = "./gdb.txt"

alph = [ printable[i:i + 16] for i in range(0, len(printable), 16) ]
# ['0123456789abcdef', 'ghijklmnopqrstuv', 'wxyzABCDEFGHIJKL', 'MNOPQRSTUVWXYZ!"', "#$%&'()*+,-./:;<", '=>?@[\\]^_`{|}~ \t', '\n\r\x0b\x0c']

cmd = [
    'b *0x55555555520a',       # Break at memcmp()

    'r 0123456789abcdef',      # Round #1
    'set logging enabled on',  # Log output to default file gdb.txt
    'x/4x $rsp+0x10',          # Get hard-coded hash
    'x/4x 0x00005555555592a0', # Get output of hash function
    'set logging enabled off', # Disable logging

    'r ghijklmnopqrstuv',      # Round #2
    'set logging enabled on',
    'x/4x 0x00005555555592a0',
    'set logging enabled off',

    'r wxyzABCDEFGHIJKL',      # Round #3
    'set logging enabled on',
    'x/4x 0x00005555555592a0',
    'set logging enabled off',

    'r MNOPQRSTUVWXYZ!_',     # Round #4
    'set logging enabled on',
    'x/4x 0x00005555555592a0',
    'set logging enabled off',

    #'r "#$%&\'()*+,-./:;<"',   # Round #5
    #'set logging enabled on',
    #'x/4x 0x00005555555592a0',
    #'set logging enabled off',

    #'r "=>?@[\\]^_`{|}~ "',    # Round #6
    #'set logging enabled on',
    #'x/4x 0x00005555555592a0',
    #'set logging enabled off'

    'quit',                    # Gracefully quit GDB
    'y'
    ]

cmds = "\n".join(cmd)
M = dict()

def rungdb():
    os.system("rm ./gdb.txt")

    p = process('./crackme.bin')
    # Attach the debugger
    gdb.attach(p, cmds)
    sleep(5)

    i = 0
    with open(gdbfile, "r") as f:
        for line in f:
            # 0x5555555592a0: 0xe6e6e6ed      0xe6e6e6e6      0xe6e6e6e6      0xb4e6e6e6
            l = line.split()[1:]
            out = b''.join([ unhexlify(i[2:])[::-1] for i in l ])
            # b'\xed\xe6\xe6\xe6\xe6\xe6\xe6\xe6\xe6\xe6\xe6\xe6\xe6\xe6\xe6\xb4'
            assert len(out) == 16
            if i == 0:
                hash_ = out
            else:
                arg = alph[i-1].encode()
                assert len(arg) == len(out)
                # Build mapping table
                #print("[x] ", l, arg, out)
                for j in range(len(arg)):
                    M[out[j]] = arg[j]
            i += 1
    return hash_

def download():
    os.system("rm ./crackme.bin ./token.txt ./chall.zip")

    c1 = remote("challenges.404ctf.fr", 31998)
    challz = b''
    while True:
        try:
            challz += c1.recv()
            sleep(1)
        except:
            break

    c1.close()
    with open("./chall.zip", "wb") as f:
        f.write(challz)

    os.system("unzip ./chall.zip")
    os.system("chmod +x ./crackme.bin")

    with open("./token.txt", "r") as f:
        token = f.read()

    print(token)
    return token

def upload(token, password):
    c2 = remote("challenges.404ctf.fr", 31999)
    c2.recvline()
    c2.sendline(token.encode())
    c2.recvline()
    c2.sendline(password.encode())
    c2.recvline()

token = download()
hash_ = rungdb()
password = ''.join([ chr(M[x]) for x in hash_ ])
print(password)
upload(token, password)
