# Generated by Django 3.1.7 on 2021-04-09 16:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='uploaded_by',
        ),
        migrations.AlterField(
            model_name='auther',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_auther', to=settings.AUTH_USER_MODEL),
        ),
    ]