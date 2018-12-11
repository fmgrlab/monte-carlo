from collections import OrderedDict

from app import utils

class GraphStep():
    def __init__(self, i):
        self.i = i
        self.nodes = []

    def as_json(self):
        dict = OrderedDict()
        dict['i'] = self.i
        dict['nodes'] = [ob.as_json() for ob in self.nodes]
        return dict


class GraphNode():
    def __init__(self, i=0, j = 0,pu ="", pm="", pd="", rate = 0):
        self.id = utils.gen_id(i,j)
        self.i = i
        self.j = j
        self.pu = pu
        self.pd = pd
        self.pm = pd
        self.rate = rate

    def as_json(self):
        dict = OrderedDict()
        dict['i'] = self.i
        dict['j'] = self.j
        dict['pu'] = self.pu
        dict['pm'] = self.pm
        dict['pd'] = self.pd
        return dict
