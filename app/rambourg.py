import math
import numpy as np
from app.models import Node

class rambourg():
    def __init__(self,maturity,volatility,ro, R,alpha):
        self.volatility = volatility
        self.alpha = alpha
        self.maturity = maturity
        self.dt = 1

    def calculate(self):


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
