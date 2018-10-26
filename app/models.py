from __future__ import unicode_literals
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer

class Node():
    def __init__(self, n,j, r, node_u,node_d, node_m):
        self.n = n
        self.j = j
        self.r = r
        self.node_u = node_u
        self.node_d = node_d
        self.node_m = node_m

    def as_json(self):
        return dict(
            n = self.n,
            j = self.j,
            r = self.r,
            node_u = self.node_u,
            node_d = self.node_d,
            node_m = self.node_m
        )


class JSONResponse(HttpResponse):

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
