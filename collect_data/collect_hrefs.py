import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm

# initial xml sitemaps for each website
xml_dicts = {
    # 'lanacion' : ['https://www.lanacion.com.ar/sitemap-news.xml', 'https://www.lanacion.com.ar/sitemap-index-historico.xml'], # 2023-2021
    # 'clarin': ['https://www.clarin.com/sitemaps/index_news.xml'], # 2023 only
    'infoabe': ['https://www.infobae.com/sitemap-index.xml', 'https://www.infobae.com/news_sitemap.xml', 'https://www.infobae.com/sitemap.xml'], # mostly 2023 month 10. There are links based on topics leading to other years
    # 'pagina12': ['https://www.pagina12.com.ar/breakingnews-short.xml'], # weak sitemap (just 2023 breaking news...?)
    'ambito': ['https://www.ambito.com/sitemap.xml'], # weak sitemap. Do manually
    'cronista': [], # no sitemap. manual collection
    # 'lavoz' : [f'https://www.lavoz.com.ar/arc/outboundfeeds/feeds/sitemap/?outputType=xml&from={i}' for i in range(0, 50000, 100)], # upto 2023-03 data.
    # 'los_andes': [f'https://www.losandes.com.ar/arc/outboundfeeds/sitemap/?outputType=xml&from={i}' for i in range(0, 50000, 100)],  # upto 2022-07 data. (Can extract more from here...)
    # 'perfil': [f'https://www.perfil.com/sitemap/archive/{year}/{month}' for year in range(2023, 2021, -1) for month in range(12, 0, -1)], # from 2023 to 2022 #consider 45k entries for data upto 2023-05
    'lagaceta' : ['https://www.lagaceta.com.ar/rss/sitemapOrganic', 'https://www.lagaceta.com.ar/rss/sitemap_news',], # weak sitemap # only 2023-10-10/11. Where even is the search bar??
    'tiempoar': [], # no sitemap. manual collection
    # 'rionegro': [f'https://www.rionegro.com.ar/sitemap.xml?yyyy={year}&mm={month}&dd={day}' for year in range(2023, 2021, -1) for month in range(12, 0, -1) for day in range(31,0,-1)], # data from 2023 to 2022. consider 60k entries for data upto 2023-05
    'tn' : [f'https://tn.com.ar/arc/outboundfeeds/sitemap/?outputType=xml&from={i}' for i in range(500)], # 2023-10
    # 'eldestapeweb': ['https://www.eldestapeweb.com/sitemap.xml'] + [f'https://www.eldestapeweb.com/sitemap-index/sitemap{i}.xml' for i in range(360)], # 2023-2022
    'a24': ['https://www.a24.com/sitemap.xml', 'https://www.a24.com/sitemap-news.xml'], # weak sitemap. Do manually
    # 'c5n': [f'https://www.c5n.com/sitemap/news-full/sitemap-{year}{month:02}.xml' for year in range(2023,2021,-1) for month in range(12,0, -1)] # 2023-2022
}



DATA_DIR = 'data/hrefs/'

# based on the xml sitemaps, collect all the hrefs for every website
def collect_hrefs(website, seed_xmls):

    visited = set()
    to_visit = set(seed_xmls)
    hrefs = set()

    while to_visit:
        # format
        print(f'visits:{len(visited):>4}/{len(to_visit):<4}    hrefs:{len(hrefs):<5}   website:{website:<15}')
        sitemap = to_visit.pop()
        visited.add(sitemap)
        try:
            req = requests.get(sitemap)
        except Exception as e:
            print(e)
            continue

        # extract all the location elements from the sitemap
        soup = BeautifulSoup(req.text, 'lxml-xml')
        locations = soup.find_all('loc')
        
        # add all the hrefs to the href set and xml sitemaps to the to_visit set
        for loc in locations:
            if (loc.text.endswith('.xml') or loc.parent.name=='sitemap') and loc.text not in visited:
                loc.text.replace('.xml.gz', '.xml')
                to_visit.add(loc.text)
            
            else:
                hrefs.add(loc.text)

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # write down the collected hrefs in a file
    with open(DATA_DIR+ website + '/_hrefs.txt', 'w') as f:
        for href in hrefs:
            f.write(href + '\n')

    return


if __name__ == '__main__':

    # start a new process for each website using multiprocessing
    import multiprocessing as mp
    processes = []
    for website in xml_dicts:
        p = mp.Process(target=collect_hrefs, args=(website, xml_dicts[website],))
        p.start()
        processes.append(p)

    # wait for all the processes to finish
    for p in processes:
        p.join()

    print('Done!')


