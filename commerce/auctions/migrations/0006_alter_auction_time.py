# Generated by Django 4.1.7 on 2023-05-23 00:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_auction_category_alter_auction_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]