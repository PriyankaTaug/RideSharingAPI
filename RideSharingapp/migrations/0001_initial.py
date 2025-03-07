# Generated by Django 4.2.7 on 2025-02-11 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DriverRegisteration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=255)),
                ('lastname', models.CharField(max_length=255)),
                ('license_number', models.CharField(max_length=50)),
                ('phonenumber', models.CharField(default=1, max_length=50)),
                ('vehicle_type', models.CharField(max_length=100)),
                ('is_available', models.BooleanField(default=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='profile')),
            ],
        ),
        migrations.CreateModel(
            name='RiderRegisteration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=255)),
                ('lastname', models.CharField(max_length=255)),
                ('phonenumber', models.CharField(default=1, max_length=50)),
                ('image', models.ImageField(blank=True, null=True, upload_to='profile')),
            ],
        ),
        migrations.CreateModel(
            name='RideTbl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_location', models.CharField(max_length=255)),
                ('drop_location', models.CharField(max_length=255)),
                ('status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Accepted'), (2, 'Ongoing'), (3, 'Completed'), (4, 'Cancelled')], default=0)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='driver_data', to='RideSharingapp.driverregisteration')),
                ('rider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rider_data', to='RideSharingapp.riderregisteration')),
            ],
        ),
        migrations.CreateModel(
            name='RiderUserTbl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('riderid', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='RideSharingapp.riderregisteration')),
            ],
        ),
        migrations.CreateModel(
            name='DriverUserTbl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('driverid', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='RideSharingapp.driverregisteration')),
            ],
        ),
    ]
