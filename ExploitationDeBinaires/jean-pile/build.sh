cd src

gcc -z execstack -no-pie -fno-stack-protector main.c -o jean_pile

cp jean_pile ../jean_pile

mv jean_pile ../data/jean_pile