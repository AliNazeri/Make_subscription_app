# Generated by Django 5.0.6 on 2024-06-06 13:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscriber_name', models.CharField(max_length=255)),
                ('subscription_plan', models.CharField(choices=[('P', 'Premium'), ('S', 'Standard')], max_length=1)),
                ('subscription_cost', models.CharField(max_length=50)),
                ('paypal_susbscription_id', models.CharField(max_length=300)),
                ('is_active', models.BooleanField(default=False)),
                ('subscriber_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
