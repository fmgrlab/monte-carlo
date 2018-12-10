import math

import numpy as np


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
        rates = []
        rates.append(0.10)
        rates.append(0.105)
        rates.append(0.11)
        rates.append(0.1125)
        rates.append(0.115)
        rates.append(0.125)
        rates.append(0.130)
        return self.compute_value(1, 3, 0.014, 0.1, rates)

    def compute_value(self, dt, maturity, sig, alpha, R):

        # Pre-calculate constants

        N = int(maturity / dt)
        dr = sig * math.sqrt(3 * dt)
        M = -alpha * dt
        jmax = math.ceil(-1.835 / M)

        self.x = np.zeros((N, 1 + N * 2))

        # Initialize yield curve

        P = []
        for i in range(0, N + 1, 1):
            P.append(math.exp(-R[i] * i * dt))

        # Initialise first node for simplified process
        self.r = np.zeros((N, 1 + N * 2))
        Q = np.zeros((N, 1 + N * 2))
        d = np.zeros((N, N * 2))

        d[0][0] = math.exp(-R[1] * dt)

        self.r[0][0] = 0
        Q[0][0] = 1
        a = []

        # Calculate tree for simplified process

        for i in range(0, N, 1):
            for j in range(-i, i + 1, 1):
                self.r[i][j] = j * dr

        # Calculate the probabilities of transition first central to top nodes
        pu = np.zeros((N, N * 2))
        pm = np.zeros((N, N * 2))
        pd = np.zeros((N, N * 2))

        for i in range(0, N, 1):
            top_node = min(i, jmax)
            for j in range(0, top_node + 1, 1):
                if j == jmax:
                    pu[i][j] = 7.0 / 6.0 + (j * j * M * M - 3 * j * M) / 2
                    pm[i][j] = -1.0 / 3.0 - (j * j * M * M - 2 * j * M)
                    pd[i][j] = 1.0 - (pm[i][j] + pu[i][j])
                else:
                    pu[i][j] = 1.0 / 6.0 + (j * j * M * M + j * M) / 2
                    pm[i][j] = 2.0 / 3.0 - (j * j * M * M)
                    pd[i][j] = 1.0 - (pm[i][j] + pu[i][j])

        # Calculate the other probability by reflection
        for i in range(0, N, 1):
            top_node = min(i, jmax)
            for j in range(0, top_node, 1):
                pu[i][j] = pd[i][-j]
                pm[i][j] = pm[i][-j]
                pd[i][j] = pu[i][-j]

        # Update state prices, find time-varying drift and displace nodes


        for i in range(1, N, 1):
            top_node = min(i, jmax)
            step_i = self.steps[i]
            sum = 0
            # Update pure security prices
            for j in range(-top_node, top_node + 1, 1):
                Q[i][j] = Q[i - 1][j + 1] * pu[i][j + 1] * d[i - 1][j + 1] + Q[i - 1][j] * pm[i][j] * d[i - 1][j] + \
                          Q[i - 1][j - 1] * pd[i][j - 1] * d[i - 1][j + 1]
                sum += Q[i][j] * math.exp(-j * dt * dr)
            a.append((math.log(sum) - math.log(P[i + 1])) / dt)

            sum = 0
            for j in range(-top_node, top_node + 1, 1):
                sum += Q[i][j] * math.exp(-j * dt * dr)
            a.append((math.log(sum) - math.log(P[i + 1])) / dt)

            for j in range(-top_node, top_node + 1, 1):
                self.r[i][j] += a[i]
                d[i][j] = math.exp(-self.r[i][j] * dt)
                step_i.nodes[j].r = self.r[i][j]
