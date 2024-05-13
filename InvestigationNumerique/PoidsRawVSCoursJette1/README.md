<div align="center">
    <h1 style=>Poids Raw vs. Cours Jette</h1>
    <i>Rootkit, Cracking, Exfiltration de données</i> 
</div>

# Introduction

Cette série de challenges est le résultat du travail commun de OwlyDuck et Lowengeist. Le but était de montrer des techniques de persistance dans un environnement original.

Nous nous sommes tournés vers les équipements réseaux par envie de trouver de nouveaux scénarios d'exploitation. De plus, nous sommes sortis de notre zone de confort pour proposer des choses que nous ne maîtrisions pas.

Cependant, des raccourcis ont été pris, et certaines alternatives abandonnées vont apparaître dans ce Write Up

# Énoncé de la partie 1

><div style="margin-bottom: 1em;"><i>Cette série de challenges implique un scénario d'attaque mettant en œuvre des programmes qui peuvent potentiellement nuire à vos équipements, nous faisons appel à votre vigilance pour toute forme d'analyse dynamique</i></div>
>
>Bienvenue chez **Entreprendre** !
>
>Nous sommes une entreprise jeune et dynamique spécialisée dans les poids. Si vous appréciez observer des boulets se projeter, enfin se faire projeter, venez lancer les nôtres !
>
>Nous avons remarqué une perte de réseau récemment et il semblerait que le switch **feuille3** ait redémarré pour des raisons inexplicables. Notre responsable du réseau a investigué, mais rien trouvé d'étrange. Dans le doute, il a fait une **capture de RAM** du switch et vous désigne vous, **oui vous**, pour trouver ce qui cloche.
>
>Nous pensons qu'il s'agit là d'un coup de nos rivaux : **Imagine**... Ces derniers travaillent dans le lancer de javelot, une discipline hérétique et vulgaire qui nous écœure ! Nous aurions dû faire attention et mettre des mots de passe plus forts sur nos équipements !
>
>*** 
>
>Trouvez le **pid** et le hash **md5** du malware présent sur le switch
>
>Format du Flag : `404CTF{111:891f490e5d7bdb06d90d56f8d7db405f}`
>
>Auteurs : @**OwlyDuck** & @**Lowengeist**



# Solution partie 1

## Identification

Comme d'habitude, on commence par une phase d'identification pour bien comprendre la nature du fichier fournit.

L'énoncé nous indique qu'il s'agit de la capture RAM d'un switch. Il faut donc identifier le système d'exploitation utilisé pour tenter de faire un profil **Volatility**.

### Identification des banners

```
$ vol3 -f memory.elf banners
Volatility 3 Framework 2.7.0
Progress:  100.00       PDB scanning finished                   
Offset  Banner

0x6fbf6d8   Linux version 5.10.0-cl-1-amd64 (dev-support@cumulusnetworks.com) (gcc-8 (Debian 8.3.0-6) 8.3.0, GNU ld (GNU Binutils for Debian) 2.31.1) #1 SMP Debian 5.10.189-1+cl5.8.0u16 (2024-01-27)
[...]
```

Le nom cumulusnetworks apparaît, ce qui nous permet d'établir que le système d'exploitation utilisé est  [Cumulus Networks](https://en.wikipedia.org/wiki/Cumulus_Networks).

On voit que l'OS est actuellement développé par Nvidia, et sert pour des gros switch de cloud. De plus, une VM toute faite existe [ici](https://www.nvidia.com/en-us/networking/ethernet-switching/cumulus-vx/).

Si l'on est frileux à l'idée de partager des informations pour télécharger l'image, on peut toujours trouver les paquets intéressants [ici](https://download.nvidia.com/cumulus/apt.cumulusnetworks.com/repo/pool/cumulus/l/linux/)

### Création du profil

#### Volatility 3

Il faut extraire le vmlinux et le System.map des paquets mentionnés plus haut, puis utiliser l'outil `dwarf2json` pour créer un fichier json qui contient tout ce qu'il faut. Pas besoin de VM ici.

#### Volatility 2

La solution utilisant Cumulus VX est proposée parce qu'elle est plus simple.

On lance la machine virtuelle et on suit [le tutoriel](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux-59/Quick-Start-Guide/).

Pour installer les paquets nécessaires pour faire un profil, il faut décommenter le fichier présents dans le `/etc/apt/sources.list` et lancer la commande `apt update`.

Ensuite suivre [le wiki](https://github.com/volatilityfoundation/volatility/wiki/Linux).

## Enquête

### PID
On nous demande de trouver le **PID** d'un processus malveillant, donc on va lancer la commande `pslist` avec volatility : [Résultat ici](./pslist.txt)

Pour savoir quel processus est malveillant, on cherche ce qui sort de l'ordinaire, soit `anssible`. C'est clairement un jeu de mot pourri des créateurs du chall, ce qui n'est pas étonnant vu le nom du challenge :D

Le **PID** du processus est donc **6985**.

Plusieurs tentatives ont été faites pour lancer le binaire at boot, dont la plus sympa est [la suivante](https://pberba.github.io/security/2022/02/07/linux-threat-hunting-for-persistence-systemd-generators/#whats-next). Un cron job était une option aussi, mais aucune des deux solutions ne semblait marcher pour des raisons obscures. J'ai lancé le binaire en ssh comme un looser du coup :/

### Hash du binaire

Ici est la partie un peu injuste pour certains participants qui se sont contentés d'utiliser volatility3 car `vol3 -s ../symbols -f cumulus-memory linux.proc --pid 6985 --dump` ne permet pas de récupérer le hash du fichier lancé.

C'est dommage, j'aurais bien aimé que ça soit possible. Cependant la première partie était une mise en jambe pour vraiment permettre de faire la suite, notamment la partie reverse, et c'était donc une manière d'être sûr que les éléments nécessaires étaient récupérés.

#### Intended way

Le plugin `linux_recover_filesystem` permet de trouver tous les fichiers présents dans la ram avec leurs chemins respectifs, dont `/usr/bin/anssible`.

Il faut donc ensuite calculer le hash MD5 du binaire.

#### Unintended way

Chose intéressante, pour m'assurer que le binaire apparaitrait dans la RAM, j'ai calculé son hash SHA-256. Ce que je n'avais pas prévu, c'est que ce hash là apparaît lui aussi, conséquemment. La différence de hash fait que le challenge, donc ma bourde, n'était pas si grave, en théorie.

Cependant, avec le nombre de participants et la durée de l'événement, c'était inévitable que quelqu'un upload le binaire sur VirusTotal. La conséquence de ça, c'est qu'une recherche à partir du SHA-256 trouvé dans la ram donne le MD5.

Honnêtement, l'unintended me plaît, introduit VirusTotal, qui est juste un super site à connaître. Cependant, c'est dommage pour les personnes qui se sont cassées les pieds à faire l'intended, même si c'est plus pratique pour la suite.

[Manière de retrouver le hash SHA-256 facilement](./grepped_strings.txt)