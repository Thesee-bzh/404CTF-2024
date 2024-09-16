# Bugdroid Fight [1/2]

## Challenge
Un Bugdroid sauvage apparait !

Il est temps de mettre vos compétences de boxe en pratique, mais attention, cette fois il n'y a ni ring ni arbitre. Assurez-vous de bien observer autour de vous car, comme sur le ring, il est important de connaître les habitudes de son adversaire. Bon courage,

Retrouvez le message du Bugdroid.

> Format de flag : 404CTF{message}

## Inputs
- apk: [Bugdroid_Fight_-_Part_1.apk](./Bugdroid_Fight_-_Part_1.apk)

## Solution
Unzip the apk, then decompile the dex classes to recover the java code:
```console
$ /opt/jadx/bin/jadx -d classes2 classes2.dex --show-bad-code --comments-level debug
```

Looking in sources/com/example/reverseintro:
```java
                if (!Intrinsics.areEqual(name, element + StringResources_androidKt.stringResource(R.string.attr_special, startRestartGroup, 0) + new Utils().lastPart)) {
                    startRestartGroup.startReplaceableGroup(-332944370);
                    final Modifier modifier4 = modifier3;
                    TextKt.Text--4IGK_g("Bien joué, un bugdroid de vaincu !", modifier4, 0L, 0L, (FontStyle) null, (FontWeight) null, (FontFamily) null, 0L, (TextDecoration) null, (TextAlign) null, 0L, 0, false, 0, 0, (Function1) null, (TextStyle) null, startRestartGroup, (i4 & 112) | 6, 0, 131068);
                    startRestartGroup.endReplaceableGroup();
```

So the name (/flag) is composed of the following string parts:
- element
- StringResources_androidKt.stringResource(R.string.attr_special, startRestartGroup, 0)
- new Utils().lastPart

Looking for strings, to directly grab the first and the last pieces:
```console
$ grep -rn "String " |grep "="
MainActivityKt.java:47:    public static final String element = "Br4v0_tU_as_";
Utils.java:5:    String lastPart = "_m3S5ag3!";
```

For the 2nd one, we only get a string ID:
```console
$ grep -rn attr_special
R.java:49:        public static int attr_special = 0x7f0c0029;
```

So we have to recover the actual string. For that, I'll use `apktool` on the apk:
```console
apktool d Bugdroid_Fight_-_Part_1.apk
```

Looking for that attr_special string again, we can now recover it from the `strings.xml` file:
```console
$ grep -rn attr_special
res/values/strings.xml:44:    <string name="attr_special">tr0uv3_m0N</string>
```

So now we have all the pieces:
- element = "Br4v0_tU_as_";
- <string name="attr_special">tr0uv3_m0N</string>
- lastPart = "_m3S5ag3!";

## Flag
> 404CTF{Br4v0_tU_as_tr0uv3_m0N_m3S5ag3!}
