# Intronisation du CHAUSSURE

## Challenge
Montrez votre valeur

Le CHAUSSURE, cette fameuse entité pionnière dans le domaine du sport de combat a ouvert un tournoi pour tous les chat-diateurs qui souhaiteraient se mesurer au reste du monde. Les présélections commencent et un premier défi a été publié par le CHAUSSURE. Ce dernier semble très cryptique, à vous d'en déceler les secrets!

> Format de flag : 404CTF{mot-de-passe}

## Inputs
- Binary: [intronisation](./intronisation)

## Solution
Opening the binary in `Ghidra`:

```c
void processEntry entry(void)

{
  size_t sVar1;
  char local_28;
  char local_27;
  char local_26;
  char local_25;
  char local_24;
  char local_23;
  char local_22;
  char local_21;
  char local_20;
  char local_1f;
  char local_1e;
  char local_1d;
  char local_1c;
  
  syscall();
  syscall();
  sVar1 = _strlen(&local_28);
  if (((((sVar1 == 0xe) && (local_27 == 't')) && (local_21 == 'r')) &&
      ((((local_1e == '1' && (local_1d == 's')) &&
        ((local_23 == 'n' && ((local_24 == '1' && (local_26 == 'u')))))) && (local_28 == '5')))) &&
     ((((local_1f == 'n' && (local_1c == '3')) && (local_20 == '0')) &&
      ((local_25 == 'p' && (local_22 == 't')))))) {
    syscall();
  }
  else {
    syscall();
  }
  syscall();
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}
```

We can manually recover the expected input and check it:

```console
$ ./intronisation
Bienvenue, rétro-ingénieur en herbe!
Montre moi que tu es à la hauteur :
>>> 5tup1ntr0n1s3
Bravo !!!
```

## Flag
> 404CTF{5tup1ntr0n1s3}
