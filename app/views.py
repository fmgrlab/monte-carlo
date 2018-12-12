from __future__ import unicode_literals

import matplotlib

matplotlib.use("Agg")
from django.shortcuts import render
from app.hull_white import HWCalculator
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer


def home(request):
    hwcalculator = HWCalculator()
    hwcalculator.execute(0.01, 0.1, 5, 1.0 / 1.0)
    return render(request, 'home.html', { "hw": hwcalculator})


def documentation(request):
    return render(request, 'document.html')


def about(request):
    return render(request, 'about.html')


def api_hullwhite(request):
    hwcalculator = HWCalculator()
    hwcalculator.execute(0.01,0.1, 5, 1)
    return JSONResponse(hwcalculator.as_json())

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)