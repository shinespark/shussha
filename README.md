# shussha

## これは何？

NFCカードリーダを利用して、 follow.jp に打刻するアプリケーションです。
ついでにSlackにも発言します。(あとで削除予定)

nfcpyがPython2.xのみ対応の為、Python2実行環境が必要です。


## 初期設定

pip install

```
$ pip install -r requirements.txt
```

起動

```
$ python shussha_follow.py
```

conf設定

```
$ cp conf{_original,}.yml
$ vi conf.yml
# 以下のフォーマットでconf.ymlを書き換えてください

<ID>: # NFCカードのID
  description: ''
  time_period: 15 # 発言するSlackチャンネルを切り替える時間(e.g. 15時)
  token: 'xoxp-xxxxxxxxxx-xxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' # Slack Legacy token
  text: 'この内容をポストするよ' # 発言するテキスト
```

## NFC IDの確認

```
$ python shussha_follow.py
$ tail -f shussha_follow.log
```

## Slack Legacy token の発行

[Legacy tokens | Slack](https://api.slack.com/custom-integrations/legacy-tokens)

## 発言するSlackチャンネルの切り替え

`time_period` の時刻以前は、 `#出勤連絡` チャンネル, 時刻以降は `#退勤連絡` チャンネルに発言する仕様になっています。
同一チャンネルに発言したい場合には、直接 shussha_follow.py を書き換えてください。


## 自動起動

shussha_follow.service を利用してください。

```
$ sudo cp shussha_follow.service /etc/systemd/system/

# 自動起動登録
$ sudo systemctl enable shussha_follow.service

# 起動
$ sudo systemctl start shussha_follow.service

# 終了
$ sudo systemctl stop shussha_follow.service
```
