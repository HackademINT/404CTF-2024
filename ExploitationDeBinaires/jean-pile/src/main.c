#include <stdio.h>
#define INPUT_SIZE 200

void menu(void) {
    puts("                                              _                    ");
    puts("                                   .-.  .--'\'` )                  ");
    puts("                                _ |  |/`   .-\'`                   ");
    puts("                               ( `\\      /`                       ");
    puts("                               _)   _.  -'._                       ");
    puts("                             /`  .'     .-.-;                      ");
    puts("                             `).'      /  \\  \\                   ");
    puts("                            (`,        \\_o/_o/__                  ");
    puts("                             /           .-''`  ``'-.              ");
    puts("                             {         /` ,___.--\'\'`             ");
    puts("                             {   ;     \'-. \\ \\                  ");
    puts("           _   _             {   |\'-....-`\'.\\_\\                =============menu=============");
    puts("          / './ '.           \\   \\          `\"`                |                            |");
    puts("       _  \\   \\  |            \\   \\                            |          1 pouler          |");
    puts("      ( '-.J     \\_..----.._ __)   `\\--..__                    |          2 pouler          |");
    puts("     .-`                    `        `\\    ''--...--.          |          3 pouler          |");
    puts("    (_,.--""`/`         .-             `\\       .__ _)           |                            |");
    puts("            |          (                 }    .__ _)           ==============================");
    puts("            \\_,         '.               }_  - _.'                ");
    puts("               \\_,         '.            } `'--'                  ");
    puts("                  '._.     ,_)          /                          ");
    puts("                     |    /           .'                           ");
    puts("                      \\   |    _   .-'                            ");
    puts("                       \\__/;--.||-'                               ");
    puts("                        _||   _||__   __                           ");
    puts("                 _ __.-` \"`)(` `\"  ```._)                        ");
    puts("                (_`,-   ,-'  `''-.   '-._)                         ");
    puts("               (  (    /          '.__.'                           ");
    puts("                `\"`'--'\"                                         ");
    puts("");
}


void service(void) {
    int choice;
    int i;
    char buffer[30];
    puts("Voulez-vous commander un plat ou plus ?");
    printf(">>> ");
    fflush(stdin);
    scanf("%d", &choice);
    getchar(); // eating \n
    if (choice == 1) {
        puts("Choisissez un plat.");
        printf(">> ");
        if (fgets(buffer, INPUT_SIZE, stdin) == NULL) exit(-1);
        for (i = 0 ; i < INPUT_SIZE ; i++) {
            if (buffer[i] == '\n') {
                buffer[i] = 0;
            }
        }
    }
    else {
        puts("Choisissez un plat.");
        printf(">> ");
        if (fgets(buffer, INPUT_SIZE, stdin) == NULL) exit(-1);
        for (i = 0 ; i < INPUT_SIZE ; i++) {
            if (buffer[i] == '\n') {
                buffer[i] = 0;
            }
        }
        puts("Un nouveau serveur revient vers vous pour la suite de votre commande au plus vite.");
        service();
    }
    return;
}



int main(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    
    puts("Bienvenue dans la cantine de la fameuse course annuelle du 404 ctf !"); // welcome
    menu(); // showing menu

    service();

    puts("Merci à vous bonne soirée!"); // goodbye

    return 0;
}