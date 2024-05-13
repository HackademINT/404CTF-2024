# Coup de circuit

Série de challenges de threat intelligence.

1. Trouver le sha1 d'un malware via une collection classique de fichiers CSV
2. En recherchant le sha1 sur VirusTotal, identifier le domaine servant de command & control au malware, 
   et identifier une interface web d'administration sur un sous-domaine via son certificat tls.
3. Trouver le code source de l'interface sur GitHub et identifier un manque d'authentification pour les resources statiques,
   qui contiennent le flag.

## Énoncé 1

Investigation numérique - Facile - 200 points - 291 validations

*Ce challenge est le premier d'une série de trois challenges faciles.
Le challenge suivant sera disponible dans la catégorie
**Renseignement en sources ouvertes** une fois que vous aurez validé celui-ci.*


C'est la catastrophe !
Je me prépare pour mon prochain match de baseball, mais on m'a volé mon mojo !
Sans lui, je vais perdre, c'est certain...
Je crois qu'on m'a eu en me faisant télécharger un virus ou je ne sais quoi,
et le fichier a été supprimé de mon ordinateur.
J'ai demandé de l'aide à un ami expert et il a extrait des choses du PC,
mais il n'a pas le temps d'aller plus loin.
Vous pourriez m'aider ?

---

Identifiez le malware et donnez son condensat sha1.
Le flag est au format suivant : `404CTF{sha1}`

Auteur : @Smyler

## Énoncé 2

Renseignement en sources ouvertes - Facile - 200 points - 224 validations

*Le challenge suivant sera disponible dans la catégorie
**Divers** une fois que vous aurez validé celui-ci.*

Super !
Grace à vous j'ai pu retirer le fichier de mon PC,
mais pensez-vous qu'il serait possible d'en savoir un peu plus sur ce malware ?

---

Retrouvez l'interface web du panneau de Command & Control du malware.

Le flag y sera reconnaissable.

Auteur : @Smyler

## Énoncé 3

Divers - Facile - 940 points - 56 validations

*Pour ce challenge,
le service web à l'adresse suivante fait partie du périmètre :
https://panel-5d4213f3bf078fb1656a3db8348282f482601690.takemeouttotheballgame.space.
L'énumération automatique est toujours interdite.
Ce challenge est un mix de plusieurs catégories.*


Le fichier que l'on m'a volé se nomme `Secret-Mojo.pdf`.
Vous pensez que l'on peut le retrouver à partir du panneau de contrôle ?

Mettez la main sur le fichier dérobé.

Auteur : @Smyler
