import numpy  as np
import  math
class Brownian:

    def brownien(self, time):
        return np.random.normal(0,1.0)*math.sqrt(time)