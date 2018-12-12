from collections import OrderedDict
import numpy as np
import math


class GraphStep:
    def __init__(self, i):
        self.i = i
        self.nodes = []

    def as_json(self):
        dict = OrderedDict()
        dict['i'] = self.i
        dict['nodes'] = [ob.as_json() for ob in self.nodes]
        return dict


class GraphNode:
    def __init__(self, i=0, j = 0, pu ="", pm="", pd="", rate = 0, j_up = 0, j_m =0,j_d = 0):
        self.id = str(i)+","+str(j)
        self.i = i
        self.j = j
        self.rate = rate
        self.j_up = j_up
        self.j_m = j_m
        self.j_d = j_d
        self.pu = pu
        self.pd = pd
        self.pm = pd
       

    def as_json(self):
        dict = OrderedDict()
        dict['i'] = self.i
        dict['j'] = self.j
        dict['rate'] = str(self.rate) + "%"
        dict['j_up'] = self.j_up
        dict['j_m'] = self.j_m
        dict['j_d'] = self.j_d
        dict['pu'] = self.pu
        dict['pm'] = self.pm
        dict['pd'] = self.pd
        return dict


class HWCalculator:
    def __init__(self):
        self.steps = []
        self.jmax = 0

    def as_json(self):
        dict = OrderedDict()
        dict['steps'] = [ob.as_json() for ob in self.steps]
        return dict

    def execute(self, sig, alpha, maturity, dt):
        return self.process(sig, alpha, maturity, dt)

    def process(self, sig, alpha, maturity, dt):
        #Init parameter

        N = int(maturity/dt)
        M = -alpha * dt
        dr = sig * math.sqrt(3 * dt)
        jmax = int(math.ceil(-0.1835 / M))
        jmin = -jmax
        self.jmax = jmax
        
        #Create empty graph

        self.steps = self.create_graph(N, jmax)

        #Calculate probability

        self.init_standard_move(N,jmax,self.steps,dr)

        self.compute_transition_probability(N,jmax, jmin, M, self.steps)

        return  0

    def create_graph(self, N,jmax):
        hwsteps = []
        for i in range(0, N, 1):
            top_node = min(i,jmax)
            current_step = GraphStep(i)
            for j in range(-top_node, top_node + 1, 1):
                node = GraphNode(i, j)
                current_step.nodes.insert(j+top_node,node)
            hwsteps.insert(i,current_step)
        return hwsteps

    def init_standard_move(self, N, jmax, hw_steps, dr):
        for i in range(0, N, 1):
            top_node = min(i, jmax)
            for j in range(-top_node, top_node + 1, 1):
                hw_steps[i].nodes[j + top_node].rate = j * dr

    def compute_transition_probability(self,N,jmax, jmin, M, hw_steps):

        for i in range(0, N, 1):
            top_node = min(i, jmax)
            for j in range(-top_node, top_node + 1, 1):
                node = hw_steps[i].nodes[j+top_node]
                if j == jmax:
                    # Branching C
                    node.pu =  7.0 / 6.0 + (j * j * M * M + 3 * j * M) / 2
                    node.pm =  -1.0 / 3.0 - j * j * M * M - 2 * j * M
                    node.pd =  1.0 / 6.0 + (j * j * M * M + j * M) / 2

                    node.j_up = j
                    node.j_m = j -1
                    node.j_d = j - 2

                if j == jmin:
                    # Branching B
                    node.pu =  1.0 / 6.0 + (j * j * M * M - j * M) / 2
                    node.pm =  -1.0 / 3.0 - j * j * M * M + 2 * j * M
                    node.pd =  7.0 / 6.0 + (j * j * M * M - j * M) / 2

                    node.j_up = j + 2
                    node.j_m = j+1
                    node.j_d = j

                if (j != jmin) and (j != jmax):
                    # Branching A
                    node.pu =  1.0 / 6.0 + (j * j * M * M + j * M) / 2
                    node.pm =  2.0 / 3.0 - (j * j * M * M)
                    node.pd =  1.0 / 6.0 + (j * j * M * M - j * M) / 2
                    node.j_up = j + 1
                    node.j_m = j
                    node.j_d = j - 1
