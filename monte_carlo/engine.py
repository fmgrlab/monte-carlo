import  math
import  numpy as np
from monte_carlo.domain import Payoff
class Engine:

    def __init__(self, param):
         self.param = param

    def compute_all_prices(self,strike,type):
        payoffs = []
        for n in [1000,2000]:
            payoff = Payoff()
            payoff.strike = strike
            payoff.type = type
            payoff.iteration_number = n
            stock_price = self.compute_price(n)
            if type =='put':
               payoff.price=  max(strike - stock_price, 0)
            else:
               payoff.price =  max(stock_price - strike, 0)
            payoffs.append(payoff)
        return payoffs

    def compute_price(self, n):
        v = 0.01
        dt = self.param.maturity/ self.param.number_of_step
        previous_stock = self.param.stock_initial
        stock = np.zeros(shape=(n, self.param.number_of_step))
        for i in range(0,n):
            for j in range(0,self.param.number_of_step):
                prob = np.random.normal(0, 1.0)
                current_stock = previous_stock + previous_stock * self.param.stock_return * dt +\
                                math.sqrt(v*dt) * previous_stock *prob
                previous_stock = current_stock
                stock[i][j] = current_stock

        row_average = []
        for i in range(0, n):
            row_average.append(np.average(stock[i]))
        total_average = np.average(row_average)
        return total_average



