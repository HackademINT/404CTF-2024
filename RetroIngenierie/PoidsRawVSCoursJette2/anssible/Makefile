obj-m = anssible.o
CC = gcc -Wall
KDIR := /lib/modules/$(shell uname -r)/build/
PWD := $(shell pwd)
all:
	make -C $(KDIR) M=$(PWD) modules
clean:
	make -C $(KDIR) M=$(PWD) clean
