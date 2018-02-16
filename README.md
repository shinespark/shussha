# shussha_follow

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
  company_id: 'follow.jpの企業ID'
  login_id: 'follow.jpのログインID'
  password: 'follow.jpのパスワード'
```

## NFC IDの確認

```
$ python shussha_follow.py
$ tail -f shussha_follow.log
```

## Slack Legacy token の発行

[Legacy tokens | Slack](https://api.slack.com/custom-integrations/legacy-tokens)

## 出勤 / 退勤切り替えについて

`time_period` の時刻以前は出勤, 時刻以降は 退勤扱いになる仕様になっています。


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
