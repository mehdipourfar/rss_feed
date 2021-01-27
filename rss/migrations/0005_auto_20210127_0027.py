# Generated by Django 3.1.5 on 2021-01-27 00:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rss', '0004_auto_20210126_0212'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='marked_by',
            field=models.ManyToManyField(related_name='marked_entries', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='entry',
            name='read_by',
            field=models.ManyToManyField(related_name='read_entries', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='entry',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='entries', to='rss.channel'),
        ),
    ]
