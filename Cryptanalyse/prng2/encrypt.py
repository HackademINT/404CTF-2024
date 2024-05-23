from LFSR import LFSR
from generator import CombinerGenerator
import random as rd

def xor(b1, b2):
	return bytes(a ^ b for a, b in zip(b1, b2))

#Polynomial representation
poly1 = [19,5,2,1] # x^19+x^5+x^2+x
poly2 = [19,6,2,1] # x^19+x^6+x^2+x
poly3 = [19,9,8,5] # x^19+x^9+x^8+x^5

# initialize states
state1 = [rd.randint(0,1) for _ in range(max(poly1))] 
state2 = [rd.randint(0,1) for _ in range(max(poly2))]
state3 = [rd.randint(0,1) for _ in range(max(poly3))]

#combine function
combine = lambda x1,x2,x3 : (x1 and x2)^(x1 and x3)^(x2 and x3)

#Create LFSRs
L1 = LFSR(fpoly=poly1,state=state1)
L2 = LFSR(fpoly=poly2,state=state2)
L3 = LFSR(fpoly=poly3,state=state3)

#Create (secure) generator
generator = CombinerGenerator(combine,L1,L2,L3)

#read the flag
clear_flag = None
with open("flag.png","rb") as f:
	clear_flag = f.read()

#encrypt the flag
encrypted_flag = b''
key = b""
for i in range(len(clear_flag)):
	random = generator.generateByte()
	byte = clear_flag[i:i+1]
	key+=random
	encrypted_flag += xor(byte,random)

#write encrypted flag
with open("flag.png.enc","w+b") as f:
	f.write(encrypted_flag)