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
from monte_carlo import  views
admin.autodiscover()

urlpatterns = [
    url(r'^api/iteration$', views.api_iteration, name='api-iteration'),
    url(r'^api/risk', views.api_risk, name='api-risk'),
    url(r'^api/volatility', views.api_volatility, name='api-volatility'),

    url(r'^demo/iteration$', views.demo_iteration, name='api-iteration'),
    url(r'^demo/risk', views.demo_risk, name='api-risk'),
    url(r'^demo/volatility', views.demo_volatility, name='api-volatility'),
]
