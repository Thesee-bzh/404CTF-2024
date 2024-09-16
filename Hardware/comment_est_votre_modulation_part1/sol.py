import numpy as np
from more_itertools import sliced

# Load signal from file (samples as float32)
signal = np.fromfile("flag.raw", dtype = np.float32)

# Group by 350 samples
symbols = list(sliced(signal, 350))

# Valence is 256 means 256 possible states
# Rescale to fit that range (0..255)
v = 256
l = [min(v-1, int(v*max(symb))) for symb in symbols]

# Build the byte stream
b = b''.join([int.to_bytes(x, length=1, byteorder='big') for x in l])

# Write to file
with open('flag', 'wb') as f:
    f.write(b)
