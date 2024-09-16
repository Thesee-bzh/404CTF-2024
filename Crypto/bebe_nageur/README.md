# Bébé nageur (Introduction)

## Challenge
Vous ressortez de votre premier cours de natation et quelqu'un vous a laissé un petit mot dans votre casier. Vous suspectez votre rival que vous venez juste de battre à plate couture lors d'une course effrénée dans le bassin des bébés nageurs.
 
Déchiffrez ce message.

## Inputs
- Python script [challenge.py](./challenge.py)

## Analysis
Looking at the Python script, the flag is encoded as follow:
- for each character, it takes its index `i` in the given `charset`
- some permutation is applied on the index: `j = (a*i+b)%n` where `n=len(charset)` and `(a, b)` are kept secret
- then we take the  character at new index `j`

```python
from flag import FLAG
import random as rd

charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_-!"

def f(a,b,n,x):
	return (a*x+b)%n

def encrypt(message,a,b,n):
	encrypted = ""
	for char in message:
		x = charset.index(char)
		x = f(a,b,n,x)
		encrypted += charset[x]

	return encrypted

n = len(charset)
a = rd.randint(2,n-1)
b = rd.randint(1,n-1)

print(encrypt(FLAG,a,b,n))

# ENCRYPTED FLAG : -4-c57T5fUq9UdO0lOqiMqS4Hy0lqM4ekq-0vqwiNoqzUq5O9tyYoUq2_
```

We can simply bruteforce `(a, b)` considering the limited searchspace and knowing the flag starts with `404CTF`.

## Solution
Here's the bruteforce function, which returns the couple `(a, b)`:

```python
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
```

Here we go:
```console
$ python3 sol.py
a=19
b=6
404CTF{Th3_r3vEnGE_1S_c0minG_S0oN_4nD_w1Ll_b3_TErRiBl3_!}
```

## Python code
Complete solution in [sol.py](./sol.py)

## Flag
> 404CTF{Th3_r3vEnGE_1S_c0minG_S0oN_4nD_w1Ll_b3_TErRiBl3_!}
