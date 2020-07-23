from django import forms
from .models import Category, Institution, Donation 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


category_choices = [(c.id, c.name)
                    for c in Category.objects.all()]

institution_choices = [(i.id, i.name)
                      for i in Institution.objects.all()]

type_of_organization =  (
    ('1', "Fundacja"),
    ('2', "Organizacja pozarządowa"),
    ('3', "Zbiórka lokalna"),
)    



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User 
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class UserLoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)

    class Meta:
        model = User 
        fields = ('username', 'password')
#Donation (form.html)
class CategoryDonationForm(forms.Form):
    categories = forms.MultipleChoiceField(choices=category_choices, widget=forms.CheckboxSelectMultiple)

class InstitutionDonationForm(forms.Form):
    institutions = forms.ChoiceField(choices=institution_choices)


class ProfileSettingsForm(forms.Form):
    first_name = forms.CharField(label="imię", required=True, widget=forms.TextInput())
    last_name = forms.CharField(label="nazwisko", required=True, widget=forms.TextInput())
    username = forms.CharField(label="nazwa użytkownika", required=True, widget=forms.TextInput())
    password = forms.CharField(label="hasło", required=True, widget=forms.PasswordInput())
    
    class Meta:
        model = User 
        fields = ('first_name', 'last_name', 'username', 'password')

class AddFundationForm(forms.Form):
    type = forms.ChoiceField(choices=type_of_organization)
    categories = forms.MultipleChoiceField(choices=category_choices, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Institution
        fields = ('type', 'categories')

