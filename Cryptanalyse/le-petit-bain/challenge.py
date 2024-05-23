import random as rd
from flag import FLAG

assert FLAG[:12] == "404CTF{tHe_c"

charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_-!"
n = len(charset)

def f(a,b,n,x):
	return (a*x+b)%n

def permute(message):
	p = [4, 3, 0, 5, 1, 2, 10, 9, 6, 11, 7, 8, 16, 15, 12, 17, 13, 14, 22, 21, 18, 23, 19, 20, 28, 27, 24, 29, 25, 26, 34, 33, 30, 35, 31, 32, 40, 39, 36, 41, 37, 38, 46, 45, 42, 47, 43, 44]
	permuted = [ message[p[i]] for i in range(len(message))]
	return ''.join(permuted)

def round(message,A,B,n):
	encrypted = ""
	for i in range(len(message)):
		x = charset.index(message[i])
		a = A[i%6]
		b = B[i%6]
		x = f(a,b,n,x)
		encrypted += charset[x]
	return permute(encrypted)

def encrypt(message):
	encrypted = message
	for k in range(6):
		A = [ rd.randint(2,n-1) for i in range(6)]
		B = [ rd.randint(1,n-1) for i in range(6)]
		encrypted = round(encrypted,A,B,n)
	return encrypted

print(encrypt(FLAG))

# OUTPUT : C_ef8K8rT83JC8I0fOPiN6P!liE03W2NXFh1viJCROAqXb6o