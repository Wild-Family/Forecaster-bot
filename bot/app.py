# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import os
import sys
import json
import openweather as ow
import message_builder as mb

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, LocationMessage
)
from linebot.models.template import (
    TemplateSendMessage, CarouselColumn, CarouselTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction
)

app = Flask(__name__)

# デバッグ用
# .envから環境変数を設定
#ow.set_env("CHANNEL_SECRET")
#ow.set_env("CHANNEL_TOKEN")

channel_secret = os.getenv('CHANNEL_SECRET', None)
channel_access_token = os.getenv('CHANNEL_TOKEN', None)

if channel_secret is None:
    print('Specify CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify CHANNEL_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return '', 200, {}


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    if event.message.text == "シドニーの天気をおしえて":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="i dont know sry :)")
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )


@handler.add(MessageEvent, message=LocationMessage)
def message_location(event):
    # result_json = ow.get_current_weather(event.message.latitude, event.message.longitude)
    # print(result_json)
    forecast = ow.get_current_forecast(event.message.latitude, event.message.longitude)
    forecast_sliced = mb.slice_per_day(forecast)

    for i, day in enumerate(forecast_sliced.values()):
        # 3日分表示
        if i < 3:
            line_bot_api.push_message(
                event.source.user_id,
                mb.CarouselSendMessage(day)
            )

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
