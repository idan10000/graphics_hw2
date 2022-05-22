import numpy as np

class Cube:
    def __init__(self, cx, cy, cz, length, material):
        self.center = np.array((cx, cy, cz))
        self.length = length
        self.material = material
