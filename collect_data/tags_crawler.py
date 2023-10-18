import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time
from bs4 import BeautifulSoup
import json
import re

            
class pagina12Scrapper:
    keyterms_dict = {
        'mariyam-bregman' :         [f'https://www.pagina12.com.ar/tags/2227-myriam-bregman?page={i}' for i in range(20)], # write page number after this
        'javier-milei' :            [f'https://www.pagina12.com.ar/tags/24483-javier-milei?page={i}' for i in range(20)],
        "gabriel-solano":           [f'https://www.pagina12.com.ar/tags/25971-gabriel-solano?page={i}' for i in range(20)],
        "alejandro-biondini":       [f'https://www.pagina12.com.ar/tags/13000-alejandro-biondini?page={i}' for i in range(20)],
        "juan-schiaretti" :         [f'https://www.pagina12.com.ar/tags/1904-juan-schiaretti?page={i}' for i in range(20)],
        "horacio-rodriguez-larreta":[f'https://www.pagina12.com.ar/tags/1204-horacio-rodriguez-larreta?page={i}' for i in range(20)],
        "patricia-bullrich" :       [f'https://www.pagina12.com.ar/tags/1318-patricia-bullrich?page={i}' for i in range(20)],
        "manuela-castaneira" :      [f'https://www.pagina12.com.ar/tags/56204-manuela-castaneira?page={i}' for i in range(20)],
        "marcelo-ramal" :           [f'https://www.pagina12.com.ar/tags/1417-marcelo-ramal?page={i}' for i in range(20)],
        "guillermo-moreno" :        [f'https://www.pagina12.com.ar/tags/12916-guillermo-moreno?page={i}' for i in range(20)],
        "sergio-massa" :            [f'https://www.pagina12.com.ar/tags/1293-sergio-massa?page={i}' for i in range(20)],
        "juan-grabois" :            [f'https://www.pagina12.com.ar/tags/2807-juan-grabois?page={i}' for i in range(20)]
    }

    def __init__(self):
        self.dir = DATA_DIR+"hrefs/"

    def collect_hrefs(self):

        hrefs = []
        for term in self.keyterms_dict:
            for i, url in enumerate(self.keyterms_dict[term]):
                # extract all the children from class 'articles-list'
                time.sleep(1)
                print(f'{term} - {i}')
                try:
                    response = requests.get(url)
                    response.raise_for_status()  # Check if the request was successful
                    # Step 2: Parse the page content with BeautifulSoup
                    page_content = BeautifulSoup(response.text, 'html.parser')
                    time.sleep(2)
                except requests.RequestException as e:
                    print(f"Failed to get content from {url}: {e}")
                    break                
                try:
                    # Step 3: Extract the desired information
                    for article in page_content.find_all(class_=re.compile('article-item article-item--teaser')):

                        # get the href from <a> who is a child of <div> with class 'article-item__header'
                        href = article.find('div', class_='article-item__header').a['href'] 
                        hrefs.append('https://www.pagina12.com.ar'+href)

                except Exception as e:
                    print(e)

            # make a dir for if not already present
            if not os.path.isdir(self.dir):
                os.mkdir(self.dir)
            

        # write the term_links to a file
        with open(f"{self.dir}pagina12tags_hrefs.txt", "w") as f:
            for link in hrefs:
                f.write(link + "\n")



class infobaeScrapper:
    def __init__(self):
        self.dir = DATA_DIR+"hrefs/"

    def collect_hrefs(self):
        urls = [
            'https://www.infobae.com/tag/patricia-bullrich/',
            'https://www.infobae.com/tag/javier-milei/',
            'https://www.infobae.com/tag/sergio-massa/',
            'https://www.infobae.com/tag/horacio-rodriguez-larreta/',
            'https://www.infobae.com/tag/myriam-bregman/',
            'https://www.infobae.com/tag/gabriel-solano/',
            'https://www.infobae.com/tag/alejandro-biondini/',
            'https://www.infobae.com/tag/juan-schiaretti/',
            'https://www.infobae.com/tag/raul-castells/',
            'https://www.infobae.com/tag/santiago-cuneo/',
            'https://www.infobae.com/tag/marcelo-ramal/',
            'https://www.infobae.com/tag/guillermo-moreno/',
            'https://www.infobae.com/tag/andres-passamonti',
            'https://www.infobae.com/tag/juan-grabois',
            'https://www.infobae.com/tag/paula-arias'
        ]
        hrefs = set()
        
        for url in urls:
            time.sleep(1)
            print(f'{url}')
            try:
                response = requests.get(url)
                response.raise_for_status()  # Check if the request was successful
                # Step 2: Parse the page content with BeautifulSoup
                page_content = BeautifulSoup(response.text, 'html.parser')
                time.sleep(2)
            except requests.RequestException as e:
                print(f"Failed to get content from {url}: {e}")
                break                
            try:
                # Step 3: Extract the desired information
                for article in page_content.find_all('a', class_=re.compile('feed-list-card')):
                    # get the href from <a> who is a child of <div> with class 'article-item__header'
                    href = article['href'] 
                    hrefs.add('https://www.infobae.com'+href)
                print(len(hrefs))

            except Exception as e:
                print(e)
        
        # write the term_links to a file
        with open(f"{self.dir}infobaetags_hrefs.txt", "w") as f:
            for link in hrefs:
                f.write(link + "\n")

class clarinScrapper:
    def __init__(self):
        self.dir = DATA_DIR+"hrefs/"

    def collect_hrefs(self):
        
        candidate_set = ['javier-milei','sergio-massa','patricia-bullrich','myriam-bregman','gabriel-solano','alejandro-biondini','juan-schiaretti','horacio-rodriguez-larreta','patricia-bullrich','javier-milei','raul-albarracin','raul-castells','marcelo-ramal','guillermo-moreno','sergio-massa','juan-grabois','julio-barbaro']
        
        urls =[f'https://www.clarin.com/tema/{candidate}' for candidate in candidate_set]

        hrefs = set()
        for url in urls:
            time.sleep(1)

            # add the page numbers
            page_list = [url+f'/page/{i}' for i in range(1,15)] 
            for page in page_list:
                # collect hrefs of all the class 'sc-9c7624e4-1 cfKQoj'
                try:
                    response = requests.get(page)
                    response.raise_for_status()  # Check if the request was successful
                    # Step 2: Parse the page content with BeautifulSoup
                    page_content = BeautifulSoup(response.text, 'html.parser')
                    
                    time.sleep(2)
                except requests.RequestException as e:
                    print(f"Failed to get content from {url}: {e}")
                    break
                try:
                    print('visiting page: ', page)
                    # Step 3: Extract the desired information
                    for article in page_content.find_all(class_='sc-9c7624e4-1 cfKQoj'):
                        # get the href from <a> who is a child of <div> with class 'article-item__header'
                        href = article.a['href'] 
                        hrefs.add('https://www.clarin.com/'+href)
                    print(len(hrefs))

                except Exception as e:
                    print(e)
                    break

        # write the term_links to a file
        with open(f"{self.dir}clarintags_hrefs.txt", "w") as f:
            for link in hrefs:
                f.write(link + "\n")




