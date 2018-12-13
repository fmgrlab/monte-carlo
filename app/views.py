from __future__ import unicode_literals

import matplotlib

matplotlib.use("Agg")
from django.shortcuts import render
from app.hull_white import HWCalculator
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer


import matplotlib

matplotlib.use("Agg")
from django.shortcuts import render
from django.http import HttpResponse
import mpld3
from pylab import *



def home(request):
    hwcalculator = HWCalculator()
    rates = []
    maturity = 5
    dt = 1
    N = int(maturity/dt)
    for i in range(0, N+1, 1):
        rates.append(0.08 - 0.05 * math.exp(-0.18 * i))
    hwcalculator.execute(0.01, 0.1, 5, 1.0 / 2.0,rates)
    html_fig = draw_data(hwcalculator)
    return render(request, 'home.html', { "hw": hwcalculator,'div_figure': html_fig})


def documentation(request):
    return render(request, 'document.html')


def about(request):
    return render(request, 'about.html')


def api_hullwhite(request):
    hwcalculator = HWCalculator()
    hwcalculator.execute(0.01,0.1, 5, 1)
    return JSONResponse(hwcalculator.as_json())


def draw_data(hw):
    N = len(hw.steps)-1
    fig, ax = plt.subplots()
    for i in range(0,N,1):
        top_node = min(i,hw.jmax)
        for j in range(-top_node,top_node+1,1):
            node = hw.steps[i].nodes[j+top_node]
            up = hw.steps[i+1].nodes[node.j_up  + top_node]
            m = hw.steps[i+1].nodes[node.j_m  + top_node]
            dw = hw.steps[i+1].nodes[node.j_d  + top_node]
            plot([i,  i+1], [node.rate*100, up.rate*100])
            plot([i,  i+1], [node.rate*100, m.rate*100])
            plot([i , i+1], [node.rate*100, dw.rate*100])

    ax.set_xlim(0, N)
    ax.set_ylim(-N,N)
    ax.set_xlabel('Maturity')
    ax.set_ylabel('Rate')

    ax.set_title('Hull White interest rate')
    ax.grid(True)
    html_fig = mpld3.fig_to_html(fig, template_type='general')
    plt.close(fig)
    return html_fig


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

