# Vaut mieux sécuriser que guérir

## Challenge
Lors d'une compétition de lancer de poids, un athlète laisse son ordinateur allumé avec sa session ouverte. Cependant, une personne a utilisé son ordinateur et, a vraisemblablement fait des cachoteries. Nous vous mettons à disposition le dump de la RAM de l'ordinateur après l'incident.
Investiguez ce dump mémoire pour comprendre ce qu'il s'est passé.

La deuxième partie du flag est le nom d'une certaine tâche.
Les deux parties sont séparées d'un tiret "-". Par exemple si le flag de la première partie est "flag1" et celui de la deuxième partie est "flag2". Le réel flag du challenge sera 404CTF{flag1-flag2}

## Inputs
- A memory dump

## Analysis
Throwing some volatility plugins:
```console
$ python3 /opt/volatility3/vol.py -f memory.dmp windows.pstree > pstree.txt
$ python3 /opt/volatility3/vol.py -f memory.dmp windows.cmdline > cmdline.txt
$ python3 /opt/volatility3/vol.py -f memory.dmp windows.filescan > filescan.txt
```

Extracting evtx logs
```console
$ git clone https://github.com/spitfirerxf/vol3-plugins.git
$ sudo cp vol3-plugins/evtxlog.py /opt/volatility3/volatility3/plugins/windows/
$ python3 /opt/volatility3/vol.py -f memory.dmp windows.evtxlog > evtxlog.txt
```

Wooo... Something pretty bad in \Windows\System32\winevt\Logs\Microsoft-Windows-PowerShell%4Operational.evtx:
- PowerShell script `C:\Users\Maison\hacked.ps1` is executed

```xml
<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event"><System><Provider Name="Microsoft-Windows-PowerShell" Guid="{a0c1853b-5c40-4b15-8766-3cf1c58f985a}"></Provider>
<EventID Qualifiers="">4104</EventID>
<Version>1</Version>
<Level>3</Level>
<Task>2</Task>
<Opcode>15</Opcode>
<Keywords>0x0000000000000000</Keywords>
<TimeCreated SystemTime="2024-03-12 09:08:00.718916"></TimeCreated>
<EventRecordID>7</EventRecordID>
<Correlation ActivityID="{b3a7a58f-7463-0000-451a-a8b36374da01}" RelatedActivityID=""></Correlation>
<Execution ProcessID="1308" ThreadID="5536"></Execution>
<Channel>Microsoft-Windows-PowerShell/Operational</Channel>
<Computer>pc-maison</Computer>
<Security UserID="S-1-5-21-3483116880-2883818974-3464947896-1000"></Security>
</System>
<EventData><Data Name="MessageNumber">1</Data>
<Data Name="MessageTotal">1</Data>
<Data Name="ScriptBlockText">############################################################################################################################################################
#                                  |  ___                           _           _              _             #              ,d88b.d88b                     #
# Title        : Wallpaper-Troll   | |_ _|   __ _   _ __ ___       | |   __ _  | | __   ___   | |__    _   _ #              88888888888                    #
# Author       : I am Jakoby       |  | |   / _` | | '_ ` _ \   _  | |  / _` | | |/ /  / _ \  | '_ \  | | | |#              `Y8888888Y'                    #
# Version      : 1.0               |  | |  | (_| | | | | | | | | |_| | | (_| | |   &lt;  | (_) | | |_) | | |_| |#               `Y888Y'                       #
# Category     : Prank             | |___|  \__,_| |_| |_| |_|  \___/   \__,_| |_|\_\  \___/  |_.__/   \__, |#                 `Y'                         #
# Target       : Windows 10,11     |                                                                   |___/ #           /\/|_      __/\\                  #
# Mode         : HID               |                                                           |\__/,|   (`\ #          /    -\    /-   ~\                 #
#                                  |  My crime is that of curiosity                            |_ _  |.--.) )#          \    = Y =T_ =   /                 #
#                                  |   and yea curiosity killed the cat                        ( T   )     / #   Luther  )==*(`     `) ~ \   Hobo          #                                                      
#                                  |    but satisfaction brought him back                     (((^_(((/(((_/ #          /     \     /     \                #
#__________________________________|_________________________________________________________________________#          |     |     ) ~   (                #
#                                                                                                            #         /       \   /     ~ \               #
#  github.com/I-Am-Jakoby                                                                                    #         \       /   \~     ~/               #
#  twitter.com/I_Am_Jakoby                                                                                   #   /\_/\_/\__  _/_/\_/\__~__/_/\_/\_/\_/\_/\_#
#  instagram.com/i_am_jakoby                                                                                 #  |  |  |  | ) ) |  |  | ((  |  |  |  |  |  |#
#  youtube.com/c/IamJakoby                                                                                   #  |  |  |  |( (  |  |  |  \\ |  |  |  |  |  |#
############################################################################################################################################################

&lt;#

.DESCRIPTION
        This program gathers details from target PC to include name associated with the microsoft account, their latitude and longitude,
        Public IP, and  and the SSID and WiFi password of any current or previously connected to networks.
        It will take the gathered information and generate a .jpg with that information on show
        Finally that .jpg will be applied as their Desktop Wallpaper so they know they were owned
        Additionally a secret message will be left in the binary of the wallpaper image generated and left on their desktop
#&gt;
#############################################################################################################################################

(...)
<powershell script>
(...)
</Data>
<Data Name="ScriptBlockId">7a4318a5-8a16-4fea-91db-595dc4732770</Data>
<Data Name="Path">C:\Users\Maison\hacked.ps1</Data>
</EventData>
</Event>
```

We can look for that `.jpg image` it is talking about:
```console
$ grep ".jpg" filescan.txt
(...)
0xd50eb9c32ef0  \Users\Maison\AppData\Roaming\Microsoft\Windows\Themes\CachedFiles\CachedImage_1024_768_POS0.jpg 216
$
$ python3 /opt/volatility3/vol.py -f memory.dmp windows.dumpfiles --virtaddr 0xd50eb9c32ef0
Volatility 3 Framework 2.7.0
Progress:  100.00               PDB scanning finished
Cache   FileObject      FileName        Result

DataSectionObject       0xd50eb9c32ef0  CachedImage_1024_768_POS0.jpg   file.0xd50eb9c32ef0.0xd50ebb2a37a0.DataSectionObject.CachedImage_1024_768_POS0.jpg.dat
```

It just contains some text:
```console
$ cp file.0xd50eb9c32ef0.0xd50ebb2a37a0.DataSectionObject.CachedImage_1024_768_POS0.jpg.dat img.jpg
$ tesseract img.jpg out
$ cat out
e1ByQG5rM2Qt
Hey

Your computer is not very secure

```

This is where I spent the most time ! I didn't realize it was `base64` encoded at first:
```console
$ echo -n e1ByQG5rM2Qt | base64 -d
{Pr@nk3d-
```

Allright, we have the first part of the flag `{Pr@nk3d-`.

Second part is the name of the scheduled task, i.e. `LUL`:
```powershell
Register-ScheduledTask -Action $Action -Trigger $Trigger -TaskName "LUL"
```

## Flag
> 404CTF{Pr@nk3d-LUL}
