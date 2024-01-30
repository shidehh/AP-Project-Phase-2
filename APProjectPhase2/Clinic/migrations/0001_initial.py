# Generated by Django 4.0 on 2024-01-30 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('capacity', models.IntegerField()),
                ('service', models.CharField(max_length=255)),
                ('clinic_reserved_appointments', models.IntegerField(default=0)),
                ('address', models.CharField(max_length=255)),
                ('clinic_contact_info', models.CharField(max_length=255)),
            ],
        ),
    ]