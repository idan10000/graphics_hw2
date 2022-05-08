import numpy as np


class Camera:
    def __init__(self, px, py, pz, lx, ly, lz, ux, uy, uz, sc_dist, sc_width):
        self.p = np.array((px, py, pz))
        self.look_at = np.array((lx, ly, lz))
        self.u = np.array((ux, uy, uz))
        self.sc_dist = sc_dist
        self.sc_width = sc_width
