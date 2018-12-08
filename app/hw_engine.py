import math

import numpy as np

from app.objects import Step,Node


class HullWhiteEngine():
    def __init__(self, hwinput):
        self.hwinput = hwinput
        self.steps = list()
        self.r = None


    def as_json(self):
        return dict(
            input=self.hwinput.as_json(),
            steps=[ob.as_json() for ob in self.steps]
        )

    def compute(self):
        rates = list()
        rates.append(0.10)
        rates.append(0.105)
        rates.append(0.11)
        rates.append(0.1125)
        rates.append(0.115)
        rates.append(0.125)
        rates.append(0.130)
        rates.append(0.115)
        rates.append(0.125)
        rates.append(0.130)
        rates.append(0.115)
        rates.append(0.125)
        rates.append(0.130)
        return self.compute_value(1, 10, 0.014, 0.1, rates)

    def compute_value(self, dt, maturity, sig, alpha, R):

        # Pre-calculate constants

        N = int(maturity / dt)
        dr = sig * math.sqrt(3 * dt)
        M = -alpha * dt
        jmax = math.ceil(-1.835 / M)

        self.r = np.zeros((N, 1 + N * 2))

        # Calculate tree for simplified process

        for i in range(0, N, 1):
            node = min(i, 2)
            for j in range(-node, node + 1, 1):
                self.r[i][j] = j * dr