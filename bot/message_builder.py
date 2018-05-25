import os
import sys
import json


def build_test_message(weather_json):
    #weather_json = json.loads(weather_str)
    print(weather_json)
    message = {
        '天気': weather_json["weather"][0]["main"],
        '天気詳細': weather_json['weather'][0]['description'],
        '気温': weather_json['main']['temp'],
        '最高気温': weather_json['main']['temp_max'],
        '最低気温': weather_json['main']['temp_min'],
        '湿度': weather_json['main']['humidity']
    }
    return json.dumps(message)


def main():
    test_data = open('bot/weather_test.json')
    test_json = json.load(test_data)
    message = build_test_message(test_json)
    print(message)

if __name__ == '__main__':
    main()