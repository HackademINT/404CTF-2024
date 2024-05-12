# Serial killer
Un challenge de lecture de trame UART

## Énoncé
En plein déménagement, vous avez invité votre amie haltérophile pour vous donner un coup de main et en deux temps trois mouvements, tout est déballé et rangé. Tout se passait bien, jusqu'au moment de rebrancher votre Arduino à votre PC. Elle essaie de rebrancher le port USB, inconsciente que le câble est dans le mauvais sens et... *CRAC* ! Le port se casse ! Grandement affecté par cet évènement, vous décidez de récupérer et de déchiffrer les dernières paroles que votre Arduino avait transmises à votre ordinateur afin de pouvoir les ajouter à son épitaphe.

## Structure
- 📄 `README.md` : ce fichier
- 📄 `chall.bin` : le challenge, un fichier en binaire brut
- 📁 `generator` : le générateur de trame, écrit en Rust
    - 📁 `src` : le code source du générateur, compilable avec `cargo build --release`. Le résultat se retrouvera dans 📁 `generator/target`
- 📁 `solver` : le solveur, écrit en Rust
    - 📁 `src` : le code source du solver, compilable de la même manière que `generator`

## Déroulé
Il faudra d'abord trouver un moyen de lire le fichier binaire pour rendre sa lecture humaine puis prendre connaissance du format d'une trame UART pour ensuite décoder le flag contenu dans les différentes trames

## Flag
`404CTF{Un3_7r1Ste_f1N_p0Ur_uN3_c4r73_1nn0c3nt3}`
