from sage.all import *
from pwn import *
import math
import json
import zlib
import base64
from Cryptodome.Util.number import long_to_bytes

def matrix_overview(BB):
  print()
  for ii in range(BB.dimensions()[0]):
    a = ('%02d ' % ii)
    for jj in range(BB.dimensions()[1]):
      if BB[ii,jj] == 0:
        a += '0' 
      elif BB[ii,jj] == 1:
        a += '1'
      else:
        a += 'X'
      if BB.dimensions()[0] < 60:
        a += ' '
    print(a)

#proc = process(['python3', 'challenge.py'])
proc = remote("challenges.404ctf.fr",31777)
_ = proc.recvuntil(b"\n")
data = json.loads(zlib.decompress(base64.b64decode(proc.recvuntil(b"\n"))))
print("[i] Finish receiving data")
c = data['encrypted']
P = Matrix(ZZ,data['public_key']).transpose()

I = Matrix.identity(ZZ,len(data['public_key']))
O = Matrix(ZZ,[0]*len(data['public_key']))
C = Matrix(ZZ,[-c])

M = block_matrix([[I,P],[O,C]])
M_reduced = M.LLL()
print(M_reduced[0])
message = M_reduced[0][::-1][3:]
print(long_to_bytes(sum([message[i]*2**i for i in range(len(message))])).decode())