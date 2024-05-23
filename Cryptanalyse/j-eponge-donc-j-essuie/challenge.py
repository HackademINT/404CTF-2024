from Crypto.Util.number import long_to_bytes,bytes_to_long
import os
from flag import FLAG

class Bob:
	def __init__(self, data):
		self.R_size = 32
		self.C_size = 96
		self.OUT_size = 512
		data = long_to_bytes(len(data)%256)+data+long_to_bytes(len(data)%256)
		self.data = self.bytes2binArray(data)
		self.state = [[0 for _ in range(self.R_size)],[0 for _ in range(self.C_size)]]

	def bytes2binArray(self,b):
		b = bin(bytes_to_long(b))[2:]
		b = '0'*(8-(len(b)%8))+b
		b = b+'0'*(self.R_size - (len(b)%self.R_size))
		return [int(i) for i in b]

	def binArray2bytes(self,b):
		bytes_in = [b[i:i+8] for i in range(0,len(b),8)]
		bytes_out = []
		for e in bytes_in:
			s = 0
			for i in range(8):
				s += e[i]*2**(7-i)
			bytes_out.append(s)
		return bytes(bytes_out)

	def xor(self,a,b):
		return [i^j for i,j in zip(a,b)]

	def _f(self):
		perm = [65, 107, 53, 90, 67, 35, 17, 100, 37, 103, 41, 92, 23, 120, 70, 11, 34, 73, 16, 29, 7, 91, 127, 69, 81, 26, 0, 98, 71, 51, 9, 112, 64, 121, 101, 47, 114, 30, 104, 113, 3, 27, 6, 32, 42, 93, 48, 21, 118, 99, 89, 84, 36, 110, 25, 102, 61, 39, 86, 50, 14, 10, 56, 28, 38, 62, 22, 46, 66, 19, 108, 18, 13, 125, 49, 2, 74, 95, 8, 122, 58, 5, 75, 97, 15, 63, 117, 123, 96, 24, 94, 43, 4, 33, 115, 45, 76, 80, 126, 109, 52, 12, 79, 72, 54, 77, 31, 57, 1, 87, 88, 60, 20, 55, 40, 111, 116, 44, 82, 85, 68, 105, 106, 83, 78, 124, 59, 119]
		input_perm = self.state[0].copy()+self.state[1].copy()
		output_perm = [input_perm[i] for i in perm]
		self.state = [output_perm[:self.R_size],output_perm[self.R_size:]]

	def _absorb(self):
		while len(self.data) != 0:
			input_data = self.data[:self.R_size]
			self.state[0] = self.xor(self.state[0],input_data)
			self.data = self.data[self.R_size:]
			self._f()

	def _squeeze(self):
		output = []
		while len(output) != self.OUT_size:
			output += self.state[0].copy()
			self._f()
		return output

	def digest(self):
		self._absorb()
		hash_out = self.binArray2bytes(self._squeeze())
		return hash_out

	def hexdigest(self):
		return self.digest().hex()

print("""

░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░  
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░  
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░  

Welcome ! I'll give you a hash, try to find an other byte sequence of different length that produces the same hash (give me in hex notation please)
""")

data = os.urandom(16)
digest = Bob(data).hexdigest()
print("Input of hash :",data.hex())
print("Hash :",digest)
pre_image = input("> ").strip().replace("\n","").lower()

if len(pre_image) == 32:
	print("Don't fool me, they have the same length")
	exit()
if len(pre_image) > 4000:
	print("It's a bit too long, I'm sure you can do better ;)")
	exit()

digest_user = Bob(bytes.fromhex(pre_image)).hexdigest()

if bytes.fromhex(pre_image) == data:
	print("Don't fool me ! It's the same input !")
	exit()
elif digest_user != digest:
	print("Wrong hash, here is your hash :",digest_user)
	exit()
else:
	print("Congratulation ! Here's the flag :",FLAG)