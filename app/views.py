from __future__ import unicode_literals

import matplotlib

matplotlib.use("Agg")
from django.shortcuts import render
from app.objects import HwInput
from django.core.serializers.json import DjangoJSONEncoder
import json
from app.hw_engine import HullWhiteEngine
import mpld3
from pylab import *
from app import utils


def home(request):
    hwinput = parse_request(request)
    hw = HullWhiteEngine(hwinput)
    hw.compute()
    input_json = json.dumps(hwinput.as_json(), cls=DjangoJSONEncoder)
    html_fig = draw_data(hw)
    return render(request, 'home.html', {"input": hwinput, "input_json": input_json, "hw": hw, 'div_figure': html_fig})


def documentation(request):
    return render(request, 'document.html')


def about(request):
    return render(request, 'about.html')


def api_hullwhite(request):
    input = parse_request(request)
    hw = HullWhiteEngine(input)
    hw.compute()
    return utils.JSONResponse(hw.as_json())


def draw_data(r):
    fig, ax = plt.subplots()
    """""
    for i in range(0,10,1):
        node = min(i,2)
        for j in range(-node,node+1,1):
            plot([i,  i+1], [r[i][j]*100, r[i][j-1]*100])
            plot([i,  i+1], [r[i][j]*100, r[i][j]*100])
            plot([i , i+1], [r[i][j]*100, r[i][j+1]*100])
    """""

    ax.set_xlim(0, 6)
    ax.set_ylim(-6, 6)
    ax.set_xlabel('Maturity')
    ax.set_ylabel('Rate')

    ax.set_title('Hull White interest rate')
    ax.grid(True)
    html_fig = mpld3.fig_to_html(fig, template_type='general')
    plt.close(fig)
    return html_fig


def parse_request(request):
    maturity = int(request.GET.get('maturity', 5))
    period = request.GET.get('period', 'y')
    alpha = float(request.GET.get('alpha', 0.1))
    volatility = float(request.GET.get('volatility', 0.01))
    source_rate = request.GET.get("source_rate", "bloomberg")
    rates = list()
    rates.append(10)
    rates.append(10.5)
    rates.append(11)
    rates.append(11.25)
    rates.append(11.50)
    rates.append(12.25)
    rate = request.GET.getlist("rate", rates)
    return HwInput(volatility, maturity, alpha, period, rate, source_rate)
