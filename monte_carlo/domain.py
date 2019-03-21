import math
from collections import OrderedDict


class Param:
    def __init__(self):
        self.stock_initial = 0
        self.stock_return = 0

        self.market_volatility = 0
        self.market_return = 0

        self.volatility_initial = 0
        self.volatility_long = 0
        self.volatility_speed = 0
        self.volatility_sigma = 0

        self.maturity = 0
        self.number_of_step = 0
        self.correlation_stock_market = 0
        self.correlation_stock_volatility = 0
        self.b = 0

    def as_json(self):
        dict = OrderedDict()
        dict['stock_initial'] = self.stock_initial
        dict['stock_return'] = self.stock_return

        dict['market_volatility'] = self.market_volatility
        dict['market_return'] = self.market_return

        dict['volatility_initial'] = self.volatility_initial
        dict['volatility_long'] = self.volatility_long
        dict['volatility_speed'] = self.volatility_speed
        dict['volatility_sigma'] = self.volatility_sigma

        dict['maturity'] = self.maturity
        dict['number_of_step'] = self.number_of_step
        dict['correlation_stock_market'] = self.correlation_stock_market
        dict['correlation_stock_volatility'] = self.correlation_stock_volatility
        return dict


class Payoff:

    def __init__(self):
        self.strike= 0
        self.iteration_number = 0
        self.price = 0
        self.std_error = 0
        self.confidence_up =0
        self.confidence_down = 0

    def as_json(self):
        dict = OrderedDict()
        dict['strike'] = self.strike
        dict['iteration'] = self.iteration_number
        dict['price'] = self.price
        dict['std_error'] = self.std_error
        dict['confidence_up'] = self.confidence_up
        dict['confidence_down'] = self.confidence_down
        return dict


class OutPut:
    def __init__(self):
        self.param = Param()
        self.payoffs = []

    def as_json(self):
        dict = OrderedDict()
        dict['input'] = self.param.as_json()
        dict['payoffs'] = [ob.as_json() for ob in self.payoffs]
        return dict



