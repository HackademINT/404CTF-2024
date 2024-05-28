#include <netinet/in.h>
#include <arpa/inet.h> 
#include <pcap/pcap.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include <signal.h>
#include <pcap.h>
#include <sys/time.h>

int sockfd;
struct sockaddr_in servaddr;
socklen_t len;
pcap_t *p;
pcap_dumper_t *dump_file;

unsigned char key[] = {
	0xfc,0x07,0xf2,0x5a,0xb6,
	0xb3,0xcd,0xe2,0x42,0x06,
	0x38,0x4f,0x4a,0x35,0x0a,
	0x1a,0xa4,0x93,0x8b,0x47,
	0x6c,0x0e,0x62,0x8b,0xfd,
	0xa5,0x27,0xda,0xab,0x41,
	0x19,0x03,0x3e,0x83,0x42,
	0x4a,0x04,0xcc,0x6f,0x32,
	0xe9,0x20,0x27,0xaa,0x0e,
	0xd4,0x00,0x81,0x38,0xb6,
	0x96,0xf5,0x54,0x06,0xe3,
	0xb5,0xe3,0xb4,0x7e,0xd7,
	0x0f,0x46,0x5c,0x48
};

struct args {
	unsigned char * packet;
	size_t n;
};

void intHandler(int dummy) {
	u_char msg[] = {0x71,0x75,0x69,0x74}; 
	sendto(sockfd, msg, sizeof(msg), MSG_CONFIRM,(const struct sockaddr *)&servaddr, sizeof(servaddr));
	pcap_dump_flush(dump_file);
	close(sockfd);
	exit(0);
}

void swap_bytes(unsigned char *a, unsigned char *b) {
	unsigned char tmp = *a;
	*a = *b;
	*b = tmp;
}

unsigned char *ksa(unsigned char *key, unsigned char key_len) {
	unsigned char *state;
	unsigned short i;
	unsigned short j;
	state = malloc(256);

	if (state == NULL)
		return NULL;
	
	for (i = 0; i<256; i++) {
		state[i] = i;
	}
	j=0;
	for (i=0; i<256; i++) {
		j = (j + state[i] + key[i%key_len]) & 0xff;
		swap_bytes(&state[i], &state[j]);
	}

	return state;
}

int cipher(unsigned char *state, unsigned char buff[], size_t buff_size) {
	unsigned char i = 0;
	unsigned char j = 0;
	unsigned char k;
	size_t byte_index;

	if (state == NULL)
		return -1;
	for (byte_index = 0; byte_index < buff_size; byte_index++) {
		i++;
		j += state[i];
		swap_bytes(&state[i], &state[j]);
		k = state[i] + state[j];
		k = state[k];
		buff[byte_index] ^= k; 
	}
	return 0;
}

void unbrutus(unsigned char *packet, size_t n) {
	for (int i = 0; i<n; i++) {
		packet[i] -= 10;
	}
}

void *writing_packet(void *arg) {
	struct args *packet_info = (struct args *) arg;
	unsigned char* packet = packet_info->packet;
	size_t n = packet_info->n;

	cipher(ksa(key, sizeof(key)), packet, n);
	unbrutus(packet, n);

	struct pcap_pkthdr *packet_header = malloc(sizeof(struct pcap_pkthdr));
	packet_header->caplen = n;
	packet_header->len = n;
	gettimeofday(&(packet_header->ts), NULL);

	pcap_dump((u_char *)dump_file, packet_header, packet);

	free(packet_header);
	free(packet);
	free(arg);
	return NULL;
}

int main(int argc, char **argv) {
	signal(SIGINT, intHandler);
	unsigned char * packet;
	unsigned char flag_n_if[] = {
		0x34,0x30,0x34,0x43,0x54,
		0x46,0x7b,0x34,0x74,0x54,
		0x33,0x6e,0x74,0x31,0x30,
		0x4e,0x5f,0x34,0x75,0x5f,
		0x43,0x72,0x30,0x63,0x48,
		0x33,0x74,0x21,0x7d,0xcd,
		0xda,0xae,0x8f
	};
	char errbuf[PCAP_ERRBUF_SIZE];
	p = pcap_open_dead(DLT_EN10MB, 65535);

	dump_file = pcap_dump_open(p,"capture_finale.pcap");
	if ( !dump_file ) {
		printf("Error : %s\n", pcap_geterr(p));
		return 1;
	}
	pthread_t th;

	if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0))<0) {
		fprintf(stderr, "FUCK");
		close(sockfd);
		return EXIT_FAILURE;
	}

	memset(&servaddr, 0, sizeof(servaddr));

	servaddr.sin_family = AF_INET;
	servaddr.sin_port = htons(31337);
	servaddr.sin_addr.s_addr = inet_addr(argv[1]);
	
	int n;
	len = sizeof(servaddr);
	sendto(sockfd, flag_n_if, sizeof(flag_n_if), MSG_CONFIRM, (const struct sockaddr *)&servaddr, sizeof(servaddr));

	while (1) {
		packet = malloc(100000);
		n = recvfrom(sockfd, packet, 100000, MSG_WAITALL, ( struct sockaddr *) &servaddr, &len);
		if (n == 100000)
			puts("limit reached");
		struct args *to_pass = malloc(sizeof(struct args));
		to_pass->packet = packet;
		to_pass->n = n;
		pthread_create(&th, NULL, writing_packet, to_pass);
	}
	close(sockfd);
	return 0;
}
