import MySQLdb
from datetime import datetime, timedelta
import logging

logging.basicConfig(filename='WeatherGUILog.log', level=logging.DEBUG)



class Forecast_Aggregate:
    def __init__(self, date):
        self.list = []
        self.date = date

    def add_forecast(self, Forecast):
        self.list.append(Forecast)

    def get_date(self):
        return self.date


class Forecast:
    def __init__(self, date):
        self.list = []
        self.date = date

    def add_hourly(self, hour_forecast):
        self.list.append(hour_forecast)

    def print_forecast(self):
        for item in self.list:
            item.print_forecast()

    def hours_list(self):
        hours = []
        for item in self.list:
            hours.append(str(item.get_hour()))
        return hours

    def temp_list(self):
        temps = []
        for item in self.list:
            temps.append(item.get_temp())
        return temps

    def wind_list(self):
        wind = []
        for item in self.list:
            wind.append(item.get_wind_speed())
        return wind

    def precip_list(self):
        precip = []
        for item in self.list:
            precip.append(item.get_precip_chance())
        return precip

    def get_date(self):
        return self.date


class HourForecast:
    # Creates location with id, name, address, and a default distance of 0. This number will change for locations inside
    # the neighbors dictionary. The neighbors dictionary includes a location's specific neighbors and their distances
    # from the location.
    # O(1)
    def __init__(self, hour, temperature, precip_chance, wind_direction, wind_speed):
        self.hour = hour
        self.temperature = temperature
        self.precip_chance = precip_chance
        self.wind_direction = wind_direction
        self.wind_speed = wind_speed

    def get_hour(self):
        hour = self.hour.hour
        return hour

    def get_temp(self):
        return self.temperature

    def get_precip_chance(self):
        return self.precip_chance

    def get_wind_direction(self):
        return self.wind_direction

    def get_wind_speed(self):
        return self.wind_speed

    def print_forecast(self):
        print(
            "At " + self.hour + ", it will be " + self.temperature + " degrees with a " + self.precip_chance + " chance of rain and the wind"
                                                                                                               " will be " + self.wind_speed + " " + self.wind_direction)


def Get_Forecasts(date):
    try:
        hour = date.strftime("%H")
        while not (hour == '08' or hour == '20'):
            date = date - timedelta(hours=1)
            hour = date.strftime("%H")
        nextDate = date + timedelta(hours=12)
        date = date.replace(minute=00, second=00)
        nextDate = nextDate.replace(minute=00, second=00)
        date = date.strftime("%Y-%m-%d %H:%M:%S")
        nextDate = nextDate.strftime("%Y-%m-%d %H:%M:%S")
        host = "*********"
        user = "admin"
        db = "WeatherData"
        my_db = MySQLdb.connect(host="*********", user="admin",
                                passwd="*****", db="WeatherData")
        c = my_db.cursor()
        c.execute("""SELECT * FROM WeatherData.KY3Forecast WHERE capturetime BETWEEN %s AND %s;""", (date, nextDate))
        hours = c.fetchall()
        KY3Forecast = Forecast(date)
        Hour_Forecast = HourForecast(0, 0, 0, 0, 0)
        for item in hours:
            Hour_Forecast = HourForecast(item[5], item[1], float(item[4].strip('%')), item[3], item[2])
            KY3Forecast.add_hourly(Hour_Forecast)
        c.execute("""SELECT * FROM WeatherData.NWS WHERE capturetime BETWEEN %s AND %s;""", (date, nextDate))
        hours = c.fetchall()
    except MySQLdb.Error:
        logging.debug(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' - SQL Error while attempting to gather forecast data.')
    NWSForecast = Forecast(date)
    Hour_Forecast = HourForecast(0, 0, 0, 0, 0)
    for item in hours:
        Hour_Forecast = HourForecast(item[4], item[1], 0, item[3], item[2])
        NWSForecast.add_hourly(Hour_Forecast)
    c.execute("""SELECT * FROM WeatherData.Accuweather WHERE capturetime BETWEEN %s AND %s;""", (date, nextDate))
    hours = c.fetchall()
    AccuweatherForecast = Forecast(date)
    Hour_Forecast = HourForecast(0, 0, 0, 0, 0)
    for item in hours:
        Hour_Forecast = HourForecast(item[5], item[1], float(item[4].strip('%')), item[3], item[2])
        AccuweatherForecast.add_hourly(Hour_Forecast)
    All_Forecasts = Forecast_Aggregate(KY3Forecast.get_date())
    All_Forecasts.add_forecast(KY3Forecast)
    All_Forecasts.add_forecast(NWSForecast)
    All_Forecasts.add_forecast(AccuweatherForecast)
    return All_Forecasts


def Get_Realized_Data(date):
    try:
        hour = date.strftime("%H")
        while not (hour == '08' or hour == '20'):
            date = date - timedelta(hours=1)
            hour = date.strftime("%H")
        nextDate = date + timedelta(hours=19)
        date = date + timedelta(hours=7)
        date = date.replace(minute=00, second=00)
        nextDate = nextDate.replace(minute=00, second=00)
        date = date.strftime("%Y-%m-%d %H:%M:%S")
        nextDate = nextDate.strftime("%Y-%m-%d %H:%M:%S")
        host = "*********"
        user = "admin"
        db = "WeatherData"
        my_db = MySQLdb.connect(host="*********", user="admin",
                                passwd="*********", db="WeatherData")
        c = my_db.cursor()
        c.execute(
            """SELECT * FROM WeatherData.Readings WHERE (timestamp BETWEEN %s AND %s) AND (MINUTE(timestamp) = 00);""",
            (date, nextDate))
        hours = c.fetchall()
    except MySQLdb.Error:
        logging.debug(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' - Error gathering data from WeatherData.Readings database')
        pass
    RealizedForecast = Forecast(date)
    for item in hours:
        hour = item[1]
        temp = item[7] * 1.8 + 32
        precip = item[5]
        direction = item[4].strip()
        speed = item[2]  # 0.62137
        Hour_Forecast = HourForecast(hour, temp, precip, direction, speed)
        RealizedForecast.add_hourly(Hour_Forecast)
    for x in range(len(RealizedForecast.list)):
        first = RealizedForecast.precip_list()[x]
        first_test = RealizedForecast.precip_list()
        try:
            second = RealizedForecast.precip_list()[x + 1]
        except IndexError:
            RealizedForecast.list[x].precip_chance = RealizedForecast.list[x - 1].precip_chance
            break
        if first < second:
            first = 100
            RealizedForecast.list[x].precip_chance = first
        else:
            first = 0
            RealizedForecast.list[x].precip_chance = first
    return RealizedForecast
