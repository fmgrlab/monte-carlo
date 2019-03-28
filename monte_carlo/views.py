
import matplotlib
matplotlib.use("Agg")
from django.http import JsonResponse
from django.shortcuts import render
from monte_carlo.domain import  *
from monte_carlo.engine import Engine


def home(request):
    return render(request, 'index.html')

def demo_iteration(request):
    param = parse_param(request)
    return render(request, 'mcarlo_iteration.html',{"param": param})

def demo_volatility(request):
    param = parse_param(request)
    return render(request, 'mcarlo_volatility.html',{"param": param})

def demo_risk(request):
    param = parse_param(request)
    return render(request, 'mcarlo_risk.html',{"param": param})

def api_volatility(request):
    param = parse_param(request)
    output = OutPut()
    output.param = param
    return JsonResponse(output.as_json())

def api_risk(request):
    param = parse_param(request)
    output = OutPut()
    output.param = param
    return JsonResponse(output.as_json())

def api_iteration(request):
    param = parse_param(request)
    output = OutPut()
    output.param = param
    engine = Engine(param)
    return JsonResponse(output.as_json())


def api_monte_carlo(request):
    param = parse_param(request)
    output = OutPut()
    output.param = param
    return JsonResponse(output.as_json())


def parse_param(request):
    param = Param()
    param.stock_initial = int(request.GET.get('stock_initial',100))
    param.stock_return = float(request.GET.get('stock_return', 0.1241))

    param.market_volatility = float(request.GET.get('market_volatility', 0.12))
    param.market_return = float(request.GET.get('market_return', 0.1))

    param.volatility_initial = float(request.GET.get('volatility_initial', 0.1))
    param.volatility_long = float(request.GET.get('volatility_long', 0.1))
    param.volatility_speed = float(request.GET.get('volatility_speed', 0.5))
    param.volatility_sigma = float(request.GET.get('volatility_sigma', 0.05))

    param.maturity = int(request.GET.get('maturity', 1))
    param.number_of_step = int(request.GET.get('number_of_step', 100))
    param.correlation_stock_market = float(request.GET.get('correlation_stock_market', 0.5))
    param.correlation_stock_volatility = float(request.GET.get('correlation_stock_volatility', -0.5))

    param.b = request.GET.get('b', 5)

    return param