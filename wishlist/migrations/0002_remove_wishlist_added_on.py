# Generated by Django 5.0.6 on 2024-07-14 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='added_on',
        ),
    ]
