# Generated by Django 3.2.25 on 2024-07-02 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_review_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]
