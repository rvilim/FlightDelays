import getweather
import datetime

print getweather.getforecast(datetime.date.today()+datetime.timedelta(days=1), 10279)