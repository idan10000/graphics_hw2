class Plane:
    def __init__(self, nx, ny, nz, offset, material):
        self.normal = (nx, ny, nz)
        self.offset = offset
        self.material = material
