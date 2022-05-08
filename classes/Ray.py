class Ray:
    def __init__(self, p, v):
        self.p = p
        self.v = v

    def getPoint(self, t):
        return self.p + t * self.v
