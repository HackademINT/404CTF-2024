from sage.all import *
from Cryptodome.Util.number import long_to_bytes
from itertools import product

def recover_poly(c, n):
    pts = enumerate(c)

    K = Zmod(n)
    F1 = PolynomialRing(QQ, "q")
    q = F1.gen()
    F2 = PolynomialRing(K, "x", implementation='NTL')
    x = F2.gen()

    return F1.lagrange_polynomial(pts).change_ring(F2)(q=x)

pgcd = lambda g1, g2: g1.monic() if not g2 else pgcd(g2, g1 % g2)

def cf(A, B):
    g = pgcd(A, B)
    if g != 1 and g.degree() == 1:
        return -list(g)[0]
    return 0

#from tqdm import tqdm
def decrypt_asym(poly, enc, n):
    x = parent(poly).gen()
    K = Zmod(n)

    diff = 0
    while not diff:
        i2 = randrange(0, len(enc))
        i1 = randrange(0, len(enc))
        P1 = poly(x=x + i1) - enc[i1]
        P2 = poly(x=x + i2) - enc[i2]

        diff = cf(P1, P2)

    assert diff != 0
    
    P = poly(x=x + diff)


    o = [K(k) / P(x=i) for i, k in enumerate(enc)]
    rec = long_to_bytes(int("".join(["1" if k != 1 else "0" for k in o])[::-1], 2))

    return rec