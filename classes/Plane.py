import numpy as np


class Plane:
    def __init__(self, nx, ny, nz, offset, material):
        self.normal = np.array((nx, ny, nz))
        self.offset = offset
        self.material = material
