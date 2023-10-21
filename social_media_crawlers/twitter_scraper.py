#NEEDS SELENIUM
#NEEDS CHROMEDRIVER

USERNAME = ''
PASSWORD=''
candidates = {'Myriam Teresa Bregman':['myriam bregman'],'Sergio Tomas Massa':['sergio massa','massa','panqueque'],'Patricia Bullrich':['patricia bullrich','montonera'],'Javier Milei':['javier milei', 'milei'],'Juan Schiaretti':['juan schiaretti']}


end_date = datetime(2023, 8, 15).date()

# Define the start date
start_date = datetime(2023, 8, 1).date()


from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

import os
import re
import tqdm
CLEANR = re.compile('<.*?>')
tweet_set = {}

# Define an empty list to store the date strings
date_strings = []






while end_date >= start_date:
    end_date -= timedelta(days=2)
    prev_date = end_date+timedelta(days=2)
    date_strings.append([prev_date.strftime('%Y-%m-%d'),end_date.strftime('%Y-%m-%d')])

def get_data(page):
    tweet_dic = {}
    soup = BeautifulSoup(page, 'html.parser')
    tweet_elements = soup.find_all("div", class_="css-1dbjc4n r-16y2uox r-1wbh5a2 r-1ny4l3l")

    # Loop through the tweet elements and extract the desired information
    for tweet_element in tweet_elements:
        try:
            tweet_time = tweet_element.find("time")['datetime']
            # Extract tweet text
            tweet_text = tweet_element.find("div", {"data-testid": "tweetText"}).text
            # Extract tweet time
            # Extract tweeter handle
            tweeter_handle = tweet_element.find("div", class_="css-1dbjc4n r-1awozwy r-18u37iz r-1wbh5a2 r-dnmrzs r-1ny4l3l").text.split('@')[0]
            # Extract tweet id
            tweet_id = tweet_element.find("a", {"aria-label": True})["href"]
            # Extract twitter username
            twitter_username = tweet_element.find("a", href=True)["href"].split("/")[1]
            #print(tweet_id,tweet_time,tweeter_handle,twitter_username,tweet_text)
            # Print the extracted information
            tweet_dic[tweet_id]=[tweet_id,tweet_time,tweeter_handle,twitter_username,tweet_text]
        except:
            continue
    return(tweet_dic)



options = Options()
#options.binary_location=r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
#options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
options.add_argument('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome') #Path to your chrome profile

driver = webdriver.Chrome()

def login(username,password):
    while(1):
        try:
            driver.get('https://www.twitter.com')
            driver.find_element(By.XPATH,'/html/body/div/div/div/div[2]/main/div/div/div[1]/div/div/div[3]/div[5]/a').click()
            break
        except:
            time.sleep(2)
    #Username
    while(1):
        try:
            try:
                inputElement = driver.find_element(By.XPATH,"/html/body/div/div/div/div/main/div/div/div/div[2]/div[2]/div/div[5]/label/div/div[2]/div/input")
            except:
                inputElement = driver.find_element(By.XPATH,"/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input")
            inputElement.send_keys(username)               
            try:
                driver.find_element(By.XPATH,'/html/body/div/div/div/div/main/div/div/div/div[2]/div[2]/div/div[6]').click()
            except:
                driver.find_element(By.XPATH,"/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]").click()
            
            break
        except:
            time.sleep(2)

    while(1):
        try:
            try:
                inputElement = driver.find_element(By.XPATH,"/html/body/div/div/div/div/main/div/div/div/div[2]/div[2]/div[1]/div/div/div/div[3]/div/label/div/div[2]/div[1]/input")
            except:
                inputElement = driver.find_element(By.XPATH,"/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input")
            inputElement.send_keys(password)
            try:
                driver.find_element(By.XPATH,'/html/body/div/div/div/div/main/div/div/div/div[2]/div[2]/div[2]/div/div/div[1]/div/div/div').click()
            except:
                driver.find_element(By.XPATH,'/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div').click()
            break
        except:
            time.sleep(2)

login(USERNAME,PASSWORD)
time.sleep(5)
driver.get('https://twitter.com/search-advanced?lang=es')
time.sleep(1)


for candidate in candidates:
    for hashtag in tqdm.tqdm(candidates[candidate]):
        hashtag_set = [hashtag]
        hashquery = ' AND '.join(hashtag_set)
        for DATE in date_strings:
            
            time.sleep(5)
            END_DATE = DATE[0]
            START_DATE = DATE[1]
            #https://twitter.com/search?lang=es&q=(%23milei)%20until%3A2023-01-02%20since%3A2023-01-01&src=typed_query
            query_url = 'https://twitter.com/search?lang=es&q=('+hashquery+')%20until%3A'+END_DATE+'%20since%3A'+START_DATE+'&src=typed_query'
            #url = 'https://twitter.com/search?lang=es&q=('+hashquery+')%20until%3A2023-03-04%20since%3A2023-03-03&src=typed_query
            driver.get(query_url)
            old = driver.page_source
            page = ''
            scrolls = 100
            i = 0
            while(i<50):
                i+=1
                print(i)
                try:
                    driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/section/div/div/div[5]/div/div/div[2]/div').click()
                    time.sleep(60)
                    query_url = 'https://twitter.com/search?lang=es&q=('+hashquery+')%20until%3A'+END_DATE+'%20since%3A'+START_DATE+'&src=typed_query'
                    driver.get(query_url)
                    print('TimeOut')
                except:
                    
                    old = page

                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    page = driver.page_source
                    tweets = get_data(page)
                    for item in tweets:
                        L = tweets[item]
                        L.append(candidate)
                        tweet_set[item] = L
                    time.sleep(7)  # Wait for the page to load
            time.sleep(120)
            print(len(tweet_set))

import csv
with open('twitter_dump_.csv', mode='w') as _file:
    _writer = csv.writer(_file, delimiter=',')
    for item in tweet_set:
        _writer.writerow(tweet_set[item])
