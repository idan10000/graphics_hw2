import numpy as np


class Light:
    def __init__(self, px, py ,pz, r, g, b, spec, shadow, width):
        self.point = np.array((px, py ,pz))
        self.color = np.array((r,g,b))
        self.spec = spec
        self.shadow = shadow
        self.width = width