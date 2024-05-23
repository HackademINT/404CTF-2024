import os
from Crypto.Util.number import bytes_to_long,long_to_bytes
from flag import FLAG

Sbox = (
	0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
	0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
	0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
	0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
	0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
	0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
	0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
	0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
	0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
	0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
	0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
	0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
	0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
	0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
	0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
	0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
)

class Feistel:
	def __init__(self,SBox,key):
		assert len(key)==8
		self.ROUND_NB = 96
		self.BLOCK_SIZE = 8
		self.SBox = SBox
		self.key = key
		self.round_keys = [bytes_to_long(self.key[i:i+self.BLOCK_SIZE//2]) for i in range(0,self.BLOCK_SIZE,self.BLOCK_SIZE//2)]
		self.state = None

	def pad(self,data):
		if len(data)%self.BLOCK_SIZE==0:
			return data
		return data+b'\x00'*(self.BLOCK_SIZE-(len(data)%self.BLOCK_SIZE))

	def left_state(self):
		return self.state>>32

	def right_state(self):
		return self.state&0xffffffff

	def f(self,block):
		b1 = (block>>24) & 0xff
		b2 = (block>>16) & 0xff
		b3 = (block>>8) & 0xff
		b4 = block & 0xff
		b1 = self.SBox[b1]
		b2 ^= b1
		b2 = self.SBox[b2]
		b1 ^= b2
		b3 ^= b1
		b3 = self.SBox[b3]
		b4 = self.SBox[b4]
		b4 ^= b3
		return (b4<<24)+(b3<<16)+(b2<<8)+b1

	def swap_state(self):
		left = self.left_state()
		right = self.right_state()
		self.state = (right<<self.BLOCK_SIZE*4)+left

	def apply_round(self,round_number):
		f_input = self.right_state()^self.round_keys[round_number%2]
		f_output = self.f(f_input)
		left = self.left_state()^f_output
		right = self.right_state()
		self.state = (left<<self.BLOCK_SIZE*4)+right

	def apply_inverse_round(self,round_number):
		f_input = self.right_state()^self.round_keys[round_number%2]
		f_output = self.f(f_input)
		left = self.left_state()^f_output
		right = self.right_state()
		self.state = (left<<self.BLOCK_SIZE*4)+right

	def encrypt_block(self,block):
		self.state = bytes_to_long(block)
		for i in range(0,self.ROUND_NB):
			self.apply_round(i)
			self.swap_state()
		return long_to_bytes(self.state)

	def decrypt_block(self,block):
		self.state = bytes_to_long(block)
		for i in range(0,self.ROUND_NB):
			self.swap_state()
			self.apply_inverse_round(self.ROUND_NB-i-1)
		return long_to_bytes(self.state)

	def encrypt(self,data):
		blocks = [ self.pad(data[i:i+self.BLOCK_SIZE]) for i in range(0,len(data),self.BLOCK_SIZE) ]
		encrypted = b''
		for block in blocks:
			encrypted_b = self.encrypt_block(block)
			encrypted+=encrypted_b
		return encrypted

	def decrypt(self,data):
		blocks = [ data[i:i+self.BLOCK_SIZE] for i in range(0,len(data),self.BLOCK_SIZE) ]
		decrypted = b''
		for block in blocks:
			decrypted+=self.decrypt_block(block)
		return decrypted

	def check_keys(self,key1,key2):
		return key1 == self.round_keys[0] and key2 == self.round_keys[1]


print("""
	Help :
		- encrypt a block (block has to be in hex format) :\tencrypt <block>
		- decrypt a block (block has to be in hex format) :\tdecrypt <block>
		- check if keys are correct (keys has to be in hex format) :\tcheck <key1> <key2>
	""")

N = 262146
n_call = 0

key = os.urandom(8)
cipher = Feistel(Sbox,key)

while n_call<N:
	command = input()
	command = command.strip().replace("\n","").split(' ')

	if command[0] == 'encrypt' and len(command) == 2:
		try:
			block = bytes.fromhex(command[1])
			if len(block)==8:
				print(cipher.encrypt(block).hex())
				n_call += 1
			else:
				print("Wrong block size",len(block),"expected 8")
				exit()
		except:
			print("Wrong block")
			exit()

	elif command[0] == 'decrypt' and len(command) == 2:
		try:
			block = bytes.fromhex(command[1])
			if len(block)==8:
				print(cipher.decrypt(block).hex())
				n_call += 1
			else:
				print("Wrong block size",len(block),"expected 8")
				exit()
		except:
			print("Wrong block")
			exit()

	elif command[0] == "check" and len(command) == 3:
		try:
			key1 = int(command[1],16)
			key2 = int(command[2],16)
			if cipher.check_keys(key1,key2):
				print("Congratulations !",FLAG)
			else:
				print("Wrong guess")
				exit()
		except:
			print("Wrong key blocks")
			exit()

	else:
		print("Unknow command")
		exit()
print("Enough work for today, bye !")