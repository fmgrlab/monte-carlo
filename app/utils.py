from __future__ import unicode_literals

from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def gen_id(i,j):
    return "("+str(i)+","+str(j) +")"

def val(value):
    return round(value,4)


def percent(value):
    return val(value)*100
