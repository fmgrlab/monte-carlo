from collections import OrderedDict
from app import utils
class HwStep():
    def __init__(self, i):
        self.i = i
        self.nodes = []

    def as_json(self):
        dict = OrderedDict()
        dict['i'] = self.i
        dict['nodes'] = [ob.as_json() for ob in self.nodes]
        return dict

class Node():
    def __init__(self, i=0, j = 0,r_initial= 0.0, q = 0.0,pu=None, pm=None, pd=None, next_up = None, next_m = None, next_d = None, ):
        self.i = i
        self.j = j
        self.r_initial = ""
        self.pu = pu
        self.pd = pd
        self.pm = pm
        self.q = 0.0
        self.j_up =0
        self.j_m = 0
        self.j_d = 0
        self.next_up = next_up
        self.next_m = next_m
        self.next_d = next_d
        self.id = utils.gen_id(i,j)

    def as_json(self):
        dict = OrderedDict()
        dict['id'] = self.id
        dict['i'] = self.i
        dict['j'] = self.j
        dict['r_initial'] = self.r_initial
        dict['q'] = self.q
        dict['pu'] = self.pu
        dict['pm'] = self.pm
        dict['pd'] = self.pd
        dict['next_up'] = self.next_up
        dict['next_m'] = self.next_m
        dict['next_d'] = self.next_d

        return dict

class HwInput():
    def __init__(self, volatility, maturity, alpha, period, rate, source_rate):
        self.volatility = volatility
        self.maturity = maturity
        self.alpha = alpha
        self.period = period
        self.rate = rate
        self.N = self.get_step(period,maturity)
        self.source_rate = source_rate

    def as_json(self):
        dict = OrderedDict()
        dict['maturity'] = self.maturity
        dict['period'] = self.period
        dict['N'] = self.N
        dict['alpha'] = self.alpha
        dict['volatility'] = self.volatility
        dict['source_rate'] = self.source_rate
        dict['rate'] = self.rate
        return dict

    def get_step(self, period, maturity):
        if period is None or len(period) == 0:
            return maturity
        if period.lower().startswith('w'):
            return 52 * maturity
        if period.lower().startswith('d'):
            return 360 * maturity
        if period.lower().startswith('s'):
            return 2 * maturity
        if period.lower().startswith('q'):
            return 4 * maturity
        return maturity
