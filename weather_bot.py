import telebot
import aiogram
import requests
import config
import pprint
import weatherData
from geopy.geocoders import Nominatim


# class InlKb:
#     def __init__(self):
#         self.inline_info_btn = aiogram.types.InlineKeyboardButton('Detailed information', callback_data='inlineBtnInfo')
#         self.inline_link_btn = aiogram.types.InlineKeyboardButton('Open on site', url="https://www.google.com/")
#         self.inline_kb = aiogram.types.InlineKeyboardMarkup().add(self.inline_info_btn, self.inline_link_btn)



bot = telebot.TeleBot(config.TOKEN)
bot_aio = aiogram.Bot(token=config.TOKEN)
dp = aiogram.Dispatcher(bot_aio)
user_weather = weatherData.WeatherData()


button_location = aiogram.types.KeyboardButton('🧭Send my location🗺️', request_location=True)
location_kb = aiogram.types.ReplyKeyboardMarkup()
location_kb.add(button_location)
location_kb1 = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_location)

inline_info_btn = aiogram.types.InlineKeyboardButton('Detailed information', callback_data='inlineBtnInfo')
inline_kb = aiogram.types.InlineKeyboardMarkup().add(inline_info_btn)


def make_inline_link_button(latitude, longitude):
    link = f"https://weather.com/weather/today/l/{latitude},{longitude}?par=google"




def get_coordinates(location_info):
    latitude = location_info["latitude"]
    longitude = location_info["longitude"]
    return latitude, longitude


def set_weather_info(latitude, longitude):
    current_weather_api_call = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon=' \
                               f'{longitude}&appid={config.WEATHER_API_KEY}&units=metric'
    res = requests.get(current_weather_api_call)
    to_json = res.json()
    pprint.pprint(to_json)

    temperature = round(to_json['main']['temp'])
    user_weather.set_temperature(temperature)

    real_feel = round(to_json['main']['feels_like'])
    user_weather.set_real_feel(real_feel)

    state_sky = to_json['weather'][0]['description']
    user_weather.set_state_sky(state_sky)

    humidity = to_json['main']['humidity']
    user_weather.set_humidity(humidity)

    wind_speed = to_json['wind']['speed']
    user_weather.set_wind_speed(wind_speed)

    pressure = to_json['main']['pressure']
    user_weather.set_pressure(pressure)

    weather_info = user_weather.get_base_info()
    return weather_info


@dp.message_handler(commands=['start'])
async def process_start_command(message: aiogram.types.Message):
    hello_message = "Hello, I'm weather bot👋.\nYou can send me your location or write the name of your " \
                    "city or village to know weather and temperature."
    await message.reply(hello_message, reply_markup=location_kb1)


@dp.message_handler(content_types=aiogram.types.ContentType.LOCATION)
async def location_message(msg: aiogram.types.Message):
    loc_info = msg.location
    latitude, longitude = get_coordinates(loc_info)
    set_weather_info(latitude, longitude)
    weather_info = user_weather.get_base_info()
    await bot_aio.send_message(msg.from_user.id, weather_info, reply_markup=inline_kb)


@dp.callback_query_handler(text='inlineBtnInfo')
async def process_callback_inline_btn(callback_query: aiogram.types.CallbackQuery):
    weather_info = user_weather.get_more_info()
    await bot_aio.send_message(callback_query.from_user.id, weather_info)


@dp.message_handler()
async def txt_message(msg: aiogram.types.Message):
    try:
        geolocator = Nominatim(user_agent=config.user_agent)
        address = msg.text
        location = geolocator.geocode(address)
        set_weather_info(location.latitude, location.longitude)
        weather_info = user_weather.get_base_info()
        await bot_aio.send_message(msg.from_user.id, weather_info, reply_markup=inline_kb)
        # print(location.address)
        # print(location.latitude, location.longitude)
    except:
        print("Address error")
        await bot_aio.send_message(msg.from_user.id, "This address does not exist")


if __name__ == '__main__':
    aiogram.executor.start_polling(dp)

    #bot.infinity_polling()

# @dp.callback_query_handler(func=lambda c: c.data == 'button1')
# async def process_callback_button1(callback_query: aiogram.types.CallbackQuery):
#     await bot.answer_callback_query(aiogram.types.CallbackQuery.id)
#     await bot.send_message(aiogram.types.CallbackQuery.from_user.id, 'Нажата первая кнопка!')


# @dp.message_handler(commands=['1'])
# async def process_command_1(message: aiogram.types.Message):
#     await message.reply("Первая инлайн кнопка", reply_markup=inline_kb1)

# @dp.callback_query_handler(func=lambda c: c.data == 'button1')
# async def process_callback_button1(callback_query: aiogram.types.CallbackQuery):
#     await bot.answer_callback_query(callback_query.id)
#     await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')





# @dp.message_handler(commands=['1'])
# async def process_command_1(message: aiogram.types.Message):
#     await message.reply("Первая инлайн кнопка", reply_markup=inline_kb1)











# @bot.message_handler(commands=['start'])
# def welcome_start(message):
#     bot.send_message(message.chat.id, 'Приветствую тебя user')


# @bot.message_handler(commands=['help'])
# def help_func(message):
#     bot.send_message(message.chat.id, 'Я простой эхо-бот')
#     print("Функция хелп отработала")


# @bot.message_handler(content_types=["text"])
# def repeat_all_messages(message):
#     if message.text == "flex":
#         bot.send_message(message.chat.id, 'hype')
#     else:
#         bot.send_message(message.chat.id, message.text)
#     print("Функция эхо сообщения отработала")