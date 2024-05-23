from Cryptodome.Util.number import long_to_bytes

def decrypt(A, a_inv, n, encrypted_message):
	encrypted_message = ( a_inv * encrypted_message ) % n
	message = []
	start = False
	for a in reversed(A):
		#print(encrypted_message)
		if not start and a < encrypted_message:
			message.append(int(a <= encrypted_message))
			start = True
			encrypted_message -= message[-1] * a
			continue
		if start:
			message.append(int(a <= encrypted_message))
			encrypted_message -= message[-1] * a
			if encrypted_message == 0:
				break
	return long_to_bytes(sum([message[i]*2**i for i in range(len(message))]))

def isSuperIncreasing(L):
	s = L[0]
	for i in range(1,len(L)):
		if not L[i] > s:
			return False
		s += L[i]
	return True