# Generated by Django 5.0.2 on 2024-03-23 00:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_rename_watchproduct_watchlist_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='products',
            field=models.ManyToManyField(to='auctions.auctionlisting'),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='watchUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
