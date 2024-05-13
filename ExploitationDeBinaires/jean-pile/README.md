# Idée

Antismash était cassé et a donné une idée incroyable à Bdenneu pour le solve en polluant le saved eip avec des `ret` jusqu'à tomber sur une addresse qui l'arrangeait. De cette idée :
1. on a patché antismash pour que ça soit le challenge qu'on voulait à la base (LOL)
2. on s'est dit qu'on allait créer un chall qui profite de cet exploit en easy/medium
Du coup l'idée c'est :
- on a une fonction main qui appelle une fonction vuln, qui s'appelle récursivement et permet donc si on rewrite bien de faire ce qui est décrit dans le schéma ascii art suivant :
```
                                        -----------
                                        | (vuln)  |
                                        | AAAAA...|  C
                                        | ...A ret|
                                        -----------
                                        |ret ret  |
                                        |ret ...  |
                                        | (vuln)  |
                                        |ret ret  |  B
                                      --|RBP      |
                                     |  -----------
                                     |  | (vuln)  |
                                     |  |BBBB.... |  A
                                     |  |.... BBBB|
                                      ->|RBP      |
                                        -----------
                                        | (main)  |
                                        -----------
```
Et c'est ce schéma qui motive la suite du chall.

On keep aussi 0 protection pour que l'exploit se passe sans avoir à leak de trucs pour garder les choses simples.