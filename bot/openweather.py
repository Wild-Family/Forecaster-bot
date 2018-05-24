import os
import sys
import json
import requests


def get_current_weather(lat, lon):
    #set_env('API_KEY')
    API_KEY = os.getenv('API_KEY', None)
    if API_KEY is None:
        print('Specify API_KEY as environment variable.')
        sys.exit(1)

    # 気温の単位は摂氏
    payload = {'lat': lat, 'lon': lon, 'units': 'metric', 'APPID': API_KEY}
    url = 'http://api.openweathermap.org/data/2.5/weather'
    response = requests.get(url, payload)

    # レスポンスをjsonで取得
    return response.json()


def get_geocode(address_json):
    address = json.loads(address_json)
    lat = address['latitude']
    lon = address['longitude']

    return lat, lon


def set_env(key_name):
    # .envファイルを改行コードを除いて文字列リストに読み込む
    str = [line.strip() for line in open('.env', 'r').readlines()]
    # API_KEYの行を抽出
    line = [line for line in str if key_name in line][0]
    # 値を取り出す
    key_value = line[line.find(key_name)+len(key_name)+1:]
    os.environ[key_name] = key_value


def main():
    set_env('API_KEY')

    weather_dict = {
        "type": "location",
        "title": "my location", "address": "〒150-0002 東京都渋谷区渋谷２丁目２１−１",
        "latitude": 35.65910807942215,
        "longitude": 139.70372892916203}
    
    weather_json = get_current_weather(weather_dict['latitude'], weather_dict['longitude'])
    print(weather_json)


if __name__ == '__main__':
    main()
