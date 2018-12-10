class Step():
    def __init__(self, i):
        self.i = i
        self.nodes = list()
        self.theta = list()

    def as_json(self):
        return dict(
            i=self.i,
            nodes=[ob.as_json() for ob in self.nodes]
        )


class Node():
    def __init__(self, i=0, j=0, x = 0.0, pu=None, pm=None, pd=None, r = 0.0 ):
        self.id
        self.i = i
        self.j = j
        self.x = x
        self.position = None
        self.r = r
        self.presentValue = None
        self.alpha = 0;
        self.pu = pu
        self.pd = pd
        self.pm = pm
        self.node_up = None
        self.node_m = None
        self.node_d = None



        self.label = "N"+str(self.i)+"_"+str(self.j)


    def as_json(self):
        return dict(
            i=self.i,
            j=self.j,
            x=self.x,
            r=self.r,
            pu=self.pu,
            pm=self.pm,
            pd=self.pd,
            label = "N"+str(self.i)+"_"+str(self.j)
        )


class HwInput():
    def __init__(self, volatility, maturity, alpha, period, rate, source_rate):
        self.volatility = volatility
        self.maturity = maturity
        self.alpha = alpha
        self.period = period
        self.rate = rate
        self.source_rate = source_rate

    def as_json(self):
        return dict(
            period=self.period,
            alpha=self.alpha,
            rate=self.rate,
            volatility=self.volatility,
            maturity=self.maturity,
            source_rate=self.source_rate

        )
