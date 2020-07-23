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
from django.urls import path, re_path
#views
from Project_1_App import views as ex_views
from Project_1_App.views import LandingPage, signup, activate

urlpatterns = [
    path('admin/', admin.site.urls),
    #1.2
    path('', ex_views.LandingPage.as_view(), name="base"),
    path('form/', ex_views.AddDonation.as_view(), name="add_donation"),
    path('add_fundation/', ex_views.AddFundation.as_view(), name="add_fundation"),
    #login/logut
    path('login/', ex_views.UserLoginView.as_view(), name="login"),
    path('logout/', ex_views.UserLogoutView.as_view(), name="logout"),
    #register
    path('register/', signup, name="register"),
    #mail confirmation 
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    #profile
    path('user_profile/', ex_views.UserProfileView.as_view(), name="user_profile"),
    path('settings/', ex_views.UserSettingsView.as_view(), name="settings"),
]
