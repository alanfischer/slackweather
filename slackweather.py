#!/Users/afischer/env/bin/python

import requests
import json
import configparser
from os.path import expanduser

parser = configparser.ConfigParser()
parser.read(expanduser("~") + "/.slackweather")

wunderground_key = parser.get('slackweather','wunderground_key')
slack_key = parser.get('slackweather','slack_key')
user = parser.get('slackweather','slack_user')
location = parser.get('slackweather','location')

icon_to_emoji = {
    'chanceflurries' : ':snow_cloud:',
    'chancesnow' : ':snow_cloud:',
    'chancerain' : ':rain_cloud:',
    'chancesleet' : ':rain_cloud:',
    'chancetstorms' : ':thunder_cloud_and_rain:',
    'clear' : ':sunny:',
    'cloudy' : ':cloud:',
    'flurries' : ':snow_cloud:',
    'fog' : ':fog:',
    'hazy' : ':fog:',
    'mostlycloudy' : ':partly_sunny:',
    'mostlysunny' : ':mostly_sunny:',
    'partlycloudy' : ':mostly_sunny:',
    'partlysunny' : 'partly_sunny:',
    'sleet' : ':rain_cloud:',
    'rain' : ':rain_cloud:',
    'snow' : ':snow_cloud:',
    'sunny' : ':sunny:',
    'tstorms' : ':thunder_cloud_and_rain:',
    'unknown' : ':question:'
}

request = requests.get("http://api.wunderground.com/api/" + wunderground_key + "/conditions/q/" + location + ".json")
if request.status_code != 200:
	print(request.json())

current_observation = request.json()['current_observation']

emoji = icon_to_emoji[current_observation['icon']]

text = current_observation['weather'] + ", " + current_observation['temperature_string'] + ", " + current_observation['wind_string']

profile = {
    'status_emoji' : emoji,
    'status_text' : text
}

request = requests.get("http://slack.com/api/users.profile.set", params = { 'token' : slack_key, 'user' : user, 'profile' : json.dumps(profile) })
if request.status_code != 200:
	print(request.json())
