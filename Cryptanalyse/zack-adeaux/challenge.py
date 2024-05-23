from Crypto.Util.number import getRandomRange, getPrime
import math
import json
import zlib
import base64

from secrets import FLAG

def encode(data):
	data = json.dumps(data).encode("utf-8")
	data = zlib.compress(data)
	data = base64.b64encode(data)
	return data.decode("utf-8")

def encrypt(B,message):
	message = list(map(int,list(bin(int.from_bytes(message,byteorder='big'))[2:])))

	encrypted_message = []
	for bit, b in zip(message, B):
		encrypted_message.append(b * bit)

	return sum(encrypted_message)

def genKeys(n,size):
	a = getRandomRange(1, n)

	A = [getRandomRange(1, 2**512)]
	s = A[-1]
	for i in range(1,size):
		A.append(getRandomRange(s+1,192 * s))
		s += A[-1]

	B = [ (A[i] * a) % n for i in range(len(A)) ]

	return A, B, a

if __name__ == "__main__":
	n = getPrime(2048)
	A, B, a = genKeys(n,256)
	data = encode({"public_key" : B, "encrypted": encrypt(B,FLAG)})

	print("Zut ! J'ai renversé mon sac à dos et tout est tombé par terre, vous pourriez mettre un peu d'ordre dans tout ça ?")	
	print(data)