# Generated by Django 2.2 on 2020-09-12 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Project_1_App', '0010_auto_20200907_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='Project_1_App/templates/images/message_image'),
        ),
    ]
