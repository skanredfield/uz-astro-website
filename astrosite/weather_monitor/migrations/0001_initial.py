# Generated by Django 4.2 on 2023-04-20 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reading_date', models.DateTimeField(verbose_name='reading date')),
                ('cwinfo', models.CharField(max_length=200)),
                ('clouds_level', models.FloatField(default=0.0)),
                ('temperature', models.FloatField(default=0.0)),
                ('wind_level', models.IntegerField(default=0)),
                ('wind_gust_level', models.IntegerField(default=0)),
                ('rain_level', models.IntegerField(default=0)),
                ('light_level', models.IntegerField(default=0)),
                ('roof_safe_to_open', models.BooleanField(default=False)),
                ('weather_permits_observations', models.BooleanField(default=False)),
                ('humidity_level', models.IntegerField(default=0)),
                ('dew_point', models.FloatField(default=0.0)),
            ],
        ),
    ]
