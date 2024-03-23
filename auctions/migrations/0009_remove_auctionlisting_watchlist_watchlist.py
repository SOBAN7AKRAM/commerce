# Generated by Django 5.0.2 on 2024-03-22 14:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auctionlisting_watchlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='watchList',
        ),
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('watchProduct', models.ManyToManyField(default='', related_name='watchProduct', to='auctions.auctionlisting')),
                ('watchUser', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='watchUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
