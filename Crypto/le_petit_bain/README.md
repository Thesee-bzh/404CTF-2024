# Le petit bain (Facile)

## Challenge
Malheureusement, votre revanche contre votre adversaire de toujours s'est soldée par une défaite. En toute bonne foi, vous suspectez de la triche. Vous décidez vivement de fouiller son casier et tombez sur un étrange mot. À vous de le déchiffrer.

> Note : ce challenge est la suite du challenge intitulé Bébé nageur

## Inputs
- Python script [challenge.py](./challenge.py)

## Analysis
Like in the previous challenge, some permutation is applied on the characters of the flag, but this time it is a little more complicated. The following process is reapeated 6 times:
- randomly choose secrets `(a, b)`
- apply the permutation `(a*i+b)%n` like in the previous challenge, but only for the characters at position `i%6` in the flag
- apply yet another permutation on the all string

```python
import random as rd
from flag import FLAG

assert FLAG[:12] == "404CTF{tHe_c"

charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_-!"
n = len(charset)

def f(a,b,n,x):
	return (a*x+b)%n

def permute(message):
	p = [4, 3, 0, 5, 1, 2, 10, 9, 6, 11, 7, 8, 16, 15, 12, 17, 13, 14, 22, 21, 18, 23, 19, 20, 28, 27, 24, 29, 25, 26, 34, 33, 30, 35, 31, 32, 40, 39, 36, 41, 37, 38, 46, 45, 42, 47, 43, 44]
	permuted = [ message[p[i]] for i in range(len(message))]
	return ''.join(permuted)

def round(message,A,B,n):
	encrypted = ""
	for i in range(len(message)):
		x = charset.index(message[i])
		a = A[i%6]
		b = B[i%6]
		x = f(a,b,n,x)
		encrypted += charset[x]
	return permute(encrypted)

def encrypt(message):
	encrypted = message
	for k in range(6):
		A = [ rd.randint(2,n-1) for i in range(6)]
		B = [ rd.randint(1,n-1) for i in range(6)]
		encrypted = round(encrypted,A,B,n)
	return encrypted

print(encrypt(FLAG))

# OUTPUT : C_ef8K8rT83JC8I0fOPiN6P!liE03W2NXFh1viJCROAqXb6o
```

Let's first see how that permutation operates by applying few iterations of it on a fake flag:
```python
>>> m = "404CTF{tHe_c01234567890123456789012345678901234}"
>>> print(m)
404CTF{tHe_c01234567890123456789012345678901234}
>>> for i in range(6):
...         m = permute(m)
...         print(m)
...
TC4F04_e{ctH430512096178652734218390874956430}12
0FT4C4tc_He{1542307108963764529320185986741}4230
C404FTeHt{c_3210549876105432761098327654983210}4
F4CT40c{e_Ht503421169087725643381209947865}03421
4TF04CH_ct{e24510380176946732502398168954724}103
404CTF{tHe_c01234567890123456789012345678901234}
```

Oh, It has a period of exactly 6, meaning that we recover the original string after 6 iterations.

But... the all encryption process is applied 6 times, meaning that this permutation is applied exactly 6 times, meaning that it does nothing overall and we can just ignore it !

We're left with bruteforcing `(a, b)` considering the limited search space and knowing that the flag starts with `404CTF`, just like in the first challenge. Except we need to bruteforce 6 sets of it, one for each of the `i%6` positions.

## Solution
Here's the code to brute force the set of parameters `(a, b)` for all indexes `i%6`:

```python
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
```

Here we go:
```console
$ python3 sol.py
A=[50, 40, 39, 34, 35, 37]
B=[42, 61, 31, 58, 26, 28]
404CTF{tHe_c4fF31ne_MakE5_m3_StR0nG3r_th4n_y0u!}
```

## Python code
Complete solution in [sol.py](./sol.py)

## Flag
> 404CTF{tHe_c4fF31ne_MakE5_m3_StR0nG3r_th4n_y0u!}
