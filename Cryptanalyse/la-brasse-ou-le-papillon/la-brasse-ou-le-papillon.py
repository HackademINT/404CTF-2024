from brasse import Brasse
from papillon import Papillon
import os
import zlib
import base64
import json

from flag_secret import FLAG


def send(data):
	data = json.dumps(data).encode("utf-8")
	data = zlib.compress(data, level=9)
	data = base64.b64encode(data).decode('utf-8')
	print(data)
	print("Pfiouuu c'est long !")


def receive(data):
	data = base64.b64decode(data)
	data = zlib.decompress(data)
	data = json.loads(data)
	
	plain = breaststroke.decrypt(data['plain'])

	assert len(plain) == butterfly.BLOCK_SIZE//8

	ciphertext = butterfly.encrypt(plain)

	return ciphertext

assert FLAG[:7] == b'404CTF{' and FLAG[-1:] == b'}'


key = os.urandom(16)

butterfly = Papillon(key)
breaststroke = Brasse()

plaintext = os.urandom(16)
ciphertext = breaststroke.encrypt(butterfly.encrypt(plaintext))

message = FLAG[7:-1]
encrypted_message = breaststroke.encrypt(butterfly.encrypt(message))


data = {
	"plain" : breaststroke.encrypt(plaintext),
	"encrypted" : ciphertext,
	"flag" : encrypted_message,
	"n" : breaststroke.n
}

send(data)
ciphertext = receive(input())

data = {
	"encrypted" : breaststroke.encrypt(ciphertext)
}

send(data)
exit()