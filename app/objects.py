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
        self.i = i
        self.j = j
        self.x = x
        self.r = r
        self.pu = pu
        self.pd = pd
        self.pm = pm
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
        self.step = self.get_step(period=period, maturity=maturity)

    def as_json(self):
        return dict(
            step=self.step,
            period=self.period,
            alpha=self.alpha,
            rate=self.rate,
            volatility=self.volatility,
            maturity=self.maturity,
            source_rate=self.source_rate

        )

    def get_step(self, period, maturity):
        if period.lower().startswith('w'):
            return 52 * maturity
        if period.lower().startswith('d'):
            return 360 * maturity
        if period.lower().startswith('s'):
            return 2 * maturity
        if period.lower().startswith('q'):
            return 4 * maturity
        return maturity
