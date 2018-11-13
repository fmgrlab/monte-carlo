
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

