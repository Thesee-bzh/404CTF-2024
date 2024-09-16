# Le soulevé de GND

## Challenge
Hooooo - Hiiiiissse......
Hooooo - Hiiiiissse......
Hooooo - Hiiiiissse......

Waouh ça fait du bien de soulever un peu de fonte ! Mais dites donc ! C'est que vous avez des sacrés bras vous ! J'ai une petite épreuve pour vous, c'est du soulevé de terre... mais la terre bouge avec vous ! Hehe... vous m'en direz des nouvelles !

> Format de flag : 404CTF{motdepasse}

## Inputs
- Python script: [chall.py](./chall.py)

## Analysis
We have a `Python script` using the `myhdl library` that models and simulates a digital circuit.

Essentially, we have:

```python
    xor_inst = xor(s, state, tc)
    gnd = GND(state, clk_sig)
```

With `GND` block yielding a new state as a linear function of the current state:

```python
A = 7
B = 1918273

@block
def GND(state, clk):
    """
    Le sol il bouge ?
    ça envoie un mauvais signal tout ça...
    """

    @always(clk.posedge)
    def core():
        state.next = A * state + B

    return core
```

So we just need to implement that same state generator and xor it with the provided data:

```python
A = 7
B = 1918273
N = 25

data = [78, 114, 87, 9, 245, 67, 252, 90, 90, 126, 120, 109, 133, 78, 206, 121, 52, 115, 123, 102, 164, 194, 170, 123, 5]

m = ''
state = 0
for d in data:
    x = state ^ d
    state = (A * state + B) % 256
    m += chr(x)
print(m)
```

And this gives us the flag !

```console
$ python3 sol.py
N3_perd3z_P45_v0tr3_t3rRe
```

## Python code
Complete solution in [sol.py](./sol.py)

## Flag
> 404CTF{N3_perd3z_P45_v0tr3_t3rRe}
