from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
# Create your views here.
from .models import Category, Institution, Donation
from django.db.models import Sum, Count


#Homepage
class LandingPage(View):
    def get(self, request):
        #total quantity count
        tq = Donation.objects.aggregate(total_q=Sum('quantity'))
        total_quantity = tq['total_q']
        #total supported organizations count
        ti = Donation.objects.values('institution_id').annotate(total_i=Count('institution_id'))
        total_institutions = len(ti)
        return render(request, "index.html", locals())





class AddDonation(View):
    def get(self, request):
        return render(request, "form.html")


class Login(View):
    def get(self, request):
        return render(request, "login.html")


class Register(View):
    def get(self, request):
        return render(request, "register.html")