import json
import datetime
import linebot.models.template as template
from collections import defaultdict


def build_test_message(weather_dict):
    # print(weather_dict)
    message = {
        '天気': weather_dict['weather'][0]['main'],
        '天気詳細': weather_dict['weather'][0]['description'],
        '気温(℃)': weather_dict['main']['temp'],
        '湿度(％)': weather_dict['main']['humidity'],
        '風速(m/s)': weather_dict['wind']['speed']
    }

    return json.dumps(message, ensure_ascii=False)


def CarouselSendMessage(forecast_day):
    columns = []
    for lapse in forecast_day.values():
        columns.append(template.CarouselColumn(
            thumbnail_image_url=None,
            title=convert_str_to_dt_jp(lapse['dt_txt']).strftime('%Y/%m/%d %H:%M'),
            text=lapse['weather'][0]['main'],
            actions=[
                template.MessageTemplateAction(
                    label='label',
                    text='hey'
                )
            ]
        ))
    
    message = template.TemplateSendMessage(
        alt_text='Carousel Forecast Data',
        template=template.CarouselTemplate(
            columns=columns
        )
    )

    return message


def slice_per_day(forecast_dict):
    result_dict = defaultdict(lambda: dict)
    index = 0
    day_count = 0
    # 同じ日付のデータをリストにまとめる
    while(index < len(forecast_dict['list'])):
        # 日付を取得
        day = convert_str_to_dt_jp(forecast_dict['list'][index]['dt_txt']).day
        day_dict = defaultdict(lambda: dict)
        # defaultdictに取得した日付のデータを入れる
        for i, item in enumerate(forecast_dict['list']):
            dt_converted = convert_str_to_dt_jp(item['dt_txt'])
            if dt_converted.day == day:
                # print(item)
                day_dict[i] = item
                day_dict[i]['dt_txt'] = dt_converted.strftime('%Y-%m-%d %H:%M:%S')
        # print(day_dict)
        result_dict[day_count] = day_dict
        # 1日進める
        day_count += 1
        index += len(day_dict)
    
    return result_dict


def convert_str_to_dt_jp(str):
    dt = datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S')
    dt_jp = dt + datetime.timedelta(hours=9)
    return dt_jp


def main():
    test_data = open('bot/weather_test.json')
    test_json = json.load(test_data)
    message = build_test_message(test_json)
    # print(message)
    forecast = slice_per_day(json.load(open('bot/forecast_test.json','r')))
    # print(forecast)
    # print(len(forecast))
    # print(type(forecast[0]))
    message = CarouselSendMessage(forecast[0])
    print(message)


if __name__ == '__main__':
    main()
