# Generated by Django 4.2.7 on 2023-11-06 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('standard_capacity', models.IntegerField()),
                ('adult_price', models.IntegerField(max_length=6)),
                ('child_price', models.IntegerField(max_length=6)),
                ('infant_price', models.IntegerField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('price', models.IntegerField(max_length=6)),
                ('available', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calendar_app.product')),
            ],
        ),
    ]
