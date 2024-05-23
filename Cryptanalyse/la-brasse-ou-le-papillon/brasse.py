from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes, getRandomRange, inverse

SIZE = 1024
DEG = 64
COEFFS = 512

class Brasse:
    def legendre(self, a, r):
        return pow(a, (r - 1) // 2, r)

    def __init__(self):
        self.p = getPrime(SIZE)
        self.q = getPrime(SIZE)
        self.n = self.p * self.q

        self.t = getRandomRange(0, self.n)
        self.pool = [getRandomRange(0, 1 << COEFFS) for _ in range(DEG)]
        
    def getWater(self):
        water = getRandomRange(0, self.n)
        while (self.legendre(water, self.p) != self.p - 1 
               or self.legendre(water, self.q) != self.q - 1):
            water = getRandomRange(0, self.n)
        return water
    
    def dive(self, a):
        return sum([pow(a, i, self.n) * k for i, k in enumerate(self.pool)]) % self.n

    def encrypt(self, a):
        m = bytes_to_long(a)
        c = []

        y = getRandomRange(0, self.n)
        for i in range(len(a) * 8):
            z = self.getWater() if m & 1 else 1
            s = self.dive(y + i)
            c.append(s**2 * z % self.n)

            m >>= 1

        return c 
    
    def decrypt(self, c):
        m = 0
        for b in c[::-1]:
            m <<= 1
            if self.legendre(b, self.p) != 1 or self.legendre(b, self.q) != 1:
                m += 1
        return long_to_bytes(m)