from django.shortcuts import render
from django.http import JsonResponse
from monte_carlo.domain import OutPut

def mcarlo_home(request):
    return render(request, 'mcarlo.html')

def api_monte_carlo(request):
    return JsonResponse(OutPut().as_json())