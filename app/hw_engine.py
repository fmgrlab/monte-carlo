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

    def compute2(self):
        return self.compute_value2(self.hwinput.alpha, self.hwinput.volatility, 1, self.hwinput.maturity,
                                   self.hwinput.rate)

    def compute_value2(self,alpha, sig, dt, maturity, R):
        # precalculate constants
        N = int(maturity / dt)
        dr = sig * math.sqrt(3 * dt)
        M = -alpha * dt
        jmax = int(math.ceil(-0.1835 / M))

        row = N + 1
        column = 1 + jmax * 2

        # initialize yield curve

        # P = premium
        P = []
        P.append(1)
        for i in range(1, len(R) + 1):
            P.append(math.exp(-R[i - 1] * i * dt))
        print(P)

        # declare the matrices
        r = np.zeros((row, column))
        Q = np.zeros((row, column))
        p = [[] for y in range(row)]

        d = np.zeros((row, column))

        a = []

        # initialise first node for simplified process
        Q[0][jmax] = 1
        d[0][jmax] = math.exp(-R[0] * dt)

        # print(Q)

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
                print("i: %d, j: %d" % (i, j))

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

                    # print("i_link: %d" % i_link)
                    # print("j_link: %d" % j_link)
                    # print("u_m_d: %d" % u_m_d)

                    print("i_link: %d, j_link: %d" % (i_link, j_link))

                    if i_link == 0:
                        # print(Q[i_link][j_link+jmax])
                        # print(p[i_link][j_link][u_m_d])
                        # print(d[i_link][j_link+jmax])

                        sum_temp = sum_temp + (
                            Q[i_link][j_link + jmax] * p[i_link][j_link][u_m_d] * d[i_link][j_link + jmax])
                    else:
                        top_node_temp = int(min(i_link, jmax))
                        # print(Q[i_link][j_link+jmax])
                        # print(p[i_link][j_link+top_node_temp][u_m_d])
                        # print(d[i_link][j_link+jmax])

                        sum_temp = sum_temp + (
                            Q[i_link][j_link + jmax] * p[i_link][j_link + top_node_temp][u_m_d] * d[i_link][
                                j_link + jmax])

                        # print(sum_temp)

                Q[i][j + jmax] = sum_temp

            # find a[i]
            for j in range(-top_node, top_node + 1):
                sum_a = sum_a + Q[i][j + jmax] * math.exp(-j * dr * dt)

            a.append((math.log(sum_a) - math.log(P[i + 1])) / dt)

            # displace nodes to obtain r[i] and d[i]
            for j in range(-top_node, top_node + 1):
                r[i][j + jmax] = r[i][j + jmax] + a[i]

                d[i][j + jmax] = math.exp(-r[i][j + jmax] * dt)

            r[0][0 + jmax] = R[0]
        # PRINT PROBABILITIES
        # for element in p:
        #    for vec in element:
        #        print(vec)
        #    print(len(element))

        # PRINT GRAPH
        # l_ = []
        # for k1 in graph:
        #    l_.append(k1)

        # l_ = sorted(l_)

        # for item in l_:
        #    print(item)
        #    print(graph[item])

        for element in Q:
            print(element)

        for element in r:
            print(element)

        return graph, r

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
        for i in range(1, len(R) + 1):
            P.append(math.exp(-R[i - 1] * i * dt))

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
