# Le match du siècle [1/2]

## Challenge
Vous voilà à quelques semaines du match tant attendu entre le Gorfou FC et l'AS Sealion.
Seulement, vous vous êtes pris au dernier moment pour acheter votre place. Trouvez un moyen d'obtenir un billet !

## Solution
Cookie is a JWT token, which we can modify the payload as follow to buy `laterale` places for instance:

```json
{
  "username": "Thesee01",
  "billets": {
    "VIP": 0,
    "Laterale": 1,
    "Familiale": 0,
    "Est": 0,
    "Ouest": 0,
    "Nord et Sud": 0
  },
  "iat": 1714584958
}
```

Apparently the JWT token signature is not verified, so it works:

![billets.png](./billets.png)

When fecthing the ticket, we get the flag:

![flag.png](./flag.png)

## Flag
> 404CTF{b5a77ed0fa6968b21df7fb137437fae1}
