
import matplotlib
matplotlib.use("Agg")
from django.http import JsonResponse
from django.shortcuts import render
from monte_carlo.domain import  *

def mcarlo_home(request):
    param = Param()
    return render(request, 'mcarlo.html',{"param": param})

def api_monte_carlo(request):
    return JsonResponse(OutPut().as_json())

4