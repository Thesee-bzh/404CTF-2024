# Coup de circuit [1/3]

## Challenge
Ce challenge est le premier d'une série de trois challenges faciles. Le challenge suivant sera disponible dans la catégorie Renseignement en sources ouvertes une fois que vous aurez validé celui-ci.

C'est la catastrophe ! Je me prépare pour mon prochain match de baseball, mais on m'a volé mon mojo ! Sans lui, je vais perdre, c'est certain... Je crois qu'on m'a eu en me faisant télécharger un virus ou je ne sais quoi, et le fichier a été supprimé de mon ordinateur. J'ai demandé de l'aide à un ami expert et il a extrait des choses du PC, mais il n'a pas le temps d'aller plus loin. Vous pourriez m'aider ?

Identifiez le malware et donnez son condensat sha1. Le flag est au format suivant : 404CTF{sha1}

## Inputs
- A collection of files extracted from the PC: [Collection.zip](./Collection.zip)

## Solution
Let's inspect what we have:

```console
$ tree
.
├── amcache
│   ├── 20240505010820_Amcache_DeviceContainers.csv
│   ├── 20240505010820_Amcache_DevicePnps.csv
│   ├── 20240505010820_Amcache_DriveBinaries.csv
│   ├── 20240505010820_Amcache_DriverPackages.csv
│   ├── 20240505010820_Amcache_ShortCuts.csv
│   └── 20240505010820_Amcache_UnassociatedFileEntries.csv
├── mft
│   └── 20240505000512_MFTECmd_$MFT_Output.csv
└── prefetch
    ├── 20240504235816_PECmd_Output.csv
    └── 20240504235816_PECmd_Output_Timeline.csv

3 directories, 9 files
```

In `20240505010820_Amcache_UnassociatedFileEntries.csv`, few items from location `C:\users\rick\downloads` stick out:

```console
$ cat amcache/20240505010820_Amcache_UnassociatedFileEntries.csv  | awk -F ',' '{print $6}' | grep rick
c:\users\rick\downloads\.opera\opera installer temp\opera_package_202405042049081\assistant\assistant_installer.exe
c:\users\rick\appdata\local\temp\{17e2c094-424a-460e-8d1a-f225396ed583}\.be\dotnet-runtime-6.0.29-win-x64.exe
c:\users\rick\appdata\local\microsoft\onedrive\onedrive.exe
c:\users\rick\appdata\local\microsoft\onedrive\update\onedrivesetup.exe
c:\users\rick\appdata\local\microsoft\onedrive\onedrivestandaloneupdater.exe
c:\users\rick\downloads\operasetup.exe
c:\users\rick\downloads\sflgdqsfhbl.exe
```

Especially the file `sflgdqsfhbl.exe`, which really looks suscipious (which is confirmed by VirusTotal).

So we just report its `sha1 hash` (4th entry) as the flag:

```console
$ cat amcache/20240505010820_Amcache_UnassociatedFileEntries.csv  | grep sflgdqsfhbl
Unassociated,0006799086f2b3631ed09571eea308213bed0000ffff,2024-05-04 23:06:35,5cf530e19c9df091f89cede690e5295c285ece3c,False,c:\users\rick\downloads\sflgdqsfhbl.exe,sflgdqsfhbl.exe,.exe,2024-05-04 17:11:14,,7319454,,,,pe64_amd64,False,,,219273384,0,
$
$ grep -rin sha1
amcache/20240505010820_Amcache_UnassociatedFileEntries.csv:1:ApplicationName,ProgramId,FileKeyLastWriteTimestamp,SHA1,IsOsComponent,FullPath,Name,FileExtension,LinkDate,ProductName,Size,Version,ProductVersion,LongPathHash,BinaryType,IsPeFile,BinFileVersion,BinProductVersion,Usn,Language,Description
$
$ cat amcache/20240505010820_Amcache_UnassociatedFileEntries.csv | grep sflgdqsfhbl | awk -F, '{print $4}'
5cf530e19c9df091f89cede690e5295c285ece3c
```

## Flag
> 404CTF{5cf530e19c9df091f89cede690e5295c285ece3c}
