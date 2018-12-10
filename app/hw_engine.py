class HullWhiteEngine():
    def __init__(self, hwinput):
        self.hwinput = hwinput
        self.steps = list()

    def as_json(self):
        return dict(
            hwinput=self.hwinput.as_json(),
            steps=[ob.as_json() for ob in self.steps]
        )

    def compute(self):
        N = self.get_step(self.hwinput.period, self.hwinput.maturity)
        return self.compute_value(N, self.hwinput.period, self.hwinput.maturity, self.hwinput.volatility,
                                  self.hwinput.alpha, self.hwinput.rate)

    def compute_value(self, N, dt, maturity, sig, alpha, R):
        return self.hwinput

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
