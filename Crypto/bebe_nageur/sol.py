charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_-!"
n = len(charset)

def f(a,b,n,x):
	return (a*x+b)%n

def encrypt(message,a,b,n):
	encrypted = ""
	for char in message:
		x = charset.index(char)
		x = f(a,b,n,x)
		encrypted += charset[x]

	return encrypted

def brute():
        # We know flag starts with "404CTF"
        # So we can bruteforce (a, b), considering the limited searchspace
        for a in range(2, n):
                for b in range(2, n):
                        c = encrypt("404CTF", a, b, n)
                        if c == enc[:6]:
                                print(f"{a=}")
                                print(f"{b=}")
                                return a, b
                        
enc = "-4-c57T5fUq9UdO0lOqiMqS4Hy0lqM4ekq-0vqwiNoqzUq5O9tyYoUq2_"
a, b = brute()

# Encrypt each char and build a mapping
M = dict()
for c in charset:
        M[encrypt(c, a, b, n)] = c

# Decrypt
flag = ''.join([M[c] for c in enc])
print(flag)

# 404CTF{Th3_r3vEnGE_1S_c0minG_S0oN_4nD_w1Ll_b3_TErRiBl3_!}
