import math
from app.models import Node,Step
import  numpy as np

class HullWhiteEngine():
    def __init__(self,hwinput):
        self.hwinput = hwinput
        self.steps = list()


    def as_json(self):
        return dict(
            input = self.hwinput.as_json(),
            steps=[ob.as_json() for ob in self.steps]
        )

    def compute(self):
        dt = 1
        N = 5
        sig = 0.014
        alpha = 0.01
        ro = 0.1
        dr = sig *sig* math.sqrt(3 * dt)
        theta = np.zeros(N)
        theta[0] = alpha*10
        for i in range(0, N, 1):
            step = Step(i)
            for j in range(-i,i+1,1):
                node = Node()
                node.i = i
                node.j = j
                rj = ro+j*dr
                mu = (theta[i] - alpha* rj)*dt
                E = mu + j*dr
                ref,k = decide_branchin(E,10,dr,j)
                eta = mu + (j-k)*dr
                node.Pu =(sig*sig*dt+eta*eta)/(2*dr*dr)+eta/(2*dr)
                node.Pm = 1 - (sig * sig * dt + eta * eta) / (dr * dr)
                node.Pd = 1 - node.Pm - node.Pu
                step.nodes.append(node)
            step.theta.append(12)
            self.steps.append(step)
        return self.steps

def decide_branchin(esperance,rj,dr,j):
        left = math.fabs(esperance - rj)
        right = math.fabs(esperance - (rj+dr))
        diff = left < right
        if math.fabs(diff) < 0.001:
            return rj,j
        if diff < rj:
            return rj,j-1,
        return rj, j+1