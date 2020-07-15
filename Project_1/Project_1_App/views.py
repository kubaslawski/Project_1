from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
# Create your views here.


#Homepage
class LandingPage(View):
    def get(self, request):
        return render(request, "index.html")


class AddDonation(View):
    def get(self, request):
        return render(request, "form.html")


class Login(View):
    def get(self, request):
        return render(request, "login.html")


class Register(View):
    def get(self, request):
        return render(request, "register.html")