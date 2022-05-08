import numpy as np


class Material:
    def __init__(self, dr, dg, db, sr, sg, sb, rr, rg, rb, phong, trans):
        self.diffuse = np.array((dr, dg, db))
        self.spec = np.array((sr, sg, sb))
        self.reflect = np.array((rr, rg, rb))
        self.phong = phong
        self.trans = trans
