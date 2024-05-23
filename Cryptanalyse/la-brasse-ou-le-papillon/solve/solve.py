from solve_sym import crack, decrypt_sym, encrypt_sym, crack2
from solve_asym import recover_poly, decrypt_asym
from papillon_solve import Papillon
from pwn import *
import zlib
import json
import base64


def encode(data):
	data = json.dumps(data).encode("utf-8")
	data = zlib.compress(data,level=9)

	data = base64.b64encode(data)

	return data

def decode(data):

	data = data.replace('\n','').replace("Pfiouuu c'est long !","")
	#print("Start",data[:100])
	#print("Stop",data[100:])
	data = base64.b64decode(data)
	#print(data)
	data = zlib.decompress(data)
	data = json.loads(data)

	return data

CORR = [4, 5]   			# 4 est un carré => déchiffré comme 0, 5 pas carré => déchiffré comme 1
PAYLOAD = [0]*128 		# Payload que va renvoyer l'oracle avant chiffrement asymétrique

##############
# Symétrique #
##############

# Remote
HOST = "challenges.404ctf.fr"
PORT = 31778
proc = remote(HOST, PORT)

# Local

#proc = process(['python3', 'la-brasse-ou-le-papillon.py'])


print("[i] Getting flag + kp")
data = proc.recvuntil(b"Pfiouuu c'est long !").decode('utf-8')
data = decode(data)

print("[i] Decoding data")
plaintext = data['plain']
ciphertext = data['encrypted']
encrypted_flag = data['flag']
n = data['n']

print("[i] Recovering key")
recovered_enc_key = crack(plaintext, ciphertext, CORR, n)

print("[i] Decrypting payload")
decrypted_payload = decrypt_sym(recovered_enc_key, PAYLOAD, CORR, n)
print(decrypted_payload)

payload = {
	"plain" : decrypted_payload
}

encoded_payload = encode(payload)

print(encoded_payload)
print("[i] Sending payload")
proc.sendline(encoded_payload)
print("[i] Decoding payload")
data = proc.recvuntil(b"Pfiouuu c'est long !").decode('utf-8')
data = decode(data)

encrypted_payload = data['encrypted']
print("[i] Début asymétrique")
#print(proc.recvuntil(b'\n').decode('utf-8'))

###############
# Asymétrique #
###############

pool = recover_poly(encrypted_payload, n)
flag = decrypt_asym(pool, encrypted_flag, n)
print("Flag",flag)
#print("Key",recovered_enc_key)
plain = decrypt_asym(pool, plaintext, n)
ciphertext = decrypt_asym(pool, ciphertext, n)
print("Recovered plain",plain)
print("Recovered ciphertext",ciphertext)
key = crack2(plain, ciphertext)
cipher = Papillon(key)
print(cipher.decrypt(flag))