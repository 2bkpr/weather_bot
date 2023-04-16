class WeatherData:
    def __init__(self):
        self.__temperature = 0
        self.__real_feel = 0
        self.__state_sky = "default"
        self.__pressure = 0
        self.__wind_speed = 0
        self.__humidity = 0

    def set_temperature(self, temperature):
        self.__temperature = temperature

    def set_real_feel(self, real_feel):
        self.__real_feel = real_feel

    def set_state_sky(self, state_sky):
        self.__state_sky = state_sky

    def set_pressure(self, pressure):
        self.__pressure = pressure

    def set_wind_speed(self, wind_speed):
        self.__wind_speed = wind_speed

    def set_humidity(self, humidity):
        self.__humidity = humidity

    def get_base_info(self):
        weather_info = f"Now is {self.__state_sky}\nTemperature is {self.__temperature}°C, feels like {self.__real_feel}°C"
        return weather_info

    def get_more_info(self):
        more_info = f"Wind speed: {self.__wind_speed}m/s\nHumidity: {self.__humidity}%\nPressure: {self.__pressure}"
        return more_info
