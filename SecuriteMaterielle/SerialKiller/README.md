# Serial killer
Un challenge de lecture de trame UART

## Énoncé
Et votre prochaine épreuve est... le déménagement ? Vous avez donc invité votre amie haltérophile pour vous donner un coup de main et, en deux temps trois mouvements, tout est déballé et rangé. Tout se passait bien jusqu'au moment de rebrancher votre Arduino à votre PC. Elle essaie de rebrancher le port USB, mais ne dose pas sa force et... *CRAC !* Le port se casse ! Cet événement vous affecte grandement.

***

Vous décidez de récupérer et de déchiffrer les dernières paroles que votre Arduino avait transmises à votre ordinateur afin de pouvoir les ajouter à son épitaphe.

[https://docs.arduino.cc/learn/communication/uart/#technical-specifications](https://docs.arduino.cc/learn/communication/uart/#technical-specifications)

## Structure
- 📄 `README.md` : ce fichier
- 📄 `chall.bin` : le challenge, un fichier en binaire brut
- 📁 `generator` : le générateur de trame, écrit en Rust
    - 📁 `src` : le code source du générateur, compilable avec `cargo build --release`. Le résultat se retrouvera dans 📁 `generator/target`
- 📁 `solver` : le solveur, écrit en Rust
    - 📁 `src` : le code source du solver, compilable de la même manière que `generator`

## Déroulé
Il faudra d'abord trouver un moyen de convertir le binaire du fichier pour rendre sa lecture humaine puis prendre connaissance du format d'une trame UART pour ensuite décoder le flag contenu dans les différentes trames.

On pourrait procéder dans l'ordre suivant :  
- Passage du fichier chall.bin sous forme de 1 et de 0
- Identification de la longueur de trame en cherchant `x` tel qu'on trouve une suite de `0[x bits]1` dans le binaire, le 0 étant le bit de début d'une trame, le 1 le bit de fin. On doit trouver `x=8`.
- On regarde les 8 bits compris entre le bit de début et bit de fin des premières trames et on trouve qu'il y a un bit de trop pouvant être un `1` pour pouvoir décoder des caractères ASCII valides, on en déduit qu'il y a un bit de parité.
- On peut alors créer un script/programme pour décoder le binaire en tenant compte du fait que les bits de donnée de chaque caractère ont leur bit de poids faible à gauche en plus de toutes les informations recueillies précédemment.
- ???
- Profit

## Flag
`404CTF{Un3_7r1Ste_f1N_p0Ur_uN3_c4r73_1nn0c3nt3}`
