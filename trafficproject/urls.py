"""
URL configuration for trafficproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from trafficapp import views as traffic_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard', traffic_views.dashboard, name='dashboard'),
    path('helmetdetection', traffic_views.helmetdetection, name='helmetdetection'),
    path('', traffic_views.index, name='index'),
    path('login', traffic_views.login, name='login'),
    path('signaljumpdetection', traffic_views.signaljumpdetection, name='signaljumpdetection'),
    path('speeddetection', traffic_views.speeddetection, name='speeddetection'),
    path('tripleridedetection', traffic_views.tripleridedetection, name='tripleridedetection'),
    path('signaljumpform', traffic_views.signaljumpform, name='signaljumpform'),
    path('triplerideform', traffic_views.triplerideform, name='triplerideform'),
    path('helmetform', traffic_views.helmetform, name='helmetform'),
    path('logout', traffic_views.logout, name='logout'),
]
