# Generated by Django 2.2 on 2020-08-24 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Project_1_App', '0005_auto_20200823_0133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='context',
            field=models.CharField(max_length=256),
        ),
    ]
