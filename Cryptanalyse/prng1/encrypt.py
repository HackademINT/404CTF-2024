from my_random import Generator
from Cryptodome.Util.number import long_to_bytes
def xor(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

def get_blocks(data,block_size):
	return [data[i:i+block_size] for i in range(0,len(data),block_size)]

def pad(data,block_size):
	return data+b'\x00'*(block_size-len(data)%block_size)

def encrypt(data,block_size):
	padded_data = pad(data,block_size)
	data_blocks = get_blocks(padded_data,block_size)
	generator = Generator()
	encrypted = b''

	for block in data_blocks:

		rd = generator.get_random_bytes(block_size)
		xored = xor(block,rd)
		encrypted+= xored
	return encrypted

BLOCK_SIZE = 4
flag = None

with open("flag.png",'rb') as f:
	flag = f.read()

with open('flag.png.enc', 'w+b') as f:
	f.write(encrypt(flag,BLOCK_SIZE))
