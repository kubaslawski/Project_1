from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.paginator import Paginator 
# Create your views here.
from .models import Category, Institution, Donation
from django.db.models import Sum, Count
import random 


#Homepage
class LandingPage(View):
    def get(self, request):
        #total quantity count
        tq = Donation.objects.aggregate(total_q=Sum('quantity'))
        total_quantity = tq['total_q']
        #total supported organizations count
        ti = Donation.objects.values('institution_id').annotate(total_i=Count('institution_id'))
        total_institutions = len(ti)
        #fundations 
        fundations = Institution.objects.filter(type='1')
        fu = []
        for obj in fundations:
            fu.append(obj)
        random.shuffle(fu)
        paginator1 = Paginator(fu, 5)
        page = request.GET.get('page')
        fdt = paginator1.get_page(page)
        #NGO
        ngos = Institution.objects.filter(type='2')
        ng = []
        for n in ngos:
            ng.append(n)
        random.shuffle(ng)
        paginator2 = Paginator(ng, 5)
        page = request.GET.get('page')
        ngt = paginator2.get_page(page)
        #lokal charities
        lcs = Institution.objects.filter(type='3')
        lc = []
        for l in lcs:
            lc.append(l)
        random.shuffle(lc)
        paginator3 = Paginator(lc, 5)
        page = request.GET.get('page')
        lct = paginator3.get_page(page)    
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