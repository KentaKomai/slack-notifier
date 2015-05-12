# coding:utf-8
#! /usr/bin/python

import sys
import urllib
import urllib2
import json

""" API関連のグローバル変数 """
api_base_url = "https://slack.com/api/"
api_channel_history_url = api_base_url + "channels.history"
api_channel_info_url = api_base_url + "channels.info"
api_channel_list_url = api_base_url + "channels.list"
api_user_list_url = api_base_url + "users.list"

""" API利用のためのトークン """
token = "please input your slack token"

notification_levels = ['good', 'warning', 'danger']
argvs = sys.argv


def main():
  channel_name = argvs[1]
  config_json_path = argvs[2]
  level = argvs[3]
  title = argvs[4]
  message = argvs[5]

  target_channel = find_channel(channel_name)
  if len(target_channel) == 0:
    print("channel " + channel_name + " is not found")
    sys.exit
  else:
    notice_config = json_parse(config_json_path)
    payload = format_slack_payload(channel_name, title, message, level, notice_config)
    send_to_slack_incomming_api(notice_config['incomming_url'], payload)

def json_parse(file_path):
  f = open(file_path, 'r')
  json_data = json.load(f)
  return json_data

# コマンドの使い方を表示
def print_usage():
  print("<usage> python " + argvs[0] + "[configure_json_path] [channel_name] [good|warning|danger] [title] [message]")
  print("example: python " + argvs[0] + "./notice.json channel_name warning 'title' 'description'")

# 送信用ペイロードの生成
def format_slack_payload(channel, title, message,level,config):
  json_data = { 
      'channel':'#'+channel,
      'username': config['name'],
      'attachments' : [{
        'fallback' : u"お知らせ",
        'color' : level,
        'pretext': config['pretext'],
        'title' : config[level]['title_prefix'] + " " + title.decode('utf-8'),
        'text' : message
      }],
      "icon_emoji": config[level]['icon_emoji']
      }
  return json.dumps(json_data)

def send_to_slack_incomming_api(url, payload):
  params = urllib.urlencode({'payload':payload})
  req = urllib2.Request(url, params)
  res = urllib2.urlopen(req)


# 名前からチャンネル情報を取得する
def find_channel(channel_name):
  params = urllib.urlencode({'token':token})
  channel_list = request_to_json(api_channel_list_url, params)

  # 完全一致するものをリストで返す
  channelList = []
  for channel in channel_list['channels']:
    if(channel['name'] == channel_name):
        channelList.append(channel)

  return channelList

def request_to_json(url, params):
  req = urllib2.Request(url, params)
  res = urllib2.urlopen(req)
  json_data = json.loads(res.read())

  if not json_data['ok']:
    exit #正しく取得できなかったら終了

  return json_data



if __name__ == "__main__":
  if len(argvs) < 6 :
    print(len(argvs))
    print_usage()
    sys.exit
  elif not (argvs[3] in notification_levels):
    print("invalid level")
    print_usage()
    sys.exit
  else:
    main()


