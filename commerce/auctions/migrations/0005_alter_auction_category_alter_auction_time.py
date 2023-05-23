# Generated by Django 4.1.7 on 2023-05-22 02:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_auction_hyperlink_alter_auction_starting_bid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='category',
            field=models.CharField(blank=True, choices=[('F', 'fashion'), ('T', 'toys'), ('E', 'electronics'), ('H', 'home'), ('O', 'other')], max_length=30),
        ),
        migrations.AlterField(
            model_name='auction',
            name='time',
            field=models.TimeField(default=datetime.time(2, 59, 53, 516527)),
        ),
    ]