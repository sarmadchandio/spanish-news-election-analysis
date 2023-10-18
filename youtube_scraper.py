
import requests
import time
import time
import random
from datetime import datetime, timedelta

# Your YouTube Data API key
api_key = ['']
#api_key.shuffle()
print(len(api_key))
api_key = api_key[::-1]

API_KEY = api_key[1]
START_DATE = '2023-10-10'
DAYS = 1
# The initial query parameters
# Interval in seconds (15 minutes)

import tqdm
def YTScrape(QUERY,START_TIME,DAYS=1):
  j=0
  API_KEY = api_key[j]
  curr_str = START_TIME+'T00:00:00Z'


  DATA = []
  i=0
  while(i<(3*DAYS)):
    print(i,3*DAYS,j)
    base_url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part': 'snippet',
        'maxResults': 1000,
        'q': QUERY,
        'type': 'video',
        'key': API_KEY
    }

    now = datetime.strptime(curr_str, '%Y-%m-%dT%H:%M:%SZ')
    prev = now - timedelta(minutes=480)

    # Format ten_minutes_ago as a string in the desired format
    prev_str = prev.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Update the time boundaries in the query parameters
    params['publishedAfter'] = prev_str
    params['publishedBefore'] = curr_str

    # Make the API request
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        # Handle the response here (e.g., parse the JSON response)
        data = response.json()
        #print(data)
        DATA.append(data)
        # Do something with the data

    else:
        print(f"Error: {response.status_code} - {response.text}")
        j = j+1
        j = j%len(api_key)
        i = i-1
        API_KEY = api_key[j]


    # Wait for the next interval
    curr_str = prev_str
    time.sleep(1)
    i+=1
  return(DATA)

import csv
QUERY = 'javier milei'
candidates = ['Sergio Massa','Myriam Bregman','Gabriel Solano','Juan Schiaretti','Horacio Rodriguez Larreta','Patricia Bullrich','Nazareno Etchepare','Ramiro Vasena','Manuela Castañeira','Raul Albarracin','Raul Castells','Santiago Cuneo','Jesus Escobar','Marcelo Ramal','Guillermo Moreno','Oscar Giardinelli','Martin Ayerbe Ortiz','Reina Ibañez','Andres Passamonti','Juan Grabois','Julio Barbaro','Eliodoro Martinez','Jorge Oliver','Carolina Bartolini','Paula Arias']
for QUERY in candidates:
  print(QUERY)
  API_KEY = api_key[1]
  START_TIME = START_DATE
  DAYS = 70
  data = YTScrape(QUERY,START_TIME,DAYS)
  #print(d['items'][0])
  DAYS=70
  videos = []
  for d in data:

    for i in range(0,len(d['items'])):
      video_info = []
      video_info.append(QUERY)
      video_info.append(d['items'][i]['snippet']['channelId'])
      video_info.append(d['items'][i]['id']['videoId'])
      video_info.append(d['items'][i]['snippet']['publishedAt'])
      video_info.append(d['items'][i]['snippet']['title'])
      video_info.append(d['items'][i]['snippet']['description'])
      videos.append(video_info)

  print(len(videos))


  with open(QUERY+'_'+START_TIME+'_'+str(DAYS)+'.csv', mode='w') as _file:
      _writer = csv.writer(_file, delimiter=',')
      for item in videos:
          _writer.writerow(item)

!zip -R foo '*.csv'

import csv

with open(QUERY+'_'+START_TIME+'_'+str(DAYS)+'.csv', mode='w') as _file:
    _writer = csv.writer(_file, delimiter=',')
    for item in videos:
        _writer.writerow(item)

!unzip foo.zip

import os
files = os.listdir('./')
import csv
channels = []
for f in files:
  if f.endswith('.csv'):
    with open(f) as csv_file:
      csv_reader = csv.reader(csv_file, delimiter=',')
      line_count = 0
      for row in csv_reader:
          channels.append(row[1])


channels = list(set(channels))

from pytube import Channel
import sys, logging
import tqdm
cv = {}
for CHANNEL in tqdm.tqdm(channels):
  logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
  channel = Channel('https://www.youtube.com/channel/'+CHANNEL+'/videos')
  #channel = Channel("https://www.youtube.com/channel/UCZRdNleCgW-BGUJf-bbjzQg/videos")
  videos ={}
  for video in channel.videos:
    DATE = video.publish_date
    videos[video.video_id] = DATE



  cv[CHANNEL] = videos

