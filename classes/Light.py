class Light:
    def __init__(self, px, py ,pz, r, g, b, spec, shadow, width):
        self.point = (px, py ,pz)
        self.r = r
        self.g = g
        self.b = b
        self.spec = spec
        self.shadow = shadow
        self.width = width