import numpy as np


class Settings:
    def __init__(self, bgr, bgg, bgb, sh_rays, rec_max):
        self.background_color = np.array((bgr, bgg, bgb))
        self.sh_rays = sh_rays
        self.rec_max = rec_max
