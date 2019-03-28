import  math
import  numpy as np
class Engine:

    def __init__(self, param):
         self.param = param
         self.rand = []
         self.rand_stock =[]
         self.rand_vol =[]
         self.rand_market = []
         self.matrix = []

    def compute_stock_volatility_path(self, cho_matrix):
         volatilities = []
         v_temp = []
         volatilities.append(self.param.volatility_initial)
         v_temp[0] = self.param.volatility_initial
         for t in range(1, self.param.number_of_step + 1):
           ran = np.dot(cho_matrix, self.rand[:, t])
           kappa = self.param.volatility_speed
           theta = self.param.volatility_long
           sigma = self.param.volatility_sigma
           v_temp[t] = (v_temp[t - 1] + kappa *(theta - max(0, v_temp[t - 1])) * self.param.dt +np.sqrt (max(0, v_temp[t - 1]) ) *sigma * self.rand_vol * math.sqrt(self.param.dt))
           volatilities.append(max(0, v_temp[t]))
         return volatilities

    def compute_constant_volatility_path(self):
        volatilities = []
        for t in range(0, self.param.number_of_step + 1):
            volatilities.append(self.param.volatility_initial)
        return volatilities

    def compute_stock_path(self, volatilties,I,):
        stock_price = []
        previous_price = self.param.stock_initial
        for t in range(1, self.param.number_of_step + 1):
            ran = np.dot(self.matrix, self.rand[:, t])
            current_price = previous_price* (1 + self.param.stock_return* self.param.dt + np.sqrt(volatilties[t - 1]) *self.rand_stock * math.sqrt(self.param.dt))
            stock_price.append(current_price)
            previous_price = current_price
        return stock_price

    def compute_market_path(self, M0,):
        sdt = math.sqrt(self.param.dt)
        market_price = []
        previous_value = M0
        for i in range(1, self.param.number_of_step + 1):
            ran = np.dot(self.matrix, self.rand[:, i])
            current_value = previous_value * (1 +self.param.market_return * self.param.dt + self.param.market_volatility * self.rand_market * sdt)
            market_price.append(current_value)
            previous_value = current_value
        return market_price

    def generate_random_by_step(self, I):
        return np.random.standard_normal((3, self.param.number_of_step + 1, I))

    def generate_covariance(self):
        covariance_matrix = np.zeros((3, 3))
        covariance_matrix[0] = [1.0, self.param.correlation_stock_volatility, self.param.correlation_stock_market]
        covariance_matrix[1] = [self.param.correlation_stock_volatility, 1.0, 0]
        covariance_matrix[2] = [self.param.correlation_stock_market, 0, 1.0]
        return np.linalg.cholesky(covariance_matrix)






