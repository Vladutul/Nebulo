# Clasa de bază (interfață) pentru toate funcțiile de apartenență
class MembershipFunction:
    def evaluate(self, x):
        # Forțează subclasele să implementeze propria metodă de calcul
        raise NotImplementedError

# Funcția de apartenență Triunghiulară (definită de punctele a, b, c)
class TriangularMF(MembershipFunction):
    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c

    def evaluate(self, x):
        # În afara limitelor [a, c], gradul de apartenență este 0
        if x <= self.a or x >= self.c: return 0
        # Panta ascendentă între a și b
        elif self.a < x < self.b: return (x - self.a)/(self.b - self.a)
        # Panta descendentă între b și c
        elif self.b <= x < self.c: return (self.c - x)/(self.c - self.b)
        return 0

# Funcția de apartenență Trapezoidală (definită de a, b, c, d)
class TrapezoidalMF(MembershipFunction):
    def __init__(self, a, b, c, d):
        self.a, self.b, self.c, self.d = a, b, c, d

    def evaluate(self, x):
        # În afara limitelor [a, d], gradul de apartenență este 0
        if x <= self.a or x >= self.d: return 0
        # Panta ascendentă (a -> b)
        elif self.a < x < self.b: return (x - self.a)/(self.b - self.a)
        # Platoul central unde apartenența este maximă (1)
        elif self.b <= x <= self.c: return 1
        # Panta descendentă (c -> d)
        elif self.c < x < self.d: return (self.d - x)/(self.d - self.c)
        return 0

# Funcția de apartenență Gaussiană (Clopotul lui Gauss)
class GaussianMF(MembershipFunction):
    def __init__(self, mean, sigma):
        self.mean, self.sigma = mean, sigma # media (centrul) și deviația standard

    def evaluate(self, x):
        e = 2.718281828459045 # Constanta Euler
        # Formula matematică: e ^ (-0.5 * ((x - medie) / sigma)^2)
        return e ** (-0.5 * ((x - self.mean) / self.sigma) ** 2)