# Echauffement

## Challenge
Un bon échauffement permet non seulement d'éviter les blessures, mais aussi de conditionner son corps et son esprit au combat qui va suivre. Ce crackme devrait constituer un exercice adéquat.

## Inputs
- Binary: [echauffement.bin](./echauffement.bin)

## Solution
We open the binary in `Ghidra` to find out what input is expected:

```c
secret[] = {68, 5f, 66, 83, a4, 87, f0, d1, b6, c1, bc, c5, 5c, dd, be, bd, 56, c9, 54, c9, d4, a9, 50, cf, d0, a5, ce, 4b, c8, bd, 44, bd, aa, d9, 00, 00, 00, 00, 00, 00}

undefined4 secret_func_dont_look_here(long param_1)

{
  size_t len;
  undefined4 check;
  int i;
  
  len = strlen(secret_data);
  check = 0;
  for (i = 0; i < (int)len; i = i + 1) {
    if ((char)(*(char *)(param_1 + i) * '\x02' - (char)i) != secret_data[i]) {
      check = 1;
    }
  }
  return check;
}
```

Then we reverse it in python:
```python
secret = [0x68, 0x5f, 0x66, 0x83, 0xa4, 0x87, 0xf0, 0xd1, 0xb6, 0xc1, 0xbc, 0xc5, 0x5c, 0xdd, 0xbe, 0xbd, 0x56, 0xc9, 0x54, 0xc9, 0xd4, 0xa9, 0x50, 0xcf, 0xd0, 0xa5, 0xce, 0x4b, 0xc8, 0xbd, 0x44, 0xbd, 0xaa, 0xd9]

pwd = ''
for i in range(len(secret)):
    pwd += chr((secret[i] + i) // 2)
print(pwd)
```

We recover the flag and check it:
```console
$ python3 sol.py
404CTF{l_ech4uff3m3nt_3st_t3rm1ne}
$
$ ./echauffement.bin
Vous ne devinerez jamais le mot de passe secret ! Mais allez-y, essayez..
404CTF{l_ech4uff3m3nt_3st_t3rm1ne}
Wow, impressionnant ! Vous avez réussi !
```

## Flag
> 404CTF{l_ech4uff3m3nt_3st_t3rm1ne}
