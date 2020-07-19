from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy 
from django.contrib.auth.models import User
# Create your views here.
from .models import Category, Institution, Donation
from django.db.models import Sum, Count
import random 
#forms
from .forms import SignUpForm, UserLoginForm, CategoryDonationForm
#Mail confirmation, signup & login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout

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
        form = CategoryDonationForm()
        return render(request, "form.html", locals())


class Login(View):
    def get(self, request):
        return render(request, "login.html", )


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignUpForm()
    return render(request, "register.html", {"form": form})


def activate(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class UserLoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, "login.html", {'form': form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid(): # uruchomienie walidacji
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('base'))
                else:
                    form.add_error(None, "Konto nie jest aktywne")
            else:
                return redirect(reverse('register'))
        return render(request, "login.html", {'form': form})

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('base'))


class UserProfileView(View):
    def get(self, request):
        logged_user = User.objects.get(id=request.user.id)
        #num of bags
        donation_quantity = Donation.objects.filter(user_id=request.user.id)
        dq = donation_quantity.aggregate(total=Sum('quantity'))
        dq_total = dq['total']
        #num of supported org.
        supp_fund = len(Donation.objects.filter(user_id=request.user.id).values('institution_id').annotate(total=Count('institution_id')))
        bag_per_fund = Donation.objects.filter(user_id=request.user.id).values('institution_id').annotate(Sum('quantity'))
        return render(request, "profile.html", locals())

