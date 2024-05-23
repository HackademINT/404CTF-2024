from LFSR import LFSR
from generator import CombinerGenerator
import itertools
import random as rd
from multiprocessing import Pool
from functools import partial

def xor(b1, b2):
	return bytes(a ^ b for a, b in zip(b1, b2))

def stat(seq1,seq2):
	"""
	Corrélation entre seq1 et seq2
	"""
	assert len(seq1) == len(seq2)
	tot = 0
	for s1,s2 in zip(seq1,seq2):
		tot += int(s1==s2)
	return tot/len(seq1)

def test(key,found):
	for p,guess in found:
		if guess == key:
			return True, found.index((p,guess))
	return False

def verify(polys, states, generated):

	L1 = LFSR(fpoly=polys[0],state=states[0])
	L2 = LFSR(fpoly=polys[1],state=states[1])
	L3 = LFSR(fpoly=polys[2],state=states[2])

	gen = CombinerGenerator(combine,L1,L2,L3)

	output_guess = [gen.generateBit() for i in range(CLEAR_LENGTH)]
	return output_guess == generated


# Les poly utilisés dans le challenge
poly1 = [19,5,2,1]
poly2 = [19,6,2,1]
poly3 = [19,9,8,5]

CLEAR_LENGTH=2**8
EPSILON = 0.05	# Seuil maximal d'écart de corrélation accepté entre la valeur théorique
				# et celle observée lors du BF

combine = lambda x1,x2,x3 : (x1 and x2)^(x1 and x3)^(x2 and x3)

states_len = [19,19,19]	# taille des états de chaque LFSR
polys = [poly1,poly2,poly3]
probas = [0.75,0.75,0.75]	# corrélation entre chaque LFSR et la fonction de combinaison

clear_partial = None
with open("flag.png.part",'rb') as f:
	clear_partial = f.read()[:CLEAR_LENGTH//8]

encryted = None
with open("flag.png.enc",'rb') as f:
	encrypted = f.read()

key = xor(clear_partial,encrypted[:CLEAR_LENGTH//8])	# flot généré par le challenge


output = []
for byte in key:	# moyen pas joli de convertir des octets en binaire
	binary = bin(byte)[2:]
	binary = (8-len(binary))*'0' + binary
	for b in binary:
		output.append(int(b))


def crack_lfsr(epsilon, length,  proba,fpoly):

	guess_state = [0 for _ in range(length)]		# intilise l'état pour un BF
	L_guess = LFSR(fpoly=fpoly,state=guess_state)	# Initialise le LFSR
	results = []
	tot = 2**length  								# nombre d'états potentiels
	i=0
	for guess_state in itertools.product([0,1],repeat=length):	# parcours tous les états potentiels
		L_guess.state=list(guess_state)							# initialise le LFSR avec l'état potentiel
		out_guess = [L_guess.generateBit() for i in range(CLEAR_LENGTH)]	# génère le flot de sortie du LFSR
		prob = stat(out_guess,output)							# corrélation entre le flot du challenge et du LFSR qu'on BF
		
		if (proba-epsilon)<prob<(proba+epsilon):				# Si la proba est suffisament proche (à un seuil epsilon qu'on choisi)
			results.append((prob,guess_state))

		i+=1
		print(round(i/tot*100,2),"%",end="\r")		# pour faire joli
	results.sort(reverse=True)
	return results

print("Cracking LFSRs")

pool = Pool()	# pour faire du multithreading
map_function = partial(crack_lfsr,EPSILON,max(states_len),0.75)

results = []
for result in pool.map(map_function,polys):	# lance un thread par LFSR
	results.append(result)					# stocke les états potentiels

results1,results2,results3 = results

for p1,s1 in results1:
	for p2,s2 in results2:
		for p3,s3 in results3:
			
			if verify(polys,(list(s1),list(s2),list(s3)),output):
				print("Find matching output",s1,s2,s3)

				L1 = LFSR(fpoly=poly1,state=list(s1))
				L2 = LFSR(fpoly=poly2,state=list(s2))
				L3 = LFSR(fpoly=poly3,state=list(s3))

				gen = CombinerGenerator(combine,L1,L2,L3)

				clear = b''.join([xor(encrypted[i:i+1],gen.generateByte()) for i in range(len(encrypted))])	# déchiffre le fichier chiffré

				with open("decrypted.png","w+b") as f:
					f.write(clear)
				exit()