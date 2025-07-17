"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from core.views import pilotos, lista_escuderias, carreras_view, register_view, login_view, logout_view, season_list, race_list, blog_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',carreras_view, name='carreras'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('season/', season_list, name='season-list'),
    path('<int:year>/', race_list, name='race-list'),
    path('pilotos/', pilotos, name='pilotos'),
    path('escuderias/', lista_escuderias, name='lista_escuderias'),
    path('blog/', blog_view, name='blog'),
]
