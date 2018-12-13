from __future__ import unicode_literals

import matplotlib

matplotlib.use("Agg")
from app.hull_white import HWCalculator
from rest_framework.renderers import JSONRenderer


import matplotlib

matplotlib.use("Agg")
from django.shortcuts import render
from django.http import HttpResponse
import mpld3
from pylab import *



def home(request):
    maturity, period_name, nbr_steps, alpha, volatility, rate_float, success = parseRequest(request=request)
    hwc = HWCalculator()
    hwc.maturity = maturity
    hwc.period = period_name
    hwc.nbr_steps = nbr_steps
    hwc.alpha = alpha
    hwc.volatility = volatility
    hwc.rates = rate_float
    if success:
        hwc.execute()
        html_fig = draw_data(hwc)
        return render(request, 'home.html', {"hw": hwc, 'div_figure': html_fig})
    else :
        return render(request, 'home_error.html', {"hw": hwc})





def documentation(request):
    return render(request, 'document.html')


def about(request):
    return render(request, 'about.html')


def api_hullwhite(request):
    maturity, period_name, nbr_steps, alpha, volatility, rate_float, success = parseRequest(request=request)
    hwc = HWCalculator()
    hwc.maturity = maturity
    hwc.period = period_name
    hwc.nbr_steps = nbr_steps
    hwc.alpha = alpha
    hwc.volatility = volatility
    hwc.rates = rate_float
    if success:
        hwc.execute()
    return JSONResponse(hwc.as_json())


def draw_data(hw):
    fig, ax = plt.subplots()
    N = hw.nbr_steps
    print(N)
    for i in range(0,N-1,1):
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
    ax.set_ylim(-10,10)
    ax.set_xlabel('Maturity')
    ax.set_ylabel('Rate')

    ax.set_title('Hull White interest rate')
    ax.grid(True)
    html_fig = mpld3.fig_to_html(fig, template_type='general')
    plt.close(fig)
    return html_fig


def parseRequest(request):
    maturity = float(request.GET.get('maturity', 3))
    alpha = float(request.GET.get('alpha', 0.1))
    volatility = float(request.GET.get('volatility', 0.01))
    period_name = request.GET.get('period', 'year')
    period = get_period_value(period_name)

    rates = request.GET.getlist("rate", '')
    nbr_steps = maturity*period
    rate_float = []
    for item in rates:
        try:
            rate_float.append(double(item))
        except :
            pass

    return maturity,period_name,nbr_steps,alpha,volatility,rate_float,len(rate_float) >= (nbr_steps+1)


def get_period_value(period_param):
    period = str(period_param)
    if period.lower().startswith('d'):
        return 250
    if period.lower().startswith('w'):
        return 52
    if period.lower().startswith('m'):
        return 12
    if period.lower().startswith('s'):
        return 2
    if period.lower().startswith('q'):
        return 4
    return 1

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

