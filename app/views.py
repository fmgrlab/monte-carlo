from __future__ import unicode_literals
import matplotlib
matplotlib.use('TkAgg')
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from app.m2_hull_white import HullWhite2
from django.core.serializers.json import DjangoJSONEncoder
import json
import numpy as np
from app.models import  HwInput
from app.hw_engine import HullWhiteEngine
from django.http import HttpResponse
from matplotlib import pylab
from pylab import *
from io import BytesIO as StringIO
import PIL, PIL.Image

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
    input = getInput(request)
    input_json = json.dumps(input.as_json(), cls=DjangoJSONEncoder)
    return render(request, 'home.html', {"input": input, "input_json" : input_json})

def documentation(request):
    return render(request, 'document.html')

def about(request):
    return render(request, 'about.html')


def compute(request):
    input  = getInput(request)
    return JSONResponse(input.as_json())

def getInput(request):
    maturity = int(request.GET.get('maturity',3))
    period = request.GET.get('period',"q")
    alpha = float(request.GET.get('alpha',0.1))
    volatility = float(request.GET.get('volatility',0.01))
    source_rate = request.GET.get("source_rate","bloomberg")
    rates = list()
    rates.append(10)
    rates.append(10.5)
    rates.append(11)
    rates.append(11.25)
    rates.append(11.50)
    rate = request.GET.getlist("rate",rates)
    return HwInput(volatility,maturity,alpha,period,rate, source_rate)



def draw_hull_white_tree(request):
    t = arange(0.0, 2.0, 0.01)
    s = sin(2 * pi * t)
    plot(t, s, linewidth=1.0)

    xlabel('time (s)')
    ylabel('voltage (mV)')
    title('About as simple as it gets, folks')
    grid(True)
    buffer = StringIO()
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    pilImage = PIL.Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())
    pilImage.save(buffer, "PNG")
    pylab.close()

    return HttpResponse(buffer.getvalue(), content_type="image/png")
