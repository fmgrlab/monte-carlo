import math
from collections import OrderedDict
import numpy as np
from app.objects import HwStep,Node

class HullWhiteEngine():
    def __init__(self, hwinput):
        self.hwinput = hwinput
        self.hwsteps = []

    def as_json(self):
        dict = OrderedDict()
        dict['hwinput'] = self.hwinput.as_json()
        dict['hwsteps'] = [ob.as_json() for ob in self.hwsteps]
        return dict

    def compute(self):
        return  self.compute_value(self.hwinput.N, self.hwinput.maturity, self.hwinput.volatility,
                                  self.hwinput.alpha, self.hwinput.rate)

    def compute_value(self,N,  maturity, sig, alpha, R):
        dt = maturity/N;
        dr = sig * math.sqrt(3*dt)
        if alpha < 0.000:
            raise Exception('alpha must be non-zero')
        M = -alpha * dt
        jmax = math.ceil(-1.835 / M)
        if(jmax < 2):
            jmax = 2
        jmin = 0 - jmax

        P = []
        for i in range(0, N + 1, 1):
            P.append(math.exp(-R[i] * i * dt))

        pu = np.zeros((N, 1+N * 2))
        pm = np.zeros((N, 1+N * 2))
        pd = np.zeros((N, 1+N * 2))

        #Create graph

        for i in range(0, N,1):
            hw_step = HwStep(i)
            for j in range(-i,i+1,1):
                node = Node(i,j)
                hw_step.nodes.append(node)
            self.hwsteps.append(hw_step)

        for i in range(0, N-1,1):
            hw_step = self.hwsteps[i]
            for j in range(-i,i+1,1):
                node = hw_step.nodes[j]
                if j == jmax:
                    # Branching C
                    pu[i][j] = 7.0 / 6.0 + (j * j * M * M + 3 * j * M) / 2
                    pm[i][j] = -1.0 / 3.0 - j * j * M * M - 2 * j * M
                    pd[i][j] = 1.0 / 6.0 + (j * j * M * M + j * M) / 2

                    node.next_up = j
                    node.next_m = j-1
                    node.next_d = j-2

                    node.pu = pu[i][j]
                    node.pm = pm[i][j]
                    node.pd = pd[i][j]

                if j == jmin:
                    # Branching B
                    pu[i][j] = 1.0 / 6.0 + (j * j * M * M - j * M) / 2
                    pm[i][j] = -1.0 / 3.0 - j * j * M * M + 2 * j * M
                    pd[i][j] = 7.0 / 6.0 + (j * j * M * M - j * M) / 2

                    node.next_up = j + 2
                    node.next_m = j+1
                    node.next_d = j

                    node.pu = pu[i][j]
                    node.pm = pm[i][j]
                    node.pd = pd[i][j]

                if (j != jmin) and (j != jmax):
                    # Branching A
                    pu[i][j] = 1.0 / 6.0 + (j * j * M * M + j * M) / 2
                    pm[i][j] = 2.0 / 3.0 - (j * j * M * M)
                    pd[i][j] = 1.0 / 6.0 + (j * j * M * M - j * M) / 2
                    node.next_up = j+1
                    node.next_m = j
                    node.next_d = j-1

                    node.pu = pu[i][j]
                    node.pm = pm[i][j]
                    node.pd = pd[i][j]

        return self.hwinput


