"""m2_hull_white URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin
from app import views
from m2_hull_white import  views
admin.autodiscover()

urlpatterns = [
    url(r'^document/', views.documentation, name='document'),
    url(r'^about/', views.about, name='about'),
    url(r'^$', views.home, name='home'),

    url(r'^hwhite/', include('app.urls')),
    url(r'^bsm/', include('bsm.urls')),
    url(r'^mcarlo/', include('monte_carlo.urls')),
]
