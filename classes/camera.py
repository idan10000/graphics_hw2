class Camera:
    def __init__(self, px, py, pz, lx, ly, lz, ux, uy, uz, sc_dist, sc_width):
        self.p = (px, py, pz)
        self.l = (lx, ly, lz)
        self.u = (ux, uy, uz)
        self.sc_dist = sc_dist
        self.sc_width = sc_width
