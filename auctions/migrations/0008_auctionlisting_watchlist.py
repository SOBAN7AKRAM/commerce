# Generated by Django 5.0.2 on 2024-03-22 14:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_auctionlisting_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='watchList',
            field=models.ManyToManyField(default='', related_name='watchList', to=settings.AUTH_USER_MODEL),
        ),
    ]
