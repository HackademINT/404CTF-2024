import os
from Cryptodome.Util.number import long_to_bytes

class Generator:

	def __init__(self,feed):
		self.feed = feed

	def get_next_byte(self):
		number = 0

		for i in range(len(self.feed)):
			if i%2==0:
				number += pow(self.feed[i],i,2**8) + self.feed[i]*i
				number = ~number
			else:
				number ^= self.feed[i]*i+i


		number %= 2**8
		self.feed = self.feed[1:]
		self.feed.append(number)
		return number

	def get_random_bytes(self,length):
		random = b''

		for i in range(length):
			random += long_to_bytes(self.get_next_byte())

		return random
clear = open("flag.png.part",'rb').read()[:2000]
enc = open("flag.png.enc",'rb').read()[:2000]

BLOCK_SIZE = 4
flag = None

def get_blocks(data,block_size):
	return [data[i:i+block_size] for i in range(0,len(data),block_size)]

def xor(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

feed = list(b''.join([xor(clear[i:i+4],enc[i:i+4]) for i in range(0,2000,4)]))

print(feed,len(feed))

g = Generator(feed)

def pad(data,block_size):
	return data+b'\x00'*(len(data)%block_size)

def encrypt(data,block_size,generator):
	padded_data = pad(data,block_size)
	data_blocks = get_blocks(padded_data,block_size)
	encrypted = b''
	i = 0
	for block in data_blocks:
		print(round(i/len(data_blocks)*100,2),"%",i,end="\r")
		rd = generator.get_random_bytes(block_size)
		encrypted += xor(block,rd)
		i+=1
	return encrypted

with open("flag.png.enc",'rb') as f:
	flag = f.read()

with open('flag_dec.png', 'w+b') as f:
	e = encrypt(flag[2000:],BLOCK_SIZE,g)
	f.write(clear[:2000]+e)
