# Zack Adeaux (Moyen)

## Challenge
Vous et votre ami Zack partez ensemble pour votre cours de natation habituel. Vers la moitié du trajet, votre ami décide de vous montrer sa toute nouvelle paire de lunettes de natation, cependant impossible de remettre la main dessus ! Vous décidez de l'aider mais vous vous rendez vite compte que son sac de piscine est un vrai bazar ! Étant un peu maniaque, vous décidez d'y mettre un peu d'ordre.

## Inputs
- Python script [challenge.py](./challenge.py)
- Target at `challenges.404ctf.fr:31777`

## Analysis
Looking at the Python script, we should recover from the target a `Public key` and an `encrypted flag`:

```python
def encode(data):
	data = json.dumps(data).encode("utf-8")
	data = zlib.compress(data)
	data = base64.b64encode(data)
	return data.decode("utf-8")

if __name__ == "__main__":
	n = getPrime(2048)
	A, B, a = genKeys(n,256)
	data = encode({"public_key" : B, "encrypted": encrypt(B,FLAG)})

	print("Zut ! J'ai renversé mon sac à dos et tout est tombé par terre, vous pourriez mettre un peu d'ordre dans tout ça ?")	
	print(data)
```

Let's first check that we indeed recover those:


```console
nc challenges.404ctf.fr 31777 > tmp
$ ^C
$ file tmp
tmp: ASCII text, with very long lines (65536), with no line terminators
$ base64 -d tmp > tmp.b64.dec
$ file tmp.b64.dec
tmp.b64.dec: zlib compressed data
$ zlib-flate -uncompress < tmp.b64.dec > tmp.zlib.dec
$ file tmp.zlib.dec
tmp.zlib.dec: JSON data
$ mv tmp.zlib.dec tmp.json
$ cat tmp.json
{"public_key": [4113016036797710504685757287646964175308506237622077896770716142514276872909941539612222317065629747808701753406703564115565273558564273409937986610707110663640509278104501831112607409263806716543422183884625355105127369745173653811829626300284929037767464914148924072258573482258860818263460688894451974560458012700631939509313960263526174553276096284689436488553041112461916941189532968751473942380207726472011605816724850323317731205403692816021904524927310825720853638532611047823651116902731721919459996862625996287444839166678578078936609543062485694169665893524758008107093740667681006165150949868951244717102, 17704295625041039183170331708665506302195910344723049440678939163399313005527573755137479387546989533689563122029372222575681198316007825921653320745269630102186105293561497703956406951035167526976730415200575265589812030404413084013531728698210051876897946115305892327681439270234063274767801014772897455849309312115540555431160978808873043810162303617523215605513430640284562322549074065944153983152376412452001250004109232751381758147766966903665553053230320055021848973295225704973866513764604977752926806359583222742666891388717749690169494919356899341159238931003290979067697023227174351938541746375690174170581, 3392923(..............................), 3628335666820777423301912700300106104806775788132267801327787134103663139231458404875571304553926054892436555299529866403376280356707655570452585663255947390771815907367157404798728823863279774322579937782219121346424893251671641277924752343741760419668730511056476639424493793542552373347672528810735738220034408732442800542372293793303242702672616840799650171924756948127580611990661253742206343350142568273463965634625694901743429647914984557944297266998464258623798612814878932784181871558420838644779351656993266262605812839826639907325824592440093591314886126602050421635270859636388275460025856529167781705616], "encrypted": 1554330031748566348256886076643487598070443339530824300578945212914551502156587322291836646817783519587101304061071357078807658454104181329600844867618029914887067771959744871680016128722028006589977874298129337441734329964835076299558655448645350532522708039380148485980834562974640975216845438653289214969168532481432885580226545239262817315108780941835540601328751858136643616315851488247604734510349510838816718788454389974297985613711849529400486878871428345746090699725504519585885380188682040398840983211868597667152053574774449174269361061887850701528018652043981280413438726741121762168166626267638699107735179}
```

Allright, we can indeed recover both the `public key` and the `encrypted message`. For the following, we can keep working on that same `tmp` blob and automate the decoding using python:

```python
# Decode blob, recover public key and encrypted message
j = json.loads(zlib.decompress(base64.b64decode(data)))
pub, enc = j['public_key'], j['encrypted']
```

The flag is encrypted using `encrypt(B,FLAG)`, where `B` is the `public key` (array of random numbers). Encryption consists in multiplying each bit of the `Flag` by the value of the `public key` at the corresponding position, then taking the sum of the all thing:

```python
def encrypt(B,message):
	message = list(map(int,list(bin(int.from_bytes(message,byteorder='big'))[2:])))

	encrypted_message = []
	for bit, b in zip(message, B):
		encrypted_message.append(b * bit)

	return sum(encrypted_message)

(...)
data = encode({"public_key" : B, "encrypted": encrypt(B,FLAG)})
```

So this is a well-known `Knapsack` system (the title was a huge hint):
- `Sum_n(ei*ai) = s`
- `(ai)_n` are known: those are the values from the `public key`
- `s` is known: this is the resulting sum, i.e the `encrypted` value
- `(ei)_n` are the coefficients to recover: those are the bits from the `FLAG` to recover

Lattice reduction is a known attack vector, allowing to recover the coefficients `(ei)_n`, i.e. the `FLAG`.

## Lattice reduction attack on knapsack system
There's a lot of litterature about it. For instance: https://eprint.iacr.org/2023/032.pdf, where the strategy is formulated as follow:
> [construct a lattice which contains a vector encoding the ei as a short vector.]

The standard solution consists in reducing a `block-based matrix` of `size n+1` composed as follow:
> M = [[I, P], [O, E]]

where:
- I is the `Identity matrix` of size `n`
- P is the colomn vector of size `n`, made of the values of `public key`
- 0 is the `Null horizontal vector` of size `n`
- E is the one-by-one matrix containing the value of the sum, i.e. the `encrypted` value

Then, considering an input vector `v=(e1,e2,...,en,-1)`, v*M gives the (short) vector `v'=(e1,e2,...,en,0)`

An amelioration to it is made in the `CJLOSS` algorithm, where the matrix M is slightly different:
> M = [[I, NP],[H, NE]]

where:
- N = ceil(sqrt(n) / 2)
- I is still the `Identity matrix` of size `n`
- N*P is the colomn vector of size `n`, made of the values of `public key` multiplies by `N`
- H is the `horizontal vector` of size `n` made of value 1/2
- N*E is the one-by-one matrix containing the value of the sum, i.e. the `encrypted` value, multiplied by `N`

Here, considering an input vector `v=(e1,e2,...,en,-1)`, v*M gives the (short) vector `v'=(e1-1/2,e2-1/2,...,en-1/2,0)`

Here's the python implementation, where we build the `Block matrix` used in the `CJLOSS` algo, using the `sage` library:

```python
    P = Matrix(ZZ, pub).transpose()
    I = Matrix.identity(ZZ, n)
    H = Matrix(QQ,[1/2 for _ in range(n)])
    E = Matrix(ZZ,[enc])

    # Build block matrix
    # Use the CJLOSS algorithm (small variant to the LO algo)
    # See https://eprint.iacr.org/2023/032.pdf for instance
    # |   I=I(n)  | N*P |
    # |-----------|-----|
    # | H=[1/2]*n | N*E |
    N = ceil(sqrt(n) / 2)
    M = block_matrix([[I, N*P], [H, N*E]])

    # Reduce the matrix
    R = M.LLL()
    print('[*] matrix reduced')
```

Then we need to find a `Good vector` in the `Reduced matrix`, i.e. one that consists in only zeros or ones:

```python
def findgoodvect(m):
    for v in m:
        if v[-1] == 0:
            good = True
            for i in range(len(v) - 1):
                vi = 1 - (v[i] + (1 / 2))
                if vi != 1 and vi != 0:
                    good = False
                    break
        if good:
            return v
    return None

(...)

	# Find good vector
	e = findgoodvect(R)
```

Once we found a `Good vector e`, we can recover the encoded bitstream and the flag !

```python
    # Recover message
    msg = ''
    for i in range(len(e) - 1):
        ei = 1 - (e[i] + (1 / 2)) # Because CJLOSS is used
        msg += str(int(ei))

    print('[*] binary:', msg)
    msg = '00' + msg[:-2] # hack to make it work, not sure why ??
    flag = ''.join([ chr(int(c, 2)) for c in list(sliced(msg, 8)) ])
    return flag
```

Here's the console output:

```console
$ python3 sol.py
[*] enc 1554330031748566348256886076643487598070443339530824300578945212914551502156587322291836646817783519587101304061071357078807658454104181329600844867618029914887067771959744871680016128722028006589977874298129337441734329964835076299558655448645350532522708039380148485980834562974640975216845438653289214969168532481432885580226545239262817315108780941835540601328751858136643616315851488247604734510349510838816718788454389974297985613711849529400486878871428345746090699725504519585885380188682040398840983211868597667152053574774449174269361061887850701528018652043981280413438726741121762168166626267638699107735179
[*] matrix reduced
[*] binary: 1101000011000000110100010000110101010001000110011110110111010101001110010111110111001100110100010000110101111101000000010111110110010000110000011100110101111101000010001100010011001101101110010111110111001000110100010011100110011100110011001000010111110100
[*] flag 404CTF{uN_s4C_@_d0s_B13n_r4Ng3!}
```

## Python code
Complete solution in [sol.py](./sol.py)

## Flag
> 404CTF{uN_s4C_@_d0s_B13n_r4Ng3!}
