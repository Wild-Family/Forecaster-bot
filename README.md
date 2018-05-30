# お天気予報Bot
#### つかいかた
1. LINE Developerにてチャネルの登録をすませ，docker-compose.ymlと同じディレクトリに下記の内容の`.env`ファイルを配置
    ```.env
    CHANNEL_SECRET="YOUR_CHANNEL_SECRET"
    CHANNEL_TOKEN="YOUR_CHANNEL_TOKEN"
    API_KEY="YOUR_OPENWEATHERMAP_API_KEY"
    ```
1. `docker-compse up -d`でコンテナを起動
    - デフォルトではホストのポート8011を使います
1. ngrokなりでSSL化し，チャネルページのWebHookURLに登録する
    - URLの末尾に/callbackが必要！
    - Toolboxだとngrokを使えないので注意

#### Credit
- Weather Icons made by Freepik from www.flaticon.com
- Weather API provided by OpenWeatherMap(https://openweathermap.org)