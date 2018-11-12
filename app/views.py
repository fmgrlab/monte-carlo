from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from app.hull_white import HullWhite
import json
from django.core.serializers.json import DjangoJSONEncoder
import numpy as np

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def home(request):
    hw = parseCompute(request)
    hw_json = json.dumps(hw.as_json(), cls=NumpyEncoder)
    print(hw_json);
    return render(request, 'home.html', {"hw": hw, "hw_json": hw_json})

def documentation(request):
    return render(request, 'document.html')

def about(request):
    return render(request, 'about.html')


def compute(request):
    return JSONResponse(parseCompute(request).as_json())

def parseCompute(request):
    maturity = int(request.GET.get('maturity',4))
    step = int(request.GET.get('step',4))
    alpha = float(request.GET.get('alpha',0.1))
    volatility = float(request.GET.get('volatility',0.01))
    hw = HullWhite(maturity,volatility,alpha,step)
    hw.init_data()
    return hw
