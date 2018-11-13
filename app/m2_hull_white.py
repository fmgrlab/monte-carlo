import math
import numpy as np
from app.models import Node

class HullWhite2():
    def __init__(self,maturity,volatility,alpha, step):
        self.volatility = volatility
        self.alpha = alpha
        self.maturity = maturity
        self.step = step
        self.dt = maturity/step
        self.M = (math.exp(-self.alpha*self.dt)-1)
        self.V = self.volatility * self.volatility *  (1- math.exp(-2*self.alpha))/(2*self.alpha)
        self.dr = math.sqrt(3*self.V)
        self.jmax = math.ceil(0.184/self.M)
        self.jmin = -self.jmax
        self.nodes = self.calculatePu()

    def calculatePu(self):
        nodes = list()
        for j in range(2,-3,-1):
            rate= j*self.dr
            pu,pm,pd = self.computePu(j,self.M)
            node = Node(j=j,r=rate,Pu=pu,Pm=pm,Pd=pd)
            nodes.append(node)
        return nodes

    def computePu(self, j,M):
        pu = 1.0 / 6.0 + (j ** 2 * M ** 2 + j * M) / 2
        pm = 2.0 / 3.0 - (j ** 2 * M ** 2)
        pd = 1.0 / 6.0 + (j ** 2 * M ** 2 - j * M) / 2
        if j == 2:
           pu =  7.0/6.0 + (j**2 * M**2 + 3*j*M)/2
           pm = -1.0 / 3.0 - (j ** 2 * M ** 2) - (2 * j * M)
           pd = 1.0 / 6.0 + (j ** 2 * M ** 2 +   j * M) / 2
        if j == -2:
           pu = 1.0 / 6.0 + (j ** 2 * M ** 2 - j * M) / 2
           pm = -1.0 / 3.0 - (j ** 2 * M ** 2) + (2 * j * M)
           pd =  7.0/6.0 + (j**2 * M**2 - 3*j*M)/2
        return pu,pm,pd

    def as_json(self):
        return dict(
            node=[ob.as_json() for ob in self.nodes],
            volatility=self.volatility,
            alpha=self.alpha,
            step = self.step,
            maturity=self.maturity
        )
