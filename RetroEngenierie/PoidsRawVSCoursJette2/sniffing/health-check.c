#include <unistd.h>
int main() {
    char *args[] = {"/usr/bin/anssible", NULL};
    execv("/usr/bin/anssible", args);
}