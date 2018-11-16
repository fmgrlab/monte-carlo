
class Node():
    def __init__(self,j,r, Pu,Pd, Pm):
        self.j = j
        self.r = r
        self.Pu = Pu
        self.Pd = Pd
        self.Pm = Pm

    def as_json(self):
        return dict(
            j = self.j,
            r = self.r,
            Pm = self.Pm,
            Pd = self.Pd,
            Pu = self.Pu
        )


class HwInput():
    def __init__(self,volatility,maturity, alpha, period, rate, source_rate):
        self.volatility = volatility
        self.maturity = maturity
        self.alpha = alpha
        self.period = period
        self.rate = rate
        self.source_rate = source_rate
        self.step = self.get_step(period = period,maturity = maturity)

    def as_json(self):
        return dict(
            step=self.step,
            period = self.period,
            alpha=self.alpha,
            rate = self.rate,
            volatility=self.volatility,
            maturity=self.maturity,
            source_rate = self.source_rate

        )

    def get_step(self,period, maturity):
        if period.lower().startswith('w'):
            return 52*maturity
        if period.lower().startswith('d'):
            return 360*maturity
        if period.lower().startswith('s'):
            return 2*maturity
        if period.lower().startswith('q'):
            return 4*maturity
        return maturity