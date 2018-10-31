

class HullWhite():
    def __init__(self, sigma,alpha, maturity,step):
        self.sigma = sigma
        self.alpha = alpha
        self.maturity = maturity
        if step <1:
            step = 1
        self.step = step




