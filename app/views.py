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
    graph, r, N, dt = hw.compute2()
    input_json = json.dumps(hwinput.as_json(), cls=DjangoJSONEncoder)
    html_fig = draw_2(graph,r,N,dt,hw.hwsteps)
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


def draw_2(graph,r,N,dt,hwsteps):
    i = 0
    matriz = []
    names = []
    names_set = set()

    for k1 in graph:
        names.append(k1)
    names = sorted(names)

    for line in r:
        j = 0
        if i < len(r) - 1:
            for element in line:
                if element != 0:
                    if j == 1 or j == 2 or j == 3:
                        matriz.append([(i, r[i, j]), (i + 1, r[i + 1, j + 1])])
                        matriz.append([(i, r[i, j]), (i + 1, r[i + 1, j])])
                        matriz.append([(i, r[i, j]), (i + 1, r[i + 1, j - 1])])
                        #names_set.add()

                    elif j == 0:
                        matriz.append([(i, r[i, j]), (i + 1, r[i + 1, j + 2])])
                        matriz.append([(i, r[i, j]), (i + 1, r[i + 1, j + 1])])
                        matriz.append([(i, r[i, j]), (i + 1, r[i + 1, j])])

                    elif j == 4:
                        matriz.append([(i, r[i, j]), (i + 1, r[i + 1, j])])
                        matriz.append([(i, r[i, j]), (i + 1, r[i + 1, j - 1])])
                        matriz.append([(i, r[i, j]), (i + 1, r[i + 1, j - 2])])

                # names_set.add((i, r[i,j]))

                j += 1

        else:
            for element in line:
                # names_set.add((i, r[i,j]))

                j += 1

        i += 1
    fig, ax = plt.subplots()
    for l in matriz:
        d = [[p[0] for p in l], [p[1] for p in l]]
        ax.plot(d[0], d[1], 'k-*')
        for p in l:
            names_set.add(p)
    i_names = 0
    for p in names_set:
       # ax.annotate(names[i_names], xy=p)
        i_names += 1

    for hstep in hwsteps:
        nodes = hstep.nodes
        for node in nodes:
            print(node.id)
            #plt.text(node.i,node.rate, node.id)

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
    maturity = int(request.GET.get('maturity', 5))
    period = request.GET.get('period', 'years')
    alpha = float(request.GET.get('alpha', 0.1))
    volatility = float(request.GET.get('volatility', 0.014))
    source_rate = request.GET.get("source_rate", "bloomberg")
    rates = []
    rates.append(0.0509389)
    rates.append(0.0579733)
    rates.append(0.0630595)
    rates.append(0.0673464)
    rates.append(0.0694816)
    rates.append(0.0708807)
    rates.append(0.0727527)
    rates.append(0.0730852)
    rates.append(0.0739790)
    rates.append(0.0749015)
    rate = request.GET.getlist("rate", rates)
    return HwInput(volatility, maturity, alpha, period, rate, source_rate)
