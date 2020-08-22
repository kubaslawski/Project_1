# Generated by Django 2.2 on 2020-08-22 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Project_1_App', '0003_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='type',
            field=models.CharField(choices=[('1', 'Notification'), ('2', 'Private Message')], default=1, max_length=32),
        ),
        migrations.AlterField(
            model_name='message',
            name='subject',
            field=models.CharField(max_length=128),
        ),
    ]
