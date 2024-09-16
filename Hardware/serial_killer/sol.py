from more_itertools import sliced

with open('chall.bin', 'rb') as f:
    data = f.read()

bits = ''
for x in data:
    bits += bin(x)[2:].rjust(8, '0')

# Split in frames or 10 bits
frames = list(sliced(bits, 10))

# Parse the frames of 10 bits
# extract the payload (and invert it for some reason)
msg = ''
for f in frames[:-1]:
    # start bit must be 0
    # end bit must be 1
    assert f[0] == '0'
    assert f[9] == '1'
    # drop the parity bit
    data = int('0b' + f[1:8][::-1], 2)
    msg += chr(data)
print(msg)
    
