encrypted = "C_ef8K8rT83JC8I0fOPiN6P!liE03W2NXFh1viJCROAqXb6o"
clear = "404CTF{tHe_c"

charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_-!"
n = len(charset)

def f(a,b,n,x):
	return (a*x+b)%n

def f_inv(a,b,n,x):
	return ((x-b)%n)*pow(a,-1,n)%n


def decrypt(message):
	decrypted = ""
	for i in range(len(message)):
		x = charset.index(message[i])
		a = A[i%6]
		b = B[i%6]
		x = f_inv(a,b,n,x)
		decrypted += charset[x]
	return decrypted

A,B = [],[]

for i in range(6):
	x1 = charset.index(clear[i])
	y1 = charset.index(encrypted[i])
	x2 = charset.index(clear[i+6])
	y2 = charset.index(encrypted[i+6])
	a = ((y2 - y1)%n)*pow((x2-x1)%n,-1,n)%n
	A.append(((y2 - y1)%n)*pow((x2-x1)%n,-1,n)%n)
	B.append((y1 - a*x1)%n)


print(decrypt(encrypted))