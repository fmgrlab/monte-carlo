import math
import numpy as np

class HullWhite():
    def __init__(self,maturity,sigma,alpha, step):
        self.sigma = sigma
        self.alpha = alpha
        self.maturity = maturity
        self.step = step
        self.dt = self.maturity/self.step
        self.variance = self.sigma * self.sigma * self.dt
        self.dx = self.sigma * math.sqrt(3 * self.dt)
        self.mean = -self.alpha * self.dt
        self.jmax = 2
        if self.jmax < 2:
           self.jmax = 3
        self.dim = min(3 + 2 * (self.step-2), 1 + 2 * self.jmax)
        self.x = np.zeros((self.step+2, self.dim+1))
        self.Pm = np.zeros((self.step+2,self.dim+1))
        self.Pu = np.zeros((self.step+2,self.dim+1))
        self.Pd = np.zeros((self.step+2,self.dim+1))



    def init_data(self):
        for i in range(1,self.step+2):
            nodes = min(3 + 2 * (i - 2), 1 + 2 * self.jmax)

            if 3 + 2 * (i + 1 - 2) <= 1 + 2 * self.jmax:
                for j in range(1,nodes+1):
                     self.x[i, j] = ((nodes+1) / 2 - j) * self.dx
                     self.Pu[i, j] = 1 / 6 + math.pow(((nodes + 1) / 2 - j) , 2) * (math.pow(self.mean,2))/ 2 + ((nodes + 1) / 2 - j) * (self.mean / 2)
                     self.Pm[i, j] = 2 / 3 - math.pow(((nodes + 1) / 2 - j) , 2) * math.pow(self.mean,2)
                     self.Pd[i, j] = 1 / 6 + math.pow(((nodes + 1) / 2 - j) , 2) * math.pow(self.mean,2 )/ 2 - ((nodes + 1) / 2 - j) * self.mean / 2
            else:
                self.x[i, 1] = ((nodes+1) / 2 - 1) * self.dx
                self.Pu[i, 1] = 7 / 6 + math.pow(((nodes + 1) / 2 - 1), 2) *  math.pow(self.mean,2 ) / 2 + 3 * ((nodes + 1) / 2 - 1) * self.mean / 2
                self.Pm[i, 1] = -1 / 3 - math.pow(((nodes + 1) / 2 - 1), 2) *  math.pow(self.mean,2 ) - 2 * ((nodes + 1) / 2 - 1) * self.mean
                self.Pd[i, 1] = 1 / 6 + math.pow(((nodes + 1) / 2 - 1), 2) *  math.pow(self.mean,2 )/ 2 + ((nodes + 1) / 2 - 1) * self.mean / 2
                self.x[i, nodes] = ((nodes+1) / 2 - nodes) * self.dx
                self.Pu[i, nodes] = 1 / 6 + math.pow(((nodes + 1) / 2 - nodes), 2) *  math.pow(self.mean,2 ) / 2 - ((nodes + 1) / 2 - nodes) * self.mean / 2
                self.Pm[i, nodes] = -1 / 3 - math.pow(((nodes + 1) / 2 - nodes), 2) *  math.pow(self.mean,2 ) + 2 * ((nodes + 1) / 2 - nodes) * self.mean
                self.Pd[i, nodes] = 7 / 6 + math.pow(((nodes + 1) / 2 - nodes), 2) *  math.pow(self.mean,2 ) / 2 - 3 * ((nodes + 1) / 2 - nodes) * self.mean / 2

                for j in range(2, nodes):
                    self.x[i, j] = ((nodes+1) / 2 - j) * self.dx
                    self.Pu[i, j] = 1 / 6 + math.pow(((nodes + 1) / 2 - j), 2) *  math.pow(self.mean,2 ) / 2 + ((nodes + 1) / 2 - j) * self.mean / 2
                    self.Pm[i, j] = 2 / 3 - math.pow(((nodes + 1) / 2 - j), 2) *  math.pow(self.mean,2 )
                    self.Pd[i, j] = 1 / 6 + math.pow(((nodes + 1) / 2 - j), 2 )*  math.pow(self.mean,2 ) / 2 - ((nodes + 1) / 2 - j) * self.mean / 2

        #self.x = np.delete(self.x, 0, 0)
        self.x = np.delete(self.x, 0, 1)

        self.Pu = np.delete(self.Pu, 0, 0)
        self.Pu = np.delete(self.Pu, 0, 1)

        self.Pm = np.delete(self.Pm, 0, 0)
        self.Pm = np.delete(self.Pm, 0, 1)

        self.Pd = np.delete(self.Pd, 0, 0)
        self.Pd = np.delete(self.Pd, 0, 1)

    def as_json(self):
        return dict(
            sigma=self.sigma,
            alpha=self.alpha,
            maturity=self.maturity,
            x=self.x,
            jmax = self.jmax,
            pu=self.Pu,
            pd=self.Pd,
            dim=self.dim,
            step=self.step,
            pm=self.Pm,
        )