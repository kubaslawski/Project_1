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
from django.urls import path, re_path, include
from Project_1_App import views
from django.conf.urls import url
#views
from Project_1_App import views as ex_views
from Project_1_App.views import LandingPage, signup, activate
from django.contrib.auth import views as auth_views
from Project_1_App.forms import EmailValidationOnForgotPassword

urlpatterns = [
    #AJAX REQUEST FORM
    url(r'^ajax/validate_categories/$', views.validate_categories, name='validate_categories'),
    #api
    path(r'^api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    #1.2
    path('', ex_views.LandingPage.as_view(), name="base"),
    path('form/', ex_views.AddDonation.as_view(), name="add_donation"),
    path('add_fundation/', ex_views.AddFundation.as_view(), name="add_fundation"),
    path('form_confirmation/', ex_views.DonationFormConfirmationView.as_view(), name="form-confirmation"),
    path('donate/<int:donate_id>', ex_views.DonateView.as_view(), name="donate"),
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
    #forgotten password
    path('reset_password/',
         auth_views.PasswordResetView.as_view(form_class=EmailValidationOnForgotPassword, template_name="password_reset/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="password_reset/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset/password_reset_complete.html"),
         name="password_reset_complete"),
 ]
