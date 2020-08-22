from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    
type_of_organization = (
    ('1', "Fundacja"),
    ('2', "Organizacja pozarządowa"),
    ('3', "Zbiórka lokalna"),
)


class Institution(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    type = models.CharField(choices=type_of_organization, default=1, max_length=32)
    categories = models.ManyToManyField(Category)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=16)
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=16)
    pick_up_date = models.DateField(null=True, blank=True)
    pick_up_time = models.DateTimeField(null=True, blank=True)
    pick_up_comment = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_taken = models.BooleanField(default=False)

type_of_message = (
    ('1', "Notification"),
    ('2', "Private Message"),
)

class Message(models.Model):
    send_from = models.ForeignKey(User,on_delete=models.CASCADE, related_name="send_from")
    send_to = models.ForeignKey(User,on_delete=models.CASCADE, related_name="send_to")
    subject = models.CharField(choices=type_of_message)
    context = models.TextField()
    timestamp = models.DataTimeField(auto_now_add=True)

@receiver(pre_delete, sender=User)
def delete_user(sender, instance, **kwargs):
    if instance.is_superuser:
        raise PermissionDenied

