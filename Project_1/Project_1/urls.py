"""Project_1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
#views
from Project_1_App import views as ex_views
from Project_1_App.views import LandingPage

urlpatterns = [
    path('admin/', admin.site.urls),
    #1.2
    path('', ex_views.LandingPage.as_view(), name="base"),
    path('form/', ex_views.AddDonation.as_view(), name="add_donation"),
    path('login/', ex_views.Login.as_view(), name="login"),
    path('register/', ex_views.Register.as_view(), name="register"),
]
