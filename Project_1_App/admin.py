from django.contrib import admin
from .models import Institution, Donation, Category, Message
# Register your models here.

class InstitutionAdmin(admin.ModelAdmin):
    model = Institution

    class Meta:
        model = Institution

admin.site.register(Institution, InstitutionAdmin)


class CategoryAdmin(admin.ModelAdmin):
    model = Category 

    class Meta:
        model = Category 

admin.site.register(Category, CategoryAdmin)


class DonationAdmin(admin.ModelAdmin):
    model = Donation 

    class Meta:
        model = Donation 

admin.site.register(Donation, DonationAdmin)

class MessageAdmin(admin.ModelAdmin):
    model = Message 

    class Meta:
        model = Message 

admin.site.register(Message, MessageAdmin)