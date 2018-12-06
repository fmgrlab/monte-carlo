from __future__ import unicode_literals

import matplotlib

matplotlib.use("Agg")
from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
import json
from app.objects import HwInput
from app.hw_engine import HullWhiteEngine
from django.http import HttpResponse
from matplotlib import pylab
import mpld3
from pylab import *
from io import BytesIO as StringIO
import PIL, PIL.Image
from app import utils
from  app.models import Hw_Step

def home(request):
    input = parseRequest(request)
    input_json = json.dumps(input.as_json(), cls=DjangoJSONEncoder)
    hw = HullWhiteEngine(input)
    hw.compute()
    hw_json = json.dumps(hw.as_json(), cls=DjangoJSONEncoder)
    Hw_Step.objects.all().delete()
    hw_step = Hw_Step()
    hw_step.data = hw_json
    hw_step.save()
    html_fig = draw_data(hw)
    return render(request, 'home.html', {"input": input, "input_json": input_json, "hw": hw, "hw_json": hw_json,'div_figure' : html_fig})

def documentation(request):
    return render(request, 'document.html')


def about(request):
    return render(request, 'about.html')


def compute(request):
    input = parseRequest(request)
    hw = HullWhiteEngine(input)
    hw.compute()
    return utils.JSONResponse(hw.as_json())


def draw_data(hw):
    fig, ax = plt.subplots()
    plot([0, 3], [0, 6])
    ax.set_xlim(0, 6)
    ax.set_ylim(-6,6)
    ax.set_xlabel('Maturity')
    ax.set_ylabel('Rate')
    ax.grid(True)
    html_fig = mpld3.fig_to_html(fig, template_type='general')
    plt.close(fig)
    return html_fig

def draw_hull_white_treOLDe(request):
    figure(figsize=(9, 7))
    hw_step = Hw_Step.objects.get(pk=1)
    hwdata = json.loads(hw_step.data)
    for stp in hwdata['steps']:
        for node in stp['nodes']:
            plot([node["i"],node["x"]],[node["i"],node["x"]])
    xlim(0, 6)
    ylim(-6, 6)
    xticks(arange(15))
    yticks(arange(-10, 15, 1))
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
