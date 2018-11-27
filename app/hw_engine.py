import math
from app.models import Node,Step
import  numpy as np

class HullWhiteEngine():
    def __init__(self,hwinput):
        self.hwinput = hwinput
        self.steps = list()
        self.Q = np.zeros((20,40))


    def as_json(self):
        return dict(
            input = self.hwinput.as_json(),
            steps=[ob.as_json() for ob in self.steps]
        )

    def compute(self):
        rates = list()
        rates.append(0.10)
        rates.append(0.105)
        rates.append(0.11)
        rates.append(0.1125)
        rates.append(0.115)
        return self.computeParam(1,3,0.014,0.1,rates)


    def computeParam(self,dt,N,sig,alpha,rate):
        R = rate
        dr = sig * math.sqrt(3 * dt)
        r,d = init_data(N,dt,R[0],dr)
        self.Q[0][0] = 1
        theta = np.zeros(N)
        mu = np.zeros((N, N * 2))
        theta[0] = 0.0201
        theta[1] = 0.02126
        theta[2] = 0.02236
        for i in range(0, N, 1):
            step = Step(i)
            for j in range(-i,i+1,1):
                node = Node()
                node.i = i
                node.j = j
                mu[i][j] = (theta[i] - alpha * r[i][j])*dt
                k = decide_branchin(r,mu,i,j)
                eta = mu[i][j] + (j-k)*dr
                node.Pu =(sig*sig*dt+eta*eta)/(2*dr*dr)+ eta/(2*dr)
                node.Pm = 1 - (sig * sig * dt + eta * eta) / (dr * dr)
                node.Pd = 1 - (node.Pm + node.Pu)
                step.nodes.append(node)
            self.steps.append(step)
            #  sum = calculate_sum(i,r[i][j],dt,alpha)
            # theta[i+1] = (i+3)*R[i+3]/dt+ sig*sig*dt/2 + (1/dt)*math.log(sum)
        return self.steps


def decide_branchin(r,mu,i,j):
        diff = r[i][j] - mu[i][j]
        if math.fabs(diff) < 0.002:
            return j
        if diff > r[i][j]:
            return j-1
        return j+1


def calculate_qui(self,Pu,Pm,Pd, i,j, d):
    return  self.Q[i-1][1]*Pu*d[i-1][1]+ self.Q[i-1][0]*Pm*d[i-1][0]+ self.Q[i-1][-1]*Pd*d[i-1][-1]


def calculate_sum(self,i,r,dt,alpha):
    sum = 0
    for j in range(-i, i + 1, 1):
        sum +=  self.Q[i][j]*math.exp(-2*r[i][j]*dt + alpha*r[i][j]*dt*dt)
    return sum


def init_data(N,dt,ro,dr):
    r = np.zeros((N, N*2))
    d = np.zeros((N, N*2))
    for i in range(0, N, 1):
        for j in range(-i, i + 1, 1):
            r[i][j] = ro+j*dr
            d[i][j] = math.exp(-r[i][j]*dt)
    return r,d