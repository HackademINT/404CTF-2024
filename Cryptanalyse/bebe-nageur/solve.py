# 404CTF 2024
# Challenge : Bébé nageur, intro
# Authors : acmo0 & Little_endi4ne

encrypted = "-4-c57T5fUq9UdO0lOqiMqS4Hy0lqM4ekq-0vqwiNoqzUq5O9tyYoUq2_"
charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_-!"
n = len(charset)

y1 = charset.index(encrypted[0])
y2 = charset.index(encrypted[1])

x1 = charset.index("4")
x2 = charset.index("0")

# a*x1 + b = y1
# a*x2 + b = y2
# <=>
# a*x1 + b = y1
# a = (y2 - y1)*(x2 - x1)^(-1)

a = ((y2 - y1)%n)*pow((x2-x1)%n,-1,n)%n
b = (y1 - a*x1)%n

def f_inv(x,a,b,n):
	return ((x-b)%n)*pow(a,-1,n)%n

def decrypt(message,a,b,n):
	decrypted = ""
	for char in message:
		x = charset.index(char)
		x = f_inv(x,a,b,n)
		decrypted += charset[x]
	return decrypted
print(decrypt(encrypted,a,b,n))

# Dumb solution


for a in range(2,n-1):
	for b in range(1,n-1):
		d = decrypt(encrypted,a,b,n)
		if "404CTF" in d:
			print(d)