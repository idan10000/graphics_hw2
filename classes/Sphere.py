import numpy as np

class Sphere:
    def __init__(self, cx, cy, cz, radius, material):
        self.center = np.array((cx, cy, cz))
        self.radius = radius
        self.material = material
