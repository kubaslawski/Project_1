from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy 
from django.contrib.auth.models import User
from django.http import JsonResponse
# Create your views here.
from .models import Category, Institution, Donation
from django.db.models import Sum, Count
import random 
#forms
from .forms import SignUpForm, UserLoginForm, CategoryDonationForm, ProfileSettingsForm, InstitutionDonationForm
from .forms import AddFundationForm, AddFundationForm, AddInstitutionForm
#django contrib
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
#Mail confirmation, signup & login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.core.mail import BadHeaderError

#Homepage
class LandingPage(View):
    def get(self, request):
        #total quantity count
        tq = Donation.objects.filter(user=request.user.id)
        tq_u = tq.aggregate(total_q=Sum('quantity'))
        total_quantity = tq_u['total_q']
        #total supported organizations count
        ti = Donation.objects.values('institution_id').annotate(total_i=Count('institution_id'))
        total_institutions = len(ti)
        #foundations
        #dobrze 
        foundations = Institution.objects.filter(type='1')
        paginator1 = Paginator(foundations, 3)
        page = request.GET.get('page')
        fdt = paginator1.get_page(page)
        # brak informacji na której zakładace znajduje się użytkownik
        #NGO
        #źle
        ngos = Institution.objects.filter(type='2')
        ng = []
        for n in ngos:
            ng.append(n)
        random.shuffle(ng)
        paginator2 = Paginator(ng, 5)
        page = request.GET.get('page')
        ngt = paginator2.get_page(page)
        #local charities
        lcs = Institution.objects.filter(type='3')
        lc = []
        for l in lcs:
            lc.append(l)
        random.shuffle(lc)
        paginator3 = Paginator(lc, 5)
        page = request.GET.get('page')
        lct = paginator3.get_page(page)    
        return render(request, "index.html", locals())
    def post(self, request):
        first_name = request.POST.get('contact-first-name')
        last_name = request.POST.get('contact-last-name')
        text = request.POST.get('message')
        email = request.user.email
        print(text, email)
        try:
            send_mail(
            'CONTACT',
            text,
            [email],
            ['kubaslawski.webdeveloper@gmail.com'],
            fail_silently=False,
            )
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return render(request, "base.html")

#Wczytać instytucje



def validate_categories(request):
    obj = request.GET.get('categories', '')
    print(obj)
    import json
    obj: list[int] = json.loads(obj)
    qs = Institution.objects.filter(categories__in=obj)
    return JsonResponse({institution.name: institution.id for institution in qs})


#TO DO
class AddDonation(View):
    def get(self, request):
        form1 = CategoryDonationForm()
        # Tylko jeden formularz 
        return render(request, "form.html",locals())

    def post(self, request):
        form1 = CategoryDonationForm(request.POST)
        if form1.is_valid():
            categories1 = form1.cleaned_data.get('categories')
        quantity1 = request.POST.get('bags')    
        institutions1 = request.POST.get('insId')
        #other data
        address1 = request.POST.get('address')
        city1 = request.POST.get('city')
        code1 = request.POST.get('postcode')
        phone1 = request.POST.get('phone')
        data1 = request.POST.get('data')
        time1 = request.POST.get('time')
        com1 = request.POST.get('more_info')
        user1 = request.user.id 
        email = request.user.email
        if categories1 and institutions1 and quantity1 and address1 and city1 and code1 and phone1 and user1:
            #Insert a message if donate is lacking some needed informations
            d = Donation()
            d.quantity = quantity1
            d.institution_id = institutions1
            d.address = address1
            d.phone_number = phone1
            d.city = city1
            d.zip_code = code1
            d.pick_up_date = data1
            d.pick_up_time = data1 + " " + time1
            d.pick_up_comment = com1
            d.user_id = user1 
            d.save()
            d.categories.set(categories1)
            return redirect('base')
        return render(request, "form.html", locals())


class DonationFormConfirmationView(View):
    def get(self, request):
        return render(request, "form-confirmation.html")     

    def post(self, request):
        return render(request, "form-confirmation.html")   


class AddFundation(View):
    def get(self, request):
        form1 = AddFundationForm()
        return render(request, 'add_fundation.html', locals())
        
    def post(self, request):
        form1 = AddFundationForm(request.POST)
        name1 = request.POST.get('name')
        description1 = request.POST.get('description')
        if form1.is_valid(): # uruchomienie walidacji
            type1 = form1.cleaned_data.get('type')
            category1 = form1.cleaned_data.get('categories')
            if type1 and category1 and name1 and description1:
                i = Institution()
                i.name = name1 
                i.description = description1
                i.type = type1 
                i.save()
                i.categories.set(category1)
        return render(request, 'add_fundation.html', locals())


class DonateView(View):
    def get(self, request):
        donate = Donation.objects.filter(user_id=request.user.id)
        return render(request, "donate.html", locals())

    def post(self, request):
        if request.POST['submit']=='False':
            d = Donation()
            d.id = request.POST['submit']
            print(d.id)
            return render(request, "donate.html", locals())




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
            user_email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            obj = User.objects.get(email=user_email)
            username = obj.username
            user = authenticate(username=username, password=password)
            if user is not None:
            # podwójne zaprzeczenie, ustawić na odwrót
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
        all_donations_not_taken = Donation.objects.filter(user_id=request.user.id).filter(is_taken=False)
        all_donations_taken = Donation.objects.filter(user_id=request.user.id).filter(is_taken=True)
        all_donations = Donation.objects.filter(user_id=request.user.id).count()
        #num of bags
        donation_quantity = Donation.objects.filter(user_id=request.user.id)
        dq = donation_quantity.aggregate(total=Sum('quantity'))
        dq_total = dq['total']
        #num of supported org.
        supp_fund = len(Donation.objects.filter(user_id=request.user.id).values('institution_id').annotate(total=Count('institution_id')))
        bag_per_fund = Donation.objects.filter(user_id=request.user.id).values('institution__name').annotate(total=Sum('quantity'))
        return render(request, "profile.html", locals())
    
    def post(self, request):
        id = request.POST.get('taken_or_not')
        print(id)
        d = Donation.objects.get(id=id)
        if d.is_taken == False:
            d.is_taken = True
            d.save()
            return redirect('user_profile')
        else:
            d.is_taken = False
            d.save()
            return redirect('user_profile')
        return render(request, "profile.html", locals())

class UserSettingsView(View):
    def get(self, request):
        form1 = ProfileSettingsForm()
        form2 = PasswordChangeForm(request.user)
        return render(request, "settings.html", locals())

    def post(self, request):
        form1 = ProfileSettingsForm(request.POST)
        if form1.is_valid(): # uruchomienie walidacji
            first_name1 = form.cleaned_data.get('first_name')
            last_name1 = form.cleaned_data.get('last_name')
            username1 = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password')
            user = authenticate(username=username1, password=password1)
            if user is not None:
                if user.is_active:
                    if first_name1 and last_name1 and username1:
                        u = User.objects.get(id=request.user.id)
                        u.first_name = form1.cleaned_data.get('first_name')
                        u.last_name = form1.cleaned_data.get('last_name')
                        u.username = form1.cleaned_data.get('username')
                        u.save()
                    return HttpResponse('Ustawienia zapisane')
                else:
                    form.add_error(None, "Niepoprawne dane")
            else:
                return HttpResponse('Niepoprawne hasło')
        form2 = PasswordChangeForm(request.user, request.POST)
        if form2.is_valid():
            user = form2.save()
            update_session_auth_hash(request, user)  # Important!
            return HttpResponse('Ustawienia zapisane')
        else:
            messages.error(request, 'Please correct the error below.')
        return render(request, "settings.html", {'form2': form2})
        
class MyFoundationsView(View):
    def get(self, request):
        #institution of user 
        institutions = Institution.objects.filter(owner=request.user.id)
        ins = institutions[0]
        donations = Donation.objects.filter(institution=ins.id)
        #list of donating users 
        users_who_donated = []
        for d in donations:
            users_who_donated.append(d.user)
        def remove_duplicates(x):
            return list(dict.fromkeys(x))
        users_who_donated = remove_duplicates(users_who_donated)
        #total quantity of donated bags 
        donation_quantity = Donation.objects.filter(institution_id=ins)
        dq = donation_quantity.aggregate(total=Sum('quantity'))
        dq_total = dq['total']
        #num of received donations 
        donation_received = Donation.objects.filter(is_taken=True).filter(institution_id=ins)
        dr = len(donation_received)
        #num of donations to be receive
        donation_unreceived = Donation.objects.filter(is_taken=False).filter(institution_id=ins)
        dur = len(donation_unreceived)
        print(ins.id)


        return render(request, "my_foundations.html", locals())

class DonationOfFoundation(View):
    def get(self, request, institution_id):
        donations = Donation.objects.filter(institution_id=institution_id).order_by('pick_up_time')
        taken = donations.filter(is_taken=True)
        not_taken = donations.filter(is_taken=False)
        return render(request, "donations_details.html", locals())

class DonationNavbar(View):
    def get(self, request):
        institution = Institution.objects.filter(owner=request.user.id)
        ins = institutions[0]
        my_institution = Institution.objects.filter(id=ins)
        print(my_institution)
        return render(request, "my_foundations_navbar.html", {{"id": my_institution}})

def taken_or_not_taken(request):
    obj = request.POST['donation_number']
    data = {
        "id": obj
    }
    print(obj)
    donate = Donation.objects.get(id=obj)
    if donate.is_taken == True: 
        donate.is_taken = False
        donate.save()
        print('Zmienione na False')
    elif donate.is_taken == False:
        donate.is_taken = True
        donate.save()
        print('Zmieniono na True')
    return JsonResponse(data)
    