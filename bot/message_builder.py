import json
import datetime


def build_test_message(weather_dict):
    print(weather_dict)
    message = {
        '天気': weather_dict['weather'][0]['main'],
        '天気詳細': weather_dict['weather'][0]['description'],
        '気温(℃)': weather_dict['main']['temp'],
        '湿度(％)': weather_dict['main']['humidity'],
        '風速(m/s)': weather_dict['wind']['speed']
    }
    return json.dumps(message, ensure_ascii=False)


def slice_per_day(forecast_dict):
    result_dict = {}
    while(True):
        index = 0
        day = datetime.datetime(forecast_dict['list'][index]['dt_txt']).day
        day_dict = {}
        for item in forecast_dict['list']:
            if datetime.datetime(item['dt_txt']).day == day:
                day_dict = item


def CarouselSendMessage(forecast_day):
    colomns_size = len(forecast_day['list'])


def main():
    test_data = open('bot/weather_test.json')
    test_json = json.load(test_data)
    message = build_test_message(test_json)
    print(message)


if __name__ == '__main__':
    main()
