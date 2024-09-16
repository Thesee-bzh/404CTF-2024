import numpy as np

def read_channel(channel):
    with open("channel_"+str(channel),"r") as f:
	    data = f.read()
    return data

def save_flag(data):
    with open("flag.png","wb") as f:
        f.write(data)
    print("[+] Saved flag.png")

def receive():
    # Read transmitted data from different channels
    ch1 = read_channel(1)
    ch2 = read_channel(2)
    ch3 = read_channel(3)
    ch4 = read_channel(4)
    ch5 = read_channel(5)
    ch6 = read_channel(6)
    ch7 = read_channel(7)
    ch_crc = read_channel(8)

    # Fix noisy channel #4 using CRCs sent on channel #8
    l = len(ch1)
    ch4_ = list(ch4)
    for i in range(l):
        crc = (int(ch1[i]) + int(ch2[i]) + int(ch3[i]) + int(ch4[i]) + int(ch5[i]) + int(ch6[i]) + int(ch7[i])) % 2
        if crc != int(ch_crc[i]):
            # Bad CRC => bit transmitted on channel #4 is wrong
            ch4_[i] = str((int(ch4_[i]) + 1) % 2)
    ch4 = ''.join(ch4_)

    # Now Rebuid the data
    data = [0] * l * 7
    for i in range(l):
        data[7*i]     = ch1[i]
        data[7*i + 1] = ch2[i]
        data[7*i + 2] = ch3[i]
        data[7*i + 3] = ch4[i]
        data[7*i + 4] = ch5[i]
        data[7*i + 5] = ch6[i]
        data[7*i + 6] = ch7[i]

    # Get bytes out of a list of '0' and '1'
    # Probably a better way to do that...
    s = ''.join([str(x) for x in data])
    out = bytes(int(s[i : i + 8], 2) for i in range(0, len(s), 8))
    return out

flag = receive()
save_flag(flag)

# 404CTF{5feef3c530abba7ae2242487b25b6f6b}
