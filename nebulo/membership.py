class MembershipFunction:
    def evaluate(self, x):
        raise NotImplementedError

class TriangularMF(MembershipFunction):
    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c

    def evaluate(self, x):
        if x <= self.a or x >= self.c: return 0
        elif self.a < x < self.b: return (x - self.a)/(self.b - self.a)
        elif self.b <= x < self.c: return (self.c - x)/(self.c - self.b)
        return 0

class TrapezoidalMF(MembershipFunction):
    def __init__(self, a, b, c, d):
        self.a, self.b, self.c, self.d = a, b, c, d

    def evaluate(self, x):
        if x <= self.a or x >= self.d: return 0
        elif self.a < x < self.b: return (x - self.a)/(self.b - self.a)
        elif self.b <= x <= self.c: return 1
        elif self.c < x < self.d: return (self.d - x)/(self.d - self.c)
        return 0

class GaussianMF(MembershipFunction):
    def __init__(self, mean, sigma):
        self.mean, self.sigma = mean, sigma

    def evaluate(self, x):
        e = 2.718281828459045
        return e ** (-0.5 * ((x - self.mean) / self.sigma) ** 2)