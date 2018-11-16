
class HullWhiteEngine():
    def __init__(self,hwinput):
        self.hwinput = hwinput


    def as_json(self):
        return dict(
            input = self.hwinput,
            output= "[]",
        )
