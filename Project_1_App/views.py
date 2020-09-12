from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Institution, Donation, Message
from django.db.models import Sum, Count
import random
from .forms import SignUpForm, UserLoginForm, CategoryDonationForm, \
     ProfileSettingsForm, InstitutionDonationForm
from .forms import AddFundationForm, AddInstitutionForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
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
        t_q = Donation.objects.filter(user=request.user.id)
        tq_u = t_q.aggregate(total_q=Sum('quantity'))
        total_quantity = tq_u['total_q']
        #total supported organizations count
        t_i = Donation.objects.values('institution_id').annotate(total_i=Count('institution_id'))
        total_institutions = len(t_i)
        ctx = {
            "total_quantity": total_quantity,
            "total_institutions": total_institutions,
        }
        type_1 = Institution.objects.filter(type=1)
        p_1 = Paginator(type_1, 3)
        page_number = request.GET.get('page')
        page_obj_1 = p_1.get_page(page_number)
        type_2 = Institution.objects.filter(type=2)
        p_2 = Paginator(type_2, 3)
        page_obj_2 = p_2.get_page(page_number)
        type_3 = Institution.objects.filter(type=3)
        p_3 = Paginator(type_3, 3)
        page_obj_3 = p_3.get_page(page_number)
        try:
            user_foundation = Institution.objects.get(owner_id=request.user.id)
        except:
            user_foundation = None
        #unread messages 
        unread_messages = Message.objects.filter(send_to=request.user.id).filter(is_read=False).count()
            
        ctx = {
            "total_quantity": total_quantity,
            "total_institutions": total_institutions,
            "page_obj_1": page_obj_1,
            "page_obj_2": page_obj_2,
            "page_obj_3": page_obj_3,
            "user_foundation": user_foundation,
            "unread_messages": unread_messages,

        }
        return render(request, "index.html", ctx)

    def post(self, request):
        first_name = request.POST.get('name')
        last_name = request.POST.get('surname')
        text = request.POST.get('message')
        email_from = "kubaslawski.webdeveloper@gmail.com"
        email_to = 'kubaslawski.webdeveloper@gmail.com'
        print(type(email_from))
        send_mail(
            'CONTACT  ' + str(first_name) + '  ' +str(last_name),
            text,
            'kubaslawski@gmail.com',
            [email_to],
            fail_silently=False,
        )
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
        ctx = {
            "form1": form1,
        }
        return render(request, "form.html", ctx)

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
        ctx = {
            "form1": form1
        }
        if categories1 and institutions1 and quantity1 and address1 and \
            city1 and code1 and phone1 and user1:
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
            if Institution.objects.get(id=institutions1).owner:
                m = Message()
                m.send_from_id = request.user.id
                m.send_to_id  = Institution.objects.get(id=institutions1).owner.id
                m.type = 1 
                m.subject = "New donation"
                m.context = "New donation has been given to your foundation!" \
                    + "Quantity: {} bags".format(quantity1) \
                        + "Address: {}, {}, {}, {} ".format(address1, city1, code1, phone1) \
                            + "Date: {} + Comments: {}".format(time1, com1)
                print(m.send_from_id, m.send_to_id, m.type, m.subject)
                m.save()
            return redirect('base')
        return render(request, "form.html", ctx)


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
        if request.POST['submit'] == 'False':
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
        return HttpResponse('Thank you for your email confirmation. \
            Now you can login your account.')
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
        all_donations_not_taken = Donation.objects.filter\
            (user_id=request.user.id).filter(is_taken=False)
        all_donations_taken = Donation.objects.filter\
            (user_id=request.user.id).filter(is_taken=True)
        all_donations = Donation.objects.filter(user_id=request.user.id).count()
        #num of bags
        donation_quantity = Donation.objects.filter(user_id=request.user.id)
        dq = donation_quantity.aggregate(total=Sum('quantity'))
        dq_total = dq['total']
        #num of supported org.
        supp_fund = len(Donation.objects.filter\
            (user_id=request.user.id).values('institution_id').annotate\
                (total=Count('institution_id')))
        bag_per_fund = Donation.objects.filter\
            (user_id=request.user.id).values('institution__name').annotate\
                (total=Sum('quantity'))
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
            first_name1 = form1.cleaned_data.get('first_name')
            last_name1 = form1.cleaned_data.get('last_name')
            username1 = form1.cleaned_data.get('username')
            password1 = form1.cleaned_data.get('password')
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
                    form1.add_error(None, "Niepoprawne dane")
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
        donators = Donation.objects.filter(institution=ins.id)
        #users with highest num of donation
        elements = Donation.objects.filter(institution=ins.id).order_by('quantity')
        donationlist = {}
        for el in elements:
            donation = el.quantity
            user = el.user
            if user not in donationlist:
                donationlist[user]=donation
            else:
                previousdonation = donationlist[user]
                sum = previousdonation + donation 
                donationlist[user] = sum 
        first5pairs = {k: donationlist[k] for k in list(donationlist)[:5]}
        print(first5pairs)
        return render(request, "my_foundations.html", locals())

class DonationOfFoundation(View):
    def get(self, request, institution_id):
        donations = Donation.objects.filter(institution_id=institution_id).order_by('pick_up_time')
        taken = donations.filter(is_taken=True)
        not_taken = donations.filter(is_taken=False)
        return render(request, "donations_details.html", locals())


def taken_or_not_taken(request):
    obj = request.POST['donation_number']
    data = {
        "id": obj
    }
    donate = Donation.objects.get(id=obj)
    if donate.is_taken == True:
        donate.is_taken = False
        donate.save()
    elif donate.is_taken == False:
        donate.is_taken = True
        donate.save()
    return JsonResponse(data)

def checkedmessages(request):
    obj = request.GET.get['CheckedMessagesArr']
    data = {
        "id": obj
    }
    print(obj)
    for num in obj:
        Message.objects.get(id=int(num)).is_read = True 

class MessageInboxView(View):
    def get(self, request):
        messages_inbox = Message.objects.filter(send_to=request.user.id).order_by('-timestamp')
        messages_starred = Message.objects.filter(send_to=request.user.id).filter(starred=True)
        messages_important = Message.objects.filter(send_to=request.user.id).filter(important=True)
        messages_sent = Message.objects.filter(send_from=request.user.id)
        messages_draft = Message.objects.filter(draft=True).filter(send_from=request.user.id)
        messages_spam = Message.objects.filter(spam=True)
        unread_messages = Message.objects.filter(is_read=False).filter(send_to=request.user.id).count()
        unread_starred = Message.objects.filter(is_read=False).filter(send_to=request.user.id).filter(starred=True).count()
        unread_important = Message.objects.filter(is_read=False).filter(send_to=request.user.id).filter(important=True).count()
        unread_spam = Message.objects.filter(is_read=False).filter(send_to=request.user.id).filter(spam=True).count()
        ctx = {
            "messages_inbox": messages_inbox,
            "messages_starred": messages_starred,
            "messages_important": messages_important,
            "messages_sent": messages_sent,
            "messages_draft": messages_draft,
            "messages_spam": messages_spam,
            "unread_messages": unread_messages,
            "unread_starred": unread_starred,
            "unread_important": unread_important,
            "unread_spam": unread_spam,
        }   
        return render(request, "messages/inbox.html", ctx)

    def post(self, request):
        user_email = request.POST.get('to')
        user_to = User.objects.get(email=user_email).id
        subject = request.POST.get('subject')
        context = request.POST.get('message')
        if user_email and subject and context:
            m = Message()
            m.send_from_id = request.user.id
            m.send_to_id = user_to
            m.subject = subject
            m.context = context 
            m.type = 2 
            m.save()
        return render(request, "messages/inbox.html")


class MessageView(View):
    def get(self, request, message_id):
        messages_inbox = Message.objects.filter(send_to=request.user.id).order_by('-timestamp')
        messages_starred = Message.objects.filter(send_to=request.user.id).filter(starred=True)
        messages_important = Message.objects.filter(send_to=request.user.id).filter(important=True)
        messages_sent = Message.objects.filter(send_from=request.user.id)
        messages_draft = Message.objects.filter(draft=True).filter(send_from=request.user.id)
        messages_spam = Message.objects.filter(spam=True)
        unread_messages = Message.objects.filter(is_read=False).filter(send_to=request.user.id).count()
        unread_starred = Message.objects.filter(is_read=False).filter(send_to=request.user.id).filter(starred=True).count()
        unread_important = Message.objects.filter(is_read=False).filter(send_to=request.user.id).filter(important=True).count()
        unread_spam = Message.objects.filter(is_read=False).filter(send_to=request.user.id).filter(spam=True).count()
        message = Message.objects.get(id=message_id)
        send_from = User.objects.get(id=message.send_from_id).email
        ctx = {
            "messages_inbox": messages_inbox,
            "messages_starred": messages_starred,
            "messages_important": messages_important,
            "messages_sent": messages_sent,
            "messages_draft": messages_draft,
            "messages_spam": messages_spam,
            "unread_messages": unread_messages,
            "unread_starred": unread_starred,
            "unread_important": unread_important,
            "unread_spam": unread_spam,
            "message": message,
            "send_from": send_from,
        }   
        if message.send_to_id == request.user.id:
            message.is_read = True
            message.save()
        return render(request, "messages/message.html", ctx)

    def post(self, request, message_id):
        user_email = request.POST.get('to')
        user_to = User.objects.get(email=user_email).id
        subject = request.POST.get('subject')
        context = request.POST.get('message')
        if user_email and subject and context:
            m = Message()
            m.send_from_id = request.user.id
            m.send_to_id = user_to
            m.subject = subject
            m.context = context 
            m.type = 2 
            m.save()
        return render(request, "messages/message.html")