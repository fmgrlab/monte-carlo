import math
from collections import OrderedDict
import numpy as np
from app import utils
from app.objects import HwStep, Node


class HullWhiteEngine():
    def __init__(self, hwinput):
        self.hwinput = hwinput
        self.dr = 0.0
        self.dt = 0.0
        self.jmax = 0.0
        self.N = 0.0
        self.hwsteps = []

    def as_json(self):
        dict = OrderedDict()
        dict['hwinput'] = self.hwinput.as_json()
        dict['hwsteps'] = [ob.as_json() for ob in self.hwsteps]
        return dict

    def find_connector(self, i, j):
        connected_nodes = []
        previous_step = self.hwsteps[i - 1]
        for node in previous_step.nodes:
            if node.next_up == utils.gen_id(i, j) or node.next_m == utils.gen_id(i, j) or node.next_d == utils.gen_id(i, j):
                connected_nodes.append(node)
        return connected_nodes

    def compute(self):
        return self.compute_value(self.hwinput.N, self.hwinput.maturity, self.hwinput.volatility,
                                  self.hwinput.alpha, self.hwinput.rate)

    def compute_value(self, N, maturity, sig, alpha, R):
        dt = maturity / N;
        self.dt = dt
        dr = sig * math.sqrt(3 * dt)
        self.dr= dr
        if alpha < 0.000:
            raise Exception('alpha must be non-zero')
        M = -alpha * dt
        jmax = math.ceil(-0.184 / M)
        if (jmax < 2):
            jmax = 2
        jmin = 0 - jmax
        self.jmax = jmax
        self.N= N

        P = []
        P.append(1)
        for i in range(1, N + 2, 1):
            P.append(math.exp(-R[i-1] * i * dt))

        # Create graph

        for i in range(0, N, 1):
            hw_step = HwStep(i)
            for j in range(-i, i + 1, 1):
                node = Node(i, j)
                hw_step.nodes.append(node)
            self.hwsteps.append(hw_step)

        node = self.hwsteps[0].nodes[0]
        node.q = 1

        self.r_initial = np.zeros((N, 2 + N * 2))
        for i in range(0, N, 1):
            hw_step = self.hwsteps[i]
            for j in range(-i, i + 1, 1):
                node = hw_step.nodes[j]
                self.r_initial[i][j] = utils.val(j * dr)
                #node.r_initial = utils.percent(self.r_initial[i][j])

        pu = np.zeros((N, 1 + N * 2))
        pm = np.zeros((N, 1 + N * 2))
        pd = np.zeros((N, 1 + N * 2))

        for i in range(0, N - 1, 1):
            hw_step = self.hwsteps[i]
            for j in range(-i, i + 1, 1):
                node = hw_step.nodes[j]
                if j == jmax:
                    # Branching C
                    pu[i][j] = utils.val(7.0 / 6.0 + (j * j * M * M + 3 * j * M) / 2)
                    pm[i][j] = utils.val(-1.0 / 3.0 - j * j * M * M - 2 * j * M)
                    pd[i][j] = utils.val(1.0 / 6.0 + (j * j * M * M + j * M) / 2)

                    node.next_up = utils.gen_id(i + 1, j)
                    node.next_m = utils.gen_id(i + 1, j - 1)
                    node.next_d = utils.gen_id(i + 1, j - 2)

                    node.j_up = j
                    node.j_m = j-1
                    node.j_d = j - 2

                    node.pu = pu[i][j]
                    node.pm = pm[i][j]
                    node.pd = pd[i][j]

                if j == jmin:
                    # Branching B
                    pu[i][j] = utils.val(1.0 / 6.0 + (j * j * M * M - j * M) / 2)
                    pm[i][j] = utils.val(-1.0 / 3.0 - j * j * M * M + 2 * j * M)
                    pd[i][j] = utils.val(7.0 / 6.0 + (j * j * M * M - j * M) / 2)

                    node.next_up = utils.gen_id(i + 1, j + 2)
                    node.next_m = utils.gen_id(i + 1, j + 1)
                    node.next_d = utils.gen_id(i + 1, j)

                    node.j_up = j + 2
                    node.j_m = j+1
                    node.j_d = j


                    node.pu = pu[i][j]
                    node.pm = pm[i][j]
                    node.pd = pd[i][j]

                if (j != jmin) and (j != jmax):
                    # Branching A
                    pu[i][j] = utils.val(1.0 / 6.0 + (j * j * M * M + j * M) / 2)
                    pm[i][j] = utils.val(2.0 / 3.0 - (j * j * M * M))
                    pd[i][j] = utils.val(1.0 / 6.0 + (j * j * M * M - j * M) / 2)
                    node.next_up = utils.gen_id(i + 1, j + 1)
                    node.next_m = utils.gen_id(i + 1, j)
                    node.next_d = utils.gen_id(i + 1, j - 1)

                    node.j_up = j + 1
                    node.j_m = j
                    node.j_d = j - 1

                    node.pu = pu[i][j]
                    node.pm = pm[i][j]
                    node.pd = pd[i][j]

        a = []
        a.append(0)

        for i in range(1, N, 1):
            previous_step = self.hwsteps[i - 1]
            for j in range(-i, i + 1, 1):
                node = self.hwsteps[i].nodes[j]
                for p_node in previous_step.nodes:
                    if p_node.next_up == node.id:
                        node.q += p_node.q * p_node.pu *math.exp(-a[i-1]+ p_node.j_up*dt)

                    if p_node.next_m == node.id:
                        node.q += p_node.q * p_node.pm *math.exp(-a[i-1]+ p_node.j_m*dt)

                    if p_node.next_d == node.id:
                        node.q += p_node.q * p_node.pd *math.exp(-a[i-1]+ p_node.j_d*dt)

            sum2 = 0
            for k  in range(-i, i + 1, 1):
                node = self.hwsteps[i].nodes[k]
                sum2 += + node.q * math.exp(-k*dt*dr)
            print(sum2)

            a.append((math.log(sum2) - math.log(P[i + 1])) / dt)

            for j in range(-i, -i + 1, 1):
               self.r_initial[i][j] += a[i]
               self.hwsteps[i].nodes[j].r_initial = utils.val(self.r_initial[i][j])


        return 0
