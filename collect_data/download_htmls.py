import requests
import os
import json
from itertools import islice
import time

DATA_DIR = 'data/htmls/'

def download_htmls(website, hrefs):

    # create a directory for the website
    if not os.path.exists(DATA_DIR+website):
        os.makedirs(DATA_DIR+website)

    download_index = {}
    error_hrefs = []
    # download the htmls
    for i, href in enumerate(hrefs):
        # format
        print(f'downloads:{i+1:>5}/{len(hrefs):<5}    website:{website:<15}')

        time.sleep(1)
        # get the html
        try:
            req = requests.get(href, timeout=20)
        except Exception as e:
            print(f"error in {website}: {e}")
            error_hrefs.append(href)
            continue

        download_index[href] = i
        # save the html
        with open(DATA_DIR + website + '/' + str(i) + '.html', 'w') as f:
            f.write(req.text)
    
    try:
        # write down the download index as json file
        with open(DATA_DIR + website + '/downloads.json', 'w') as f:
            json.dump(download_index, f, indent=4)
    except Exception as e:
        print(f"error in {website}: {e}")


    try:
        # write down the error_hrefs as txt file
        with open(DATA_DIR + website + '/errors.txt', 'w') as f:
            for href in error_hrefs:
                f.write(href + '\n')

    except Exception as e:
        print(f"error in {website}: {e}")


    return



if __name__ == '__main__':

    # web_list = ['lanacion', 'clarin', 'lavoz', 'los_andes', 'perfil', 'rionegro', 'eldestapeweb', 'c5n']
    # web_list = ['pagina12']
    # web_list = ['infobae']
    web_list = ['clarintags']

    # Maximum number of lines to read
    MAX_LINES = 60000

    # load the hrefs
    href_dict = {}
    for href_txt in os.listdir('data/hrefs/'):
        website = href_txt.split('_')[0]
        if website in web_list:
            with open('data/hrefs/' + href_txt, 'r') as f:
                href_dict[website] = [href.strip() for href in islice(f, MAX_LINES)]
    
    # start a new process for each website using multiprocessing
    import multiprocessing as mp
    processes = []
    for website in href_dict:
        p = mp.Process(target=download_htmls, args=(website, href_dict[website],))
        p.start()
        processes.append(p)

    # wait for all the processes to finish
    for p in processes:
        p.join()