import math
from collections import OrderedDict
import numpy as np
from app import utils
from app.objects import HwStep, Node
from app.graph_objects import GraphStep,GraphNode


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

    def compute2(self):
        return self.compute_value2(self.hwinput.alpha, self.hwinput.volatility, 1, self.hwinput.maturity,self.hwinput.rate,self.hwinput.period)

    def compute_value2(self,alpha, sig, dt, maturity, rates,periode):
        # precalculate constants

        N = int(maturity / dt)
        dr = sig * math.sqrt(3 * dt)
        M = -alpha * dt
        jmax = int(math.ceil(-0.1835 / M))
        if len(periode) == 0:
            periode = 'years'

        time = 1
        if periode.startswith('d'):
            time = 250
        elif periode.startswith('w'):
            time = 48
        elif periode.startswith('m'):
            time = 12
        elif periode.startswith('s'):
            time = 2
        else:
            time = 1

        N = int(N * time)
        row = N + 1
        column = 1 + jmax * 2

        # initialize yield curve

        R = []
        for j in range(0, len(rates)):
            for i in range(0, time):
                R.append(rates[j] / time)


        # P = premium
        P = []
        P.append(1)
        for i in range(1, time * len(rates) + 1):
            P.append(math.exp(-R[i - 1] * i * dt))

        # declare the matrices
        r = np.zeros((row, column))
        Q = np.zeros((row, column))
        p = [[] for y in range(row)]

        d = np.zeros((row, column))

        a = []

        # initialise first node for simplified process
        for i in range(0, time):
            Q[i][jmax] = 1
            d[i][jmax] = math.exp(-R[i] * dt)



        graph = {'(0,0)': ['(0,0)']}

        # BEGIN# calculate tree for simplified process
        for i in range(0, N + 1):

            top_node = int(min(i, jmax))

            # create rate nodes at time step i
            for j in range(-top_node, top_node + 1):
                r[i, j + jmax] = j * dr  # adding top_node will set the first postion as zero

            # calculate probabilities - first central to top nodes

            for j in range(0, top_node + 1):

                # here I define which type of branching

                if j == jmax:
                    pu = 7.0 / 6.0 + (j * j * M * M + 3 * j * M) / 2
                    pm = -1.0 / 3.0 - j * j * M * M - 2 * j * M
                    pd = 1.0 / 6.0 + (j * j * M * M + j * M) / 2

                    # branching B
                    # positive
                    actual_point = '(' + str(i) + ',' + str(j) + ')'
                    graph[actual_point] = ['(' + str(i + 1) + ',' + str(j - 2) + ')']
                    graph[actual_point].append('(' + str(i + 1) + ',' + str(j - 1) + ')')
                    graph[actual_point].append('(' + str(i + 1) + ',' + str(j) + ')')

                    # branching C
                    # negative
                    actual_point = '(' + str(i) + ',' + str(-j) + ')'
                    graph[actual_point] = ['(' + str(i + 1) + ',' + str(-j) + ')']
                    graph[actual_point].append('(' + str(i + 1) + ',' + str(-j + 1) + ')')
                    graph[actual_point].append('(' + str(i + 1) + ',' + str(-j + 2) + ')')

                # branching A
                else:
                    pu = 1.0 / 6.0 + (j * j * M * M + j * M) / 2
                    pm = 2.0 / 3.0 - (j * j * M * M)
                    pd = 1.0 / 6.0 + (j * j * M * M - j * M) / 2

                    # positive
                    actual_point = '(' + str(i) + ',' + str(j) + ')'
                    graph[actual_point] = ['(' + str(i + 1) + ',' + str(j - 1) + ')']
                    graph[actual_point].append('(' + str(i + 1) + ',' + str(j) + ')')
                    graph[actual_point].append('(' + str(i + 1) + ',' + str(j + 1) + ')')

                    # negative
                    if j != 0:
                        actual_point = '(' + str(i) + ',' + str(-j) + ')'
                        graph[actual_point] = ['(' + str(i + 1) + ',' + str(-j - 1) + ')']
                        graph[actual_point].append('(' + str(i + 1) + ',' + str(-j) + ')')
                        graph[actual_point].append('(' + str(i + 1) + ',' + str(-j + 1) + ')')

                p_temp_pos = []
                p_temp_pos.append(pd)
                p_temp_pos.append(pm)
                p_temp_pos.append(pu)

                p[i].append(p_temp_pos)

                # calculate the other probabilities by reflection
                if i > 0 and j > 0:
                    p_temp_neg = p_temp_pos[::-1]
                    p[i].insert(0, p_temp_neg)

            p[i] = p[i][::-1]

        for i in range(0, N, 1):
            top_node = int(min(i, jmax))
            hw_step = GraphStep(i)
            for j in range(-top_node, top_node + 1, 1):
                node = GraphNode(i, j, pu=utils.val(p[i][j][2]), pm=utils.val(p[i][j][1]), pd=utils.val(p[i][j][0]))
                hw_step.nodes.append(node)
            self.hwsteps.append(hw_step)

        # END# calculate tree for simplified process

        # sorting the graph nodes
        graph_sorted = []
        for k1 in graph:
            graph_sorted.append(k1)

        graph_sorted = sorted(graph_sorted)

        # at the origin of the tree a0 reduces to the simpler form
        a.append((-math.log(P[1])) / dt)

        # BEGIN# update state prices, find time-varying drift and displace nodes
        for i in range(1, N + 1):
            top_node = int(min(i, jmax))

            sum_a = 0
            sum_temp = 0

            # update pure security prices
            for j in range(-top_node, top_node + 1):

                list_connexions = []

                fixed = '(' + str(i) + ',' + str(j) + ')'


                # create rate nodes at time step i
                top_node_p = int(min(i - 1, jmax))
                for j_p in range(-top_node_p, top_node_p + 1):

                    position = '(' + str(i - 1) + ',' + str(j_p) + ')'

                    for item in graph_sorted:
                        if item == position:
                            for connect in graph[item]:
                                if connect == fixed:
                                    list_connexions.append(position)

                # by here, I have the list of nodes that connect to the actual node

                u_m_d = 0
                sum_temp = 0

                for link in list_connexions:
                    i_link = int(link[1])
                    if link[3] == '-':
                        j_link = int(link[3:5])
                    else:
                        j_link = int(link[3])

                    if j == jmax:
                        u_m_d = 0
                    elif j == -jmax:
                        u_m_d = 2
                    elif j == 0:
                        if j_link < 0:
                            u_m_d = 0
                        elif j_link > 0:
                            u_m_d = 2
                        else:
                            u_m_d = 1
                    elif j > 0 and j != jmax:
                        if (j - j_link) <= 0:
                            u_m_d = 1
                        else:
                            u_m_d = 0
                    elif j < 0 and j != -jmax:
                        if (j_link - j) <= 0:
                            u_m_d = 1
                        else:
                            u_m_d = 2

                            # by here, I know which probability I should use for each node connection




                    if i_link == 0:
                        sum_temp = sum_temp + (
                            Q[i_link][j_link + jmax] * p[i_link][j_link][u_m_d] * d[i_link][j_link + jmax])
                    else:
                        top_node_temp = int(min(i_link, jmax))


                        sum_temp = sum_temp + (
                            Q[i_link][j_link + jmax] * p[i_link][j_link + top_node_temp][u_m_d] * d[i_link][
                                j_link + jmax])



                Q[i][j + jmax] = sum_temp

            # find a[i]
            for j in range(-top_node, top_node + 1):
                sum_a = sum_a + Q[i][j + jmax] * math.exp(-j * dr * dt)

            a.append((math.log(sum_a) - math.log(P[i + 1])) / dt)

            # displace nodes to obtain r[i] and d[i]
            for j in range(-top_node, top_node + 1):
                r[i][j + jmax] = r[i][j + jmax] + a[i]
                d[i][j + jmax] = math.exp(-r[i][j + jmax] * dt)
                try:
                    self.hwsteps[i].nodes[j].rate = utils.percent(r[i][j + jmax])
                except:
                    pass

            r[0][0 + jmax] = R[0]

        return r,N,dt,jmax
