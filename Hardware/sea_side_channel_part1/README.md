# Sea side channel [1/4] - Introduction

## Challenge
NB : Il n'est pas nécessaire de calculer l'isogénie phi elle-même, il suffit de calculer le nouveau B à l'aide de la fonction Velu complétée précédemment. L'opération Q = phi(Q) n'est pas non plus nécessaire: on peut remplacer Q par n'importe quel point de EB adapté, et pas forcément par phi(Q).

Vous et votre collègue, Alice, ne cessez de gagner les compétitions d'haltérophilie. Cela est probablement dû en grande partie à votre échange continu de nouvelles méthodes d'entrainement !

Cependant, vos prochaines compétitions sont dans des pays différents et vous décidez donc de protéger vos messages pour éviter que des concurrents puissent vous copier. Il semblerait malheureusement que certains de ces concurrents aient à leur disposition des ordinateurs quantiques ! Alice vous a donc proposé d'utiliser un chiffrement à base d'isogénies : CSIDH.

Ce challenge est un fichier jupyter notebook avec une progression pas à pas pour commencer à comprendre CSIDH, complétez le code là où des espaces sont démarqués par des séries de "......" et finissez par déchiffrer le message que vous a envoyé Alice.


```console
$ python3 Chall_1_CSIDH2.py
0 3 Elliptic Curve defined by y^2 = x^3 + 158*x^2 + x over Finite Field of size 419
0 3 Elliptic Curve defined by y^2 = x^3 + 410*x^2 + x over Finite Field of size 419
0 3 Elliptic Curve defined by y^2 = x^3 + 368*x^2 + x over Finite Field of size 419
0 3 Elliptic Curve defined by y^2 = x^3 + 404*x^2 + x over Finite Field of size 419
1 5 Elliptic Curve defined by y^2 = x^3 + 295*x^2 + x over Finite Field of size 419
2 7 Elliptic Curve defined by y^2 = x^3 + 275*x^2 + x over Finite Field of size 419
0 3 Elliptic Curve defined by y^2 = x^3 + 158*x^2 + x over Finite Field of size 419
0 3 Elliptic Curve defined by y^2 = x^3 + 410*x^2 + x over Finite Field of size 419
0 3 Elliptic Curve defined by y^2 = x^3 + 368*x^2 + x over Finite Field of size 419
0 3 Elliptic Curve defined by y^2 = x^3 + 404*x^2 + x over Finite Field of size 419
0 3 Elliptic Curve defined by y^2 = x^3 + 75*x^2 + x over Finite Field of size 419
0 3 Elliptic Curve defined by y^2 = x^3 + 144*x^2 + x over Finite Field of size 419
1 5 Elliptic Curve defined by y^2 = x^3 + 6*x^2 + x over Finite Field of size 419
1 5 Elliptic Curve defined by y^2 = x^3 + 368*x^2 + x over Finite Field of size 419
1 5 Elliptic Curve defined by y^2 = x^3 + 220*x^2 + x over Finite Field of size 419
1 5 Elliptic Curve defined by y^2 = x^3 + x over Finite Field of size 419
1 5 Elliptic Curve defined by y^2 = x^3 + 199*x^2 + x over Finite Field of size 419
1 5 Elliptic Curve defined by y^2 = x^3 + 51*x^2 + x over Finite Field of size 419
1 5 Elliptic Curve defined by y^2 = x^3 + 413*x^2 + x over Finite Field of size 419
2 7 Elliptic Curve defined by y^2 = x^3 + 29*x^2 + x over Finite Field of size 419
2 7 Elliptic Curve defined by y^2 = x^3 + 245*x^2 + x over Finite Field of size 419
2 7 Elliptic Curve defined by y^2 = x^3 + 51*x^2 + x over Finite Field of size 419
2 7 Elliptic Curve defined by y^2 = x^3 + 410*x^2 + x over Finite Field of size 419
2 7 Elliptic Curve defined by y^2 = x^3 + 191*x^2 + x over Finite Field of size 419
2 7 Elliptic Curve defined by y^2 = x^3 + 199*x^2 + x over Finite Field of size 419
2 7 Elliptic Curve defined by y^2 = x^3 + 40*x^2 + x over Finite Field of size 419
2 7 Elliptic Curve defined by y^2 = x^3 + 344*x^2 + x over Finite Field of size 419
344
0 3 Elliptic Curve defined by y^2 = x^3 + 228*x^2 + x over Finite Field of size 419
0 3 Elliptic Curve defined by y^2 = x^3 + 275*x^2 + x over Finite Field of size 419
0 3 Elliptic Curve defined by y^2 = x^3 + 344*x^2 + x over Finite Field of size 419
0 3 Elliptic Curve defined by y^2 = x^3 + 15*x^2 + x over Finite Field of size 419
0 3 Elliptic Curve defined by y^2 = x^3 + 51*x^2 + x over Finite Field of size 419
0 3 Elliptic Curve defined by y^2 = x^3 + 9*x^2 + x over Finite Field of size 419
1 5 Elliptic Curve defined by y^2 = x^3 + 379*x^2 + x over Finite Field of size 419
1 5 Elliptic Curve defined by y^2 = x^3 + 344*x^2 + x over Finite Field of size 419
1 5 Elliptic Curve defined by y^2 = x^3 + 191*x^2 + x over Finite Field of size 419
1 5 Elliptic Curve defined by y^2 = x^3 + 245*x^2 + x over Finite Field of size 419
1 5 Elliptic Curve defined by y^2 = x^3 + 404*x^2 + x over Finite Field of size 419
1 5 Elliptic Curve defined by y^2 = x^3 + 295*x^2 + x over Finite Field of size 419
1 5 Elliptic Curve defined by y^2 = x^3 + 158*x^2 + x over Finite Field of size 419
2 7 Elliptic Curve defined by y^2 = x^3 + 144*x^2 + x over Finite Field of size 419
2 7 Elliptic Curve defined by y^2 = x^3 + 124*x^2 + x over Finite Field of size 419
2 7 Elliptic Curve defined by y^2 = x^3 + 295*x^2 + x over Finite Field of size 419
2 7 Elliptic Curve defined by y^2 = x^3 + 275*x^2 + x over Finite Field of size 419
2 7 Elliptic Curve defined by y^2 = x^3 + 261*x^2 + x over Finite Field of size 419
2 7 Elliptic Curve defined by y^2 = x^3 + 404*x^2 + x over Finite Field of size 419
2 7 Elliptic Curve defined by y^2 = x^3 + 413*x^2 + x over Finite Field of size 419
2 7 Elliptic Curve defined by y^2 = x^3 + 29*x^2 + x over Finite Field of size 419
29
Personne ne pourra nous écouter ! 404CTF{C4lcul_d'1s0g3n135_3n_b0rd_d3_m3r}
```

## Flag
> 404CTF{C4lcul_d'1s0g3n135_3n_b0rd_d3_m3r}
