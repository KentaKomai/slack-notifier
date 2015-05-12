Slackに任意のメッセージをコマンドラインから送信します。

## 使い方

チャンネル名、設定ファイルへのパス、タイトル、メッセージ本文の順で指定します。

```
$ python main.py channel_name ./notice.json good 'title' 'description'
```

## 設定ファイル

```
{
  "name":"SlackNotifier",
  "incomming_url": "https://hooks.slack.com/services/slackincomming-url",
  "pretext":"This text has been automatically sent",
  "good": {
    "title_prefix":"[OK]",
    "icon_emoji":":yum:"
  },
  "warning": {
    "title_prefix":"[WARNING]",
    "icon_emoji":":sweat:"
  },
  "danger" : {
    "title_prefix":"[DANGER]",
    "icon_emoji":":rage:"
  }
}
```

* name:送信者の名前
* incomming_url:incomming_webhookを追加したときのURLを設定する
* pre_text: 全てのメッセージに共通するメッセージです
* {good|warning|danger}.title_prefix: それぞれのメッセージレベルのときにタイトルにつくprefixです
* {good|warning|danger}.icon_emoji : それぞれのメッセージレベルのときのアイコンです


