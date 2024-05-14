<div align="center">
    <h1 style=>Poids Raw vs. Cours Jette</h1>
    <i>Rootkit, Cracking, Exfiltration de données</i> 
</div>

# Petit mot

Ceci est vraiment la partie finale du challenge, où on met tout en commun. La nature de la connexion aurait pu être bien plus chevelue, mais ce n'était pas une difficulté souhaitée. La manière d'implémenter RC4 permet de faire une inintended assez marrante (sera présentée dans la solution).

Le fichier de flag était censé être une image split entre plusieurs paquets, mais la phase de récupération ne marchait pas. En hommage à cette idée morte en cours de route, voici le meilleur résultat de récupération de flag :

![image presque bien](./almost_a_flag.jpg)

# Énoncé de la partie 3

><div style="margin-bottom: 1em;"><i>Cette série de challenges implique un scénario d'attaque mettant en œuvre des programmes qui peuvent potentiellement nuire à vos équipements, nous faisons appel à votre vigilance pour toute forme d'analyse dynamique</i></div>
>
>Ça nous avance... Vous devriez désormais avoir toutes les **clés** pour retrouver quelles informations nous ont été soutirées... non ?
>
>Allez, on croit en vous... Voici une capture réseau, qui, on l'espère, vous sera utile !
>
>*** 
>
><style>#multi-author:before { content: "Auteurs : ";}</style>
><div class="author" id="multi-author"> @OwlyDuck & @Lowengeist</div>
>

# Solution de la partie 3

## Analyse globale de la capture réseau

On analyse la pcap pour retrouver les flux udp d'exfiltration. On pouvait trouver le port de réception en faisant du reverse des appels socket ou en utilisant le plugin netscan de volatility.

On peut donc faire un filtre pour voir seulement le protocole udp, rajouter les addresses ip en filtre, et le port d'envoi également.

Une fois le filtre appliqué, on se rend compte qu'il y a du chiffrement de données d'exfiltration, et que c'est vraisemblablement bit par bit de la même manière pour chaque paquet car les données se ressemblent.

Il y a ici deux chiffrements qui peuvent être retrouvés dans le code source.

## Chiffrement du rootkit

### En faisant du reverse

Je vous encourage à regarder des write up de participants pour voir la méthode de rétro-ingénierie qui leur a permis de comprendre ce qu'il se passait. Cependant, le code source est présent et permet de comparer avec le résultat compilé.

On peut donc voir que le rootkit fait du RC4 ligne 272 et 294. C'est un algorithme de chiffrement bien connu des ctf facilement implémentable (oui, flemme de faire des trucs plus compliqués). On peut donc retrouver la clé dans la mémoire (ligne 20) et faire le déchiffrement.

En termes de script de résolution, [ce programme](../../RetroEngenierie/PoidsRawVSCoursJette2/sniffing/udp_client.c) montre bien ce qui peut être fait.

### En faisant du sandboxing comme un gros BG

Flemme de reverse un rootkit ? Exécute-le dans une VM et comprendre ce qu'il fait de cette manière.

Bon pour ça il faut un peu guess que l'opération est un xor, ou alors faire du reverse sans comprendre que c'est du RC4. De toute manière, on peut bien voir que c'est le même chiffrement pour chaque paquet au vu des ressemblances. L'idée, c'est de faire un faux malware qui émet un signal 31 puis envoie un grand paquet udp rempli de zéros.

```c
#include <stuff>
[...]

int main(int argc, char **argv) {

    char * buffer = calloc(1,4000) // ou la taille du plus grand paquet udp de la pcap
    // se tagg soit même en hidden
    pid = getpid();
    if (fork()==0) {
        kill(pid, 31);
        exit(0);
    } else {
        wait(NULL);
    }
    // créer une socket
    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0))<0) {
        return EXIT_FAILURE;
    }
    memset(&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(31337);
    servaddr.sin_addr.s_addr = inet_addr(argv[1]);

    int n;
    len = sizeof(servaddr);
    sendto(sockfd, buffer, 4000, MSG_CONFIRM, (const struct sockaddr *)&servaddr, sizeof(servaddr));
}
```

Puis faire une capture réseau du paquet et voir la différence.

### Chiffrement du malware

CF partie 2, par rapport à la fonction brutus.

Elle ajoute 10 à chaque byte, donc il faut (sans se tromper d'ordre, donc après le xor) enlever 10 à chaque byte.

## Reconstitution

Un petit script python avec pyshark devrait permettre de déchiffrer chaque paquet.

Ensuite, soit on a la flemme et on concatène tous les paquets bruts déchiffrés et on fait un binwalk, soit on reconstruit la pcap en mettant les bons headers à chaque paquet, soit la timestamp et deux fois la longueur.

Si la récupération de la pcap vous intéresse, vous pouvez toujours regarder [notre programme](../../RetroEngenierie/PoidsRawVSCoursJette2/sniffing/udp_client.c). 
Il est évidemment à modifier, car il traitait les paquets au moment de la réception. 

Les deux méthodes permettent de trouver un fichier 7z qui contient le flag.

# Ressources utiles pour comprendre ce qu'est un rootkit

Les bases et un peu d'histoire, toujours un bon point de départ.

[Wikipedia](https://en.wikipedia.org/wiki/Rootkit)

Comprendre ce qu'est un module kernel, pas forcémént malveillant.

[Linux Device Drivers, Third Edition](https://lwn.net/Kernel/LDD3/)

Blog qui explique la base pour faire un module malveillant.

[(nearly) Complete Linux Loadable Kernel Modules](https://web.archive.org/web/20140701183221/https://www.thc.org/papers/LKM_HACKING.html)

Un des rootkit les plus connus, qui a inspiré celui présenté (celui de ce challenge aussi).

[Diamorphine](https://github.com/m0nad/Diamorphine)

Pour aller plus loin, blog qui montre des idées de fonctionnalités en plus.

[Blog chouette](https://xcellerator.github.io/posts/linux_rootkits_01/)

