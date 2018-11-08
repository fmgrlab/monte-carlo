from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from app.hull_white import HullWhite


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def home(request):
    return render(request, 'home.html')

def documentation(request):
    return render(request, 'document.html')

def about(request):
    return render(request, 'about.html')


def compute(request):
    return JSONResponse(parseCompute(request).as_json())

def parseCompute(request):
    maturity = float(request.GET.get('maturity',50))
    step = float(request.GET.get('step',50))
    alpha = float(request.GET.get('alpha',10))
    volatility = float(request.GET.get('volatility',30))
    hw = HullWhite(maturity,volatility,alpha)
    hw.init_data()
    return hw
