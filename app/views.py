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
import  numpy as np


def home(request):
    hwinput = parse_request(request)
    hw = HullWhiteEngine(hwinput)
    r, N, dt, jmax = hw.compute2()
    input_json = json.dumps(hwinput.as_json(), cls=DjangoJSONEncoder)
    html_fig = draw_2(r,N,dt, jmax)
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


def draw_data(hw):
    fig, ax = plt.subplots()
    r = hw.r_initial
    N = hw.N
    dt = hw.dt
    dr = hw.dr
    plot([0, 100*r[2][1]])
    plot([0, 100*r[2][0]])
    plot([0, 100*r[2][-1]])

    for i in range(0, N, 1):
        for j in range(-i, i + 1, 1):
            plot([i, i + 1], [r[i][j] * 100, r[i][j - 1] * 100])
            plot([i, i + 1], [r[i][j] * 100, r[i][j    ] * 100])
            plot([i, i + 1], [r[i][j] * 100, r[i][j + 1] * 100])

    ax.set_xlim(0, N+1)
    ax.set_ylim(-N-1, N+1)
    ax.set_xlabel('Time step')
    ax.set_ylabel('Rate')
    ax.set_xticks(np.arange(0, N + 1, dt))

    ax.set_title('Hull White Trinomial tree')
    ax.grid(True)
    html_fig = mpld3.fig_to_html(fig, template_type='general')
    plt.close(fig)
    return html_fig


def draw_2(r,N,dt,jmax):
    # Implementing the graphique

    i = 0
    matriz = []
    names = []
    names_set = []

    for line in r:
        j = 0
        top_node = int(min(i, jmax))

        if i < len(r) - 1:
            for j in range(-top_node, top_node + 1):
                if j == -jmax:
                    matriz.append([(i, r[i, j + jmax]), (i + 1, r[i + 1, j + 2 + jmax])])
                    matriz.append([(i, r[i, j + jmax]), (i + 1, r[i + 1, j + 1 + jmax])])
                    matriz.append([(i, r[i, j + jmax]), (i + 1, r[i + 1, j + jmax])])

                elif j == jmax:
                    matriz.append([(i, r[i, j + jmax]), (i + 1, r[i + 1, j + jmax])])
                    matriz.append([(i, r[i, j + jmax]), (i + 1, r[i + 1, j - 1 + jmax])])
                    matriz.append([(i, r[i, j + jmax]), (i + 1, r[i + 1, j - 2 + jmax])])

                else:
                    matriz.append([(i, r[i, j + jmax]), (i + 1, r[i + 1, j + 1 + jmax])])
                    matriz.append([(i, r[i, j + jmax]), (i + 1, r[i + 1, j + jmax])])
                    matriz.append([(i, r[i, j + jmax]), (i + 1, r[i + 1, j - 1 + jmax])])

                names_set.append((i, r[i, j + jmax]))
                names.append((i, j))
        else:
            for j in range(-top_node, top_node + 1):
                names_set.append((i, r[i, j + jmax]))
                names.append((i, j))
        i += 1

    fig = plt.figure()
    ax = fig.add_subplot(111)

    for l in matriz:
        d = [[p[0] for p in l], [p[1] for p in l]]
        ax.plot(d[0], d[1], 'k-*')

    i_names = 0
    for p in names_set:
        print(p[1] * 0.9)
        ax.annotate(names[i_names], xy=(p[0], p[1]), xytext=(p[0] * 0.95, p[1] * 0.9), fontsize=13, color='blue')
        i_names += 1

    plt.ylim([0, .15])
    ax.set_xlim(0, N + 1)
    ax.set_xlabel('Time step')
    ax.set_ylabel('Rate')
    ax.set_xticks(np.arange(0, N + 1, dt))
    ax.set_title('Hull White Trinomial tree')
    ax.grid(True)
    html_fig = mpld3.fig_to_html(fig, template_type='general')
    plt.close(fig)
    return html_fig


def parse_request(request):
    maturity = int(request.GET.get('maturity', 4))
    period = request.GET.get('period', 'years')
    alpha = float(request.GET.get('alpha', 0.1))
    volatility = float(request.GET.get('volatility', 0.01))
    source_rate = request.GET.get("source_rate", "bloomberg")
    rates = []
    rates.append(0.0509389)
    rates.append(0.0579733)
    rates.append(0.0630595)
    rates.append(0.0673464)
    rates.append(0.0694816)

    rate = request.GET.getlist("rate", rates)
    try:
        rate_float = [float(i) for i in rate]
    except :
        rate_float = rates

    return HwInput(volatility, maturity, alpha, period, rate_float, source_rate)
