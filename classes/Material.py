class Material:
    def __init__(self, dr, dg, db, sr, sg, sb, rr, rg, rb, phong, trans):
        self.diffuse = (dr, dg, db)
        self.spec = (sr, sg, sb)
        self.reflect = (rr, rg, rb)
        self.phong = phong
        self.trans = trans
