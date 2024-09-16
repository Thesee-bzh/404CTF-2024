# Revers(ibl)e Engineering [1/2]

## Challenge
Après une année éprouvante marquée par les compétitions, vous décidez de rentrer dans votre village natal. C'est avec beaucoup d'émotion que vous apercevez le dojo de votre enfance et décidez de vous y rendre. Votre ancienne sensei vous y attend, le sourire aux lèvres.

"La clairvoyance est l'arme la plus redoutable du combattant. Anticiper chaque mouvement avant qu'il ne soit lancé, voilà la véritable maîtrise du combat. Relève mon défi et prouve ta valeur."

Récupérer une archive zip avec netcat contenant un crackme et un token, renvoyer le token avec la solution du crackme à un deuxième serveur, recevoir un flag... Facile. Petit détail : vous avez vingt secondes pour faire tout ça, et le binaire change à chaque essai.

> Connexion :
> - nc challenges.404ctf.fr 31998 > chall.zip
> - nc challenges.404ctf.fr 31999

## Analysis
Here's the main function decompiled by  `Ghidra`:

```c
undefined8 FUN_00101169(int param_1,long param_2)

{
  int iVar1;
  undefined8 uVar2;
  size_t sVar3;
  void *__s1;
  undefined8 local_28;
  undefined8 local_20;
  int local_c;

  if (param_1 < 2) {
    puts("J\'ai besoin d\'un argument!");
    uVar2 = 1;
  }
  else {
    sVar3 = strlen(*(char **)(param_2 + 8));
    local_c = (int)sVar3;
    if (local_c == 0x10) {
      local_28 = 0xa9dab58698ccb89d;
      local_20 = 0xbbd949da83d394c9;
      __s1 = (void *)FUN_0010123f(*(undefined8 *)(param_2 + 8));
      iVar1 = memcmp(__s1,&local_28,0x10);
      if (iVar1 == 0) {
        puts("GG!");
        uVar2 = 0;
      }
      else {
        puts("Dommage... Essaie encore!");
        uVar2 = 1;
      }
    }
    else {
      puts(&DAT_00102028);
      uVar2 = 1;
    }
  }
  return uVar2;
}
```

We see that the input parameter (`param_2 + 8`) is passed through some function (`FUN_0010123f`), which output is then compared (`memcmp`) to some 16bytes long static data (the 8 bytes stored in var `local_28`, followed by the 8 bytes stored in var `local_20`), which is an `hard-coded hash`:

```c
      local_28 = 0xa9dab58698ccb89d;
      local_20 = 0xbbd949da83d394c9;
      __s1 = (void *)FUN_0010123f(*(undefined8 *)(param_2 + 8));
      iVar1 = memcmp(__s1,&local_28,0x10);
```

The function `FUN_0010123f` is some sort of hash function. Note that each byte of the input is encrypted independantly of each other:

```c
void * FUN_0010123f(long param_1)

{
  byte bVar1;
  byte bVar2;
  void *pvVar3;
  int local_c;

  pvVar3 = malloc(0x10);
  for (local_c = 0; local_c < 0x10; local_c = local_c + 1) {
    bVar1 = *(byte *)(param_1 + local_c);
    bVar1 = bVar1 ^ (byte)((bVar1 >> 2 & 1) << 4) ^ (bVar1 >> 5) * '\x02' & 2;
    bVar1 = bVar1 ^ (byte)(((uint)bVar1 & (int)(uint)bVar1 >> 3 & 1U) << 7);
    bVar1 = bVar1 ^ (bVar1 >> 7 & (byte)((int)(uint)bVar1 >> 2) & 1) * '\x02';
    bVar1 = bVar1 ^ ((char)bVar1 >> 7) * -2 & 2U;
    bVar1 = bVar1 ^ (byte)((int)(uint)bVar1 >> 5) & 1 & (byte)((int)(uint)bVar1 >> 1) ^ 0x40;
    bVar2 = bVar1 ^ bVar1 >> 1 & 1;
    bVar1 = bVar2 ^ (byte)((int)(uint)bVar2 >> 5) & 1 & (byte)((int)(uint)bVar2 >> 2) ^
            (byte)((bVar1 >> 5 & 1) << 4);
    bVar1 = bVar1 ^ (byte)((bVar1 & 1) << 2);
    bVar1 = bVar1 ^ (byte)((int)(uint)bVar1 >> 1) & 1 & (byte)((int)(uint)bVar1 >> 6) ^ 0x21;
    bVar1 = bVar1 ^ bVar1 >> 5 & 1 ^ 0x80;
    bVar1 = bVar1 ^ (byte)(((int)(uint)bVar1 >> 2 & (int)(uint)bVar1 >> 1 & 1U) << 3) ^
            (bVar1 >> 7) << 3;
    *(byte *)((long)local_c + (long)pvVar3) =
         bVar1 ^ (byte)(((int)(uint)bVar1 >> 3 & (int)(uint)bVar1 >> 4 & 1U) << 2) ^ 5;
  }
  return pvVar3;
}
```

After fetching a new `crackme` sample and throwing it at `Ghidra` as well, the only differences are as follow:
- the hard-coded hash
- the hashing function (which still encrypts the input bytes independantly of each other)

## Using GDB
With `GDB` (and I use `GEF` as an extension), we can easily get the output of the `hashing function` for whatever input parameter by breaking at the `memcmp` function call:

```
gef➤  b *0x55555555520a
gef➤  r 1000000000000001
```

The output of the hashing function is passed as first argument of `memcmp`, hence at address `0x00005555555592a0`:

```
memcmp@plt (
   $rdi = 0x00005555555592a0 → 0xcfcfcfcfcfcfcfc2,
   $rsi = 0x00007fffffffdc80 → 0xa9dab58698ccb89d,
   $rdx = 0x0000000000000010,
   $rcx = 0x00005555555592a0 → 0xcfcfcfcfcfcfcfc2
)
```

So we can dump 16bytes from that address and get the hash for that specific input:
```
gef➤  x/4x 0x00005555555592a0
0x5555555592a0: 0xe6e6e6ed      0xe6e6e6e6      0xe6e6e6e6      0xede6e6e6
```

Since the input bytes are encrypted independantly of each other, we can generate the ouput for each possible byte. We'll `automate GDB` to do that.

## Automate GDB
Here is the set of `GDB commands` we'll automate from Python. In order to get the outputs from `GDB` (and only those we're interested in), we'll enable `GDB logging` to default file `gdb.txt` using `set logging enabled on` and disable it using `set logging enabled off`. Since we can only pass arguments consisting of 16 bytes, we make multiple rounds:

```python
cmd = [
    'b *0x55555555520a',       # Break at memcmp()

    'r 0123456789abcdef',      # Round #1
    'set logging enabled on',  # Log output to default file gdb.txt
    'x/4x $rsp+0x10',          # Get hard-coded hash
    'x/4x 0x00005555555592a0', # Get output of hash function
    'set logging enabled off', # Disable logging

    'r ghijklmnopqrstuv',      # Round #2
    'set logging enabled on',
    'x/4x 0x00005555555592a0',
    'set logging enabled off',

    'r wxyzABCDEFGHIJKL',      # Round #3
    'set logging enabled on',
    'x/4x 0x00005555555592a0',
    'set logging enabled off',

    'r MNOPQRSTUVWXYZ!_',     # Round #4
    'set logging enabled on',
    'x/4x 0x00005555555592a0',
    'set logging enabled off',

    #'r "#$%&\'()*+,-./:;<"',   # Round #5
    #'set logging enabled on',
    #'x/4x 0x00005555555592a0',
    #'set logging enabled off',

    #'r "=>?@[\\]^_`{|}~ "',    # Round #6
    #'set logging enabled on',
    #'x/4x 0x00005555555592a0',
    #'set logging enabled off'

    'quit',                    # Gracefully quit GDB
    'y'
    ]
```

Automating `GDB` is so easy with `Pwntools`:
```python
    p = process('./crackme.bin')
    # Attach the debugger
    gdb.attach(p, cmds)
    sleep(5)
```

And here we go, we get the outputs we want in default file `gdb.txt`:
```console
$ cat gdb.txt
0x7fffffffdc70: 0x98ccb89d      0xa9dab586      0x83d394c9      0xbbd949da
0x5555555592a0: 0xc9ccc2cf      0xdcd9d3da      0x989349c7      0x8d828f9d
0x5555555592a0: 0x941d9688      0x85028713      0x8c838e08      0x99929b89
0x5555555592a0: 0x8409869c      0xbdafa2a8      0xa5b3bab8      0xb128aa2f
0x5555555592a0: 0xb933b638      0xa9bbb2bc      0xb5a3aeac      0x23d2be3b
```

## Recover the password
The rest is just parsing the data from file `gdb.txt`, to recover the `hard-coded hash` (var `hash_`) and build a `Mapping table` (var `M`) of each `printable char`, giving its encrypted output (actually the reverse):
```python
	alph = [ printable[i:i + 16] for i in range(0, len(printable), 16) ]

	i = 0
    with open(gdbfile, "r") as f:
        for line in f:
            # 0x5555555592a0: 0xe6e6e6ed      0xe6e6e6e6      0xe6e6e6e6      0xb4e6e6e6
            l = line.split()[1:]
            out = b''.join([ unhexlify(i[2:])[::-1] for i in l ])
            # b'\xed\xe6\xe6\xe6\xe6\xe6\xe6\xe6\xe6\xe6\xe6\xe6\xe6\xe6\xe6\xb4'
            assert len(out) == 16
            if i == 0:
                hash_ = out
            else:
                arg = alph[i-1].encode()
                assert len(arg) == len(out)
                # Build mapping table
                #print("[x] ", l, arg, out)
                for j in range(len(arg)):
                    M[out[j]] = arg[j]
            i += 1
```

Finally, the `Mapping table` allows to recover the input password corresponding to the `hard-coded hash`:
```python
password = ''.join([ chr(M[x]) for x in hash_ ])
print(password)
```

Here we see it in action (and the verification):
```console
$ python3 sol.py
[+] Starting local process './crackme.bin': pid 7901
[*] running in new terminal: ['/usr/bin/gdb', '-q', './crackme.bin', '7901', '-x', '/tmp/pwnfmdq5pe8.gdb']
[-] Waiting for debugger: debugger exited! (maybe check /proc/sys/kernel/yama/ptrace_scope)
cE2bxX4T3j5q496S
[*] Process './crackme.bin' stopped with exit code 1 (pid 7901)
$
$ ./crackme.bin cE2bxX4T3j5q496S
GG!
```

Now we can automatically crack the `crackme`. Remaining thing to do is to automate the fetching of a `new crackme`, as well as the sending of the solution. Using `Pwntools`, of course.

## Automate the full process of downloading, cracking, uploading the solution
The `Download` is as follow, consisting in removing any remainder of crackme files, fetching another sample, writing it to a file, unzipping that file, making the extracted binary `crackme.bin` executable and reading the token from the extracted file `token.txt`:
```python
def download():
    os.system("rm ./crackme.bin ./token.txt ./chall.zip")

    c1 = remote("challenges.404ctf.fr", 31998)
    challz = b''
    while True:
        try:
            challz += c1.recv()
            sleep(1)
        except:
            break

    c1.close()
    with open("./chall.zip", "wb") as f:
        f.write(challz)

    os.system("unzip ./chall.zip")
    os.system("chmod +x ./crackme.bin")

    with open("./token.txt", "r") as f:
        token = f.read()

    print(token)
    return token
```

The `Upload` is as follow: we send the `token value` when asked for, then the `password` when the solution is asked for:
```python
def upload(token, password):
    c2 = remote("challenges.404ctf.fr", 31999)
    c2.recvline()
    c2.sendline(token.encode())
    c2.recvline()
    c2.sendline(password.encode())
    c2.recvline()
```

Putting everything together gives us the flag !
```console
[-] Waiting for debugger: debugger exited! (maybe check /proc/sys/kernel/yama/ptrace_scope)
cE2bxX4T3j5q496S
[+] Opening connection to challenges.404ctf.fr on port 31999: Done
[DEBUG] Received 0xa bytes:
    b'Token ? \r\n'
[DEBUG] Sent 0x21 bytes:
	b'4f2ef85f72a604a10651ff71f705530b\n'
[DEBUG] Received 0x17 bytes:
    b'Alors, la solution ? \r\n'
[DEBUG] Sent 0x11 bytes:
	b'cE2bxX4T3j5q496S\n'
[DEBUG] Received 0x41 bytes:
    b'GG. Voila ton flag!\r\n'
    b'404CTF{e9d749db81e9f8caf745a5547da13579}\r\n'
    b'\r\n'
[*] Closed connection to challenges.404ctf.fr port 31999
[*] Process './crackme.bin' stopped with exit code 1 (pid 47790)
```

## Python code
Complete solution in [sol.py](./sol.py)

## Flag
> 404CTF{e9d749db81e9f8caf745a5547da13579}
