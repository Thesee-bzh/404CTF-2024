from modified_random import Generator
from Cryptodome.Util.number import long_to_bytes

def xor(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

def get_blocks(data,block_size):
    return [data[i:i+block_size] for i in range(0,len(data),block_size)]

def pad(data,block_size):
    return data+b'\x00'*(block_size-len(data)%block_size)

def decrypt(data,gen,block_size):
    padded_data = pad(data,block_size)
    data_blocks = get_blocks(padded_data,block_size)
    generator = Generator(gen)
    decrypted = b''
    for block in data_blocks:
        rd = generator.get_random_bytes(block_size)
        xored = xor(block,rd)
        decrypted+= xored
    return decrypted

BLOCK_SIZE = 4
flag = None

# Read partial plaintext
with open("flag.png.part",'rb') as f:
    flag_part = f.read()

# Read ciphertext
with open("flag.png.enc",'rb') as f:
    flag_enc = f.read()

# Recover the 2000 first generated numbers used for encryption
# Just XOR the first 2000 bytes from plaintext & ciphertext
gen = list(xor(flag_part[:2000], flag_enc[:2000]))

# After 2000 bytes, the generated numbers completely fill the Generator feed
# But we just recovered those first 2000 generated numbers, so there's no randomness anymore...
dec = decrypt(flag_enc[2000:], gen, BLOCK_SIZE)

# Just concatenate both parts and write to file system
flag = flag_part[:2000] + dec
with open("flag.png",'wb') as f:
    f.write(flag)
print("[+] Wrote flag.png")

# 404CTF{5294dbe4adf1fd96b34635abc07c6a5dba3be8bf}
