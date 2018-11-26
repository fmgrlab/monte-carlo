from __future__ import unicode_literals
import matplotlib
matplotlib.use('TkAgg')
from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
import json
from app.models import  HwInput
from app.hw_engine import HullWhiteEngine
from django.http import HttpResponse
from matplotlib import pylab
from pylab import *
from io import BytesIO as StringIO
import PIL, PIL.Image
from app import utils

def home(request):
    input = parseRequest(request)
    input_json = json.dumps(input.as_json(), cls=DjangoJSONEncoder)
    hw = HullWhiteEngine(input)
    hw_json  = json.dumps(hw.as_json(), cls=DjangoJSONEncoder)
    hw.compute()
    return render(request, 'home.html', {"input": input, "input_json" : input_json,"hw": hw, "hw_json" : hw_json})

def documentation(request):
    return render(request, 'document.html')

def about(request):
    return render(request, 'about.html')


def compute(request):
    input  = parseRequest(request)
    hw = HullWhiteEngine(input)
    hw.compute()
    return utils.JSONResponse(hw.as_json())

def draw_hull_white_tree(request):
    figure(figsize=(16, 16))

    for i in range(0,10,1):
        for j in range(-i,i+1,1):
            text(i, j, "AA")

    xlim(0, 10)
    ylim(-15, 15)
    xticks(arange(10))
    yticks(arange(-15,15,1))
    xlabel('Maturity')
    ylabel('Rate')
    title('Hull White interest rate')
    grid(True)
    buffer = StringIO()
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    pilImage = PIL.Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())
    pilImage.save(buffer, "PNG")
    pylab.close()

    return HttpResponse(buffer.getvalue(), content_type="image/png")


def parseRequest(request):
    maturity = int(request.GET.get('maturity', 3))
    period = request.GET.get('period', "q")
    alpha = float(request.GET.get('alpha', 0.1))
    volatility = float(request.GET.get('volatility', 0.01))
    source_rate = request.GET.get("source_rate", "bloomberg")
    rates = list()
    rates.append(10)
    rates.append(10.5)
    rates.append(11)
    rates.append(11.25)
    rates.append(11.50)
    rate = request.GET.getlist("rate", rates)
    return HwInput(volatility, maturity, alpha, period, rate, source_rate)
