from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def documentation(request):
    return render(request, 'document.html')

def about(request):
    return render(request, 'about.html')


def compute(request):
    return  render(request, 'about.html')


