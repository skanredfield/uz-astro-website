import datetime

from django.db import models
from django.utils import timezone

# dataGMTTime=2019/05/30 10:19:54
# cwinfo=Serial: 1526, FW: 5.7
# clouds=-6.730000
# temp=27.950000
# wind=8
# gust=9
# rain=5120
# light=2
# switch=1
# safe=1
# hum=6
# dewp=-12.960000

class WeatherData(models.Model):
    reading_date = models.DateTimeField("reading date")
    cwinfo = models.CharField(max_length=200)
    clouds_level = models.FloatField(default=0.0)
    temperature = models.FloatField(default=0.0)
    wind_level = models.IntegerField(default=0)
    wind_gust_level = models.IntegerField(default=0)
    rain_level = models.IntegerField(default=0)
    light_level = models.IntegerField(default=0)
    roof_safe_to_open = models.BooleanField(default=False)
    weather_permits_observations = models.BooleanField(default=False)
    humidity_level = models.IntegerField(default=0)
    dew_point = models.FloatField(default=0.0)

    def was_published_recently(self):
        # now = timezone.now()
        now = datetime.datetime.now(datetime.timezone.utc)
        return now - datetime.timedelta(days=1) <= self.reading_date <= now

    def get_text(self) -> str:
        return "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(
            str(self.reading_date),  
            self.cwinfo,  
            str(self.clouds_level),  
            str(self.temperature),  
            str(self.wind_level),  
            str(self.wind_gust_level),  
            str(self.rain_level),  
            str(self.light_level),
            1 if self.roof_safe_to_open else 0,
            1 if self.weather_permits_observations else 0,
            str(self.humidity_level),  
            str(self.dew_point)
        )
    
    def get_formatted_datetime(self):
        return self.reading_date.strftime("%m/%d/%Y, %H:%M:%S")

    def __str__(self) -> str:
        return str(self.reading_date)

