"""
URL configuration for tmysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import views
from django.contrib import admin
from django.urls import path

from mysite.views import hello, current_datetime, hours_ahead, math, valid_date

urlpatterns = [
    path('admin/', admin.site.urls),
    path("hello/", hello),
    path("time/", current_datetime),
    path("time/plus/<int:offset>/", hours_ahead),
    path('math/<int:number1>/<int:number2>/', math, name='math_two'),
    path('math/<int:number1>/<int:number2>/<int:number3>/', math, name='math_three'),
    path('valid-date/<int:year>/<int:month>/<int:day>/', valid_date),
]
