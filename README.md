# shussha_follow

## これは何？

NFCカードリーダを利用して、 follow.jp に打刻するアプリケーションです。  
打刻したらIFTTT経由でプッシュ通知も可能です。

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
  follow:
    company_id: 'follow.jpの企業ID'
    login_id:   'follow.jpのログインID'
    password:   'follow.jpのパスワード'
  ifttt: # Optional
    trigger: 'WebHookのトリガーイベント名'
    key:     'WebHookのキー'
```

## NFC IDの確認

```
$ python shussha_follow.py
$ tail -f shussha_follow.log
```

## 出勤 / 退勤切り替えについて

`time_period` の時刻以前は出勤, 時刻以降は退勤扱いになる仕様になっています。


## 自動起動

shussha_follow.service を利用してください。
Raspberry Pi用に書いてあるので、パスは適宜変更してください。

```
$ sudo cp shussha_follow.service /etc/systemd/system/

# 自動起動登録
$ sudo systemctl enable shussha_follow.service

# 起動
$ sudo systemctl start shussha_follow.service

# 終了
$ sudo systemctl stop shussha_follow.service
```
