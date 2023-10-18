import pandas as pd
import os
from bs4 import BeautifulSoup
import re
import multiprocessing as mp
import concurrent.futures
import glob
import random
import time
from tqdm import tqdm


scraping_dict = {
                # name, attributes, <extract text/attr>
    'c5n' : {
        'title': ['h1', {'class': 'news-headline__title'}],
        'date': ['time', {'itemprop': 'datePublished'}, 'text'],
        'text': [True, {'class': re.compile('article-body article-body')}]
    },

    'clarin':
    {
        'title': ['h1', {'class': 'storyTitle'}],
        'date': ['meta', {'itemprop': 'datePublished'}, 'content'],
        'text': ['div', {'class': 'StoryTextContainer'}]
    },

    'eldestapeweb':{
        'title': ['h1', {'class': 'titulo'}],
        'date': ['div', {'class': 'fecha'}, 'text'],
        'text': ['div', {'itemprop': 'articleBody'}]
    },

    'lanacion':{
        'title': ['h1', {'class': re.compile('com-title')}],
        'date': ['span', {'class': 'mod-date'}, 'text'],
        'text': [True, {'class': re.compile('com-paragraph')}]
    },
    
    'lavoz':{
        'title': ['h1', {'class': re.compile('false h1 boldbold')}],
        'date': ['div', {'class': re.compile('story-meta-datetime')}, 'text'],
        'text': ['div', {'class': re.compile('story-content')}]

    },

    'perfil':{
        'title': ['h1', {'class': 'article__title'}],
        'date': ['time', {'class': 'article__date'}, 'text'],
        'text': ['div', {'class': re.compile('article__content')}]
    },

    'pagina12':{
        'title': ['h1', {}],
        'date': ['time', {}, 'text'],
        'text': ['div', {'class': re.compile('article-main-content article-text')}]

    },

    'infobae' :{
        'title': ['h1', {'class': re.compile('article-headline')} ],
        'date': ['span', {'class': 'sharebar-article-date'}, 'text'],
        'text': ['div', {'class': re.compile('body-article')}]
    },

    'rionegro':{
        'title': ['h1', {'class': 'newsfull__title'}],
        'date': ['time', {'class': 'newsfull__time'}, 'text'],
        'text': ['div', {'class': 'newsfull__body'}]
    },

}

# return a dataframe with columns: 'title', 'date', 'text'
def scrape_htmls(html):
    website = html.split('/')[2]
    if html.endswith('tags'):
        website = website.replace('tags', '')
    try:
        # read the html
        with open(html, 'r') as f:
            html_file = f.read()
        # parse the html
        soup = BeautifulSoup(html_file, 'html.parser')
        title_tag = scraping_dict[website]['title']
        date_tag = scraping_dict[website]['date']
        text_tag = scraping_dict[website]['text']
        # get the title in h1 with class 'news-headline__title'
        title = soup.find(name=title_tag[0], attrs=title_tag[1]).text
        # get the date in time with itemprop 'datePublished' stored in 'content' tag
        date = soup.find(date_tag[0], date_tag[1])[date_tag[2]] if date_tag[2]!='text' else soup.find(date_tag[0], date_tag[1]).text
        # get the text of any class containing keywords: 'article-body article-body'
        text_elements = soup.find_all(name=text_tag[0], attrs=text_tag[1])

        text = ''
        for text_element in text_elements:
            # get all the <p> tags inside of text_element and their text if the current text_element is not a <p> tag
            if text_element.name != 'p':
                p_tags = text_element.find_all('p')
                for p_tag in p_tags:
                    text += '\n'+p_tag.text.strip()
            else:
                text += '\n'+text_element.text.strip()
        
        return [website, title, date, text]

    except Exception as e:
        return [website, '', '', '']
        
    
    





if __name__ == '__main__':
    # glob 100 random htmls from data/htmls/*/
    html_folders = os.listdir('data/htmls/')
    htmls = []
    for folder in html_folders:
        files = glob.glob(f'data/htmls/{folder}/*.html')
        # htmls.extend(random.sample(files, min(len(files),10000)))
        htmls.extend(files)
    
    start = time.time()
    # scrape the htmls
    # use multiprocessing to speed up the process
    with concurrent.futures.ProcessPoolExecutor(64) as executor:
        results = list(executor.map(scrape_htmls, htmls))
    

    end = time.time()

    # time diff in seconds
    print(f'Time taken: {end-start}')
    
    # create a dataframe to store the data
    df = pd.DataFrame(results, columns=['website', 'title', 'date', 'text'])

    # save the dataframe
    df.to_csv('data/htmls_scraped/scraped_data.csv', index=False)