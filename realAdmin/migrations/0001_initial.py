# Generated by Django 2.1.1 on 2019-03-22 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hospitals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hospital_name', models.CharField(max_length=40)),
                ('country', models.CharField(max_length=40)),
                ('district', models.CharField(max_length=40)),
                ('hospital_type', models.CharField(max_length=40)),
                ('email', models.EmailField(blank=True, max_length=40)),
                ('phone_number', models.CharField(blank=True, max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='speciality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spec1', models.CharField(blank=True, max_length=30)),
                ('spec2', models.CharField(blank=True, max_length=30)),
                ('spec3', models.CharField(blank=True, max_length=30)),
                ('hospitals', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='realAdmin.Hospitals')),
                ('persons', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.Persons')),
            ],
        ),
    ]
