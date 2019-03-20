from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.shortcuts import render
# Create your views here.


def home(request):
    return render(request, 'base_home.html')

def documentation(request):
    return render(request, 'document.html')

def about(request):
    return render(request, 'about.html')

