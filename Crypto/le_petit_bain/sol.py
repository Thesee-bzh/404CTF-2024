enc = "C_ef8K8rT83JC8I0fOPiN6P!liE03W2NXFh1viJCROAqXb6o"

charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_-!"
n = len(charset)

def f(a,b,n,x):
	return (a*x+b)%n

def round_no_permute(message,a,b,n):
	encrypted = ""
	for i in range(len(message)):
		x = charset.index(message[i])
		x = f(a,b,n,x)
		encrypted += charset[x]
	return encrypted

def brute(i):
        m = "404CTF{tHe_c"
        # We know flag starts with "404CTF"
        # So we can bruteforce (a, b), considering the limited searchspace
        for a in range(2, n):
                for b in range(2, n):
                        c1 = round_no_permute(m[i], a, b, n)
                        c2 = round_no_permute(m[6+i], a, b, n)
                        if c1 == enc[i] and c2 == enc[6+i]:
                                return a, b

# Bruteforce (a, b) for each char in the beginning of FLAG
A = list(); B = list()
for i in range(6):
        a, b = brute(i)
        A.append(a); B.append(b)
print(f"{A=}")
print(f"{B=}")

# Encrypt each char and build a mapping for each position
MM = list()
for i in range(6):
        M = dict()
        for c in charset:
                M[round_no_permute(c, A[i], B[i], n)] = c
        MM.append(M)

# Decrypt
flag = ''
for i in range(len(enc)):
        M = MM[i%6]
        flag += M[enc[i]]
print(flag)

# 404CTF{tHe_c4fF31ne_MakE5_m3_StR0nG3r_th4n_y0u!}
