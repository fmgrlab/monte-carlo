import matplotlib
matplotlib.use("Agg")
from django.shortcuts import render
import mpld3
from pylab import *

def home(request):
    data = draw_data()
    return render(request, 'portofolio.html', {'graph': data})

def draw_data():
    fig, ax = plt.subplots()
    N  = 100
    xvals = np.arange(0, N)  # Grid of 0.01 spacing from -2 to 10
    yvals = list()  # Evaluate function on xvals

    rendement =list()
    rendement2 = list()

    for i in range(0,N) :
        brownien = np.random.normal(0, 1.0) * math.sqrt(1.0/100)
        rendement.append(0.15*(1.0/100)+0.4*brownien)
        st = 55.25*math.exp((0.15-0.5*0.4*0.4*1)+0.4*brownien)
        yvals.append(st)

    for i in range(0,N-1) :
        v = (yvals[i+1]-yvals[i])/yvals[i]
        rendement2.append(v)
    plt.plot(xvals, rendement)
    plt.plot(xvals[:N-1], rendement2)
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.set_title('Bromwien')
    ax.grid(True)
    html_fig = mpld3.fig_to_html(fig, template_type='general')
    plt.close(fig)
    return html_fig