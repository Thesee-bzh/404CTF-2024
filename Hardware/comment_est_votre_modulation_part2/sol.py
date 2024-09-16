import numpy as np
from more_itertools import sliced

def QAM16(symbol):
    return -3+2*(symbol>>2)+1j*(3-2*(symbol&0b11))

qam16_mapping = dict()
for i in range(16):
    b = str(bin(i)[2:].rjust(4, '0'))
    s = QAM16(i)
    qam16_mapping[s] = b
#print(qam16_mapping)
# {(-3+3j): '0000', (-3+1j): '0001', (-3-1j): '0010', (-3-3j): '0011', (-1+3j): '0100', (-1+1j): '0101', (-1-1j): '0110', (-1-3j): '0111', (1+3j): '1000', (1+1j): '1001', (1-1j): '1010', (1-3j): '1011', (3+3j): '1100', (3+1j): '1101', (3-1j): '1110', (3-3j): '1111'}

def decode_ofdm(samples, nb_samp, n_sc):
    # Demodulate OFDM
    demod = np.fft.fft(samples)
    # Return as many symbols as subcarriers
    symbols = [ round(x.real / nb_samp) + round(x.imag / nb_samp) * 1j for x in demod[:n_sc] ]
    return symbols

# Load signal from file (samples as float32)
signal = np.fromfile("flag.iq", dtype = np.complex64)

# Group by 350 samples
samples = list(sliced(signal, 350))

l = []
for s in range(len(samples)):
    samp = samples[s]
    symbols = decode_ofdm(samp, 350, 8)
    for i in range(0, len(symbols), 2):
        # Demap bytes (4MSB and 4LSB) using QAM16 symbol mapping
        msb4 = qam16_mapping[symbols[i]]
        lsb4 = qam16_mapping[symbols[i+1]]
        v = int(msb4 + lsb4, 2)
        l.append(v)

# Build the byte stream
b = b''.join([int.to_bytes(x, length=1, byteorder='big') for x in l])

# Write to file
with open('flag', 'wb') as f:
    f.write(b)
