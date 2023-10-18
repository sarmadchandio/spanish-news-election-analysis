# import the classes from news-crawlers.py
from tags_crawler import pagina12Scrapper, infobaeScrapper, clarinScrapper
import sys



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 engine.py <news_site>")
        sys.exit(1)

    news_site = sys.argv[1]

    Scrapper = None
    if news_site == 'pagina12':
        Scrapper = pagina12Scrapper()
    elif news_site == 'infobae':
        Scrapper = infobaeScrapper()
    elif news_site == 'clarin':
        Scrapper = clarinScrapper()
    else:
        print("The news site you have chosen is not supported")
        sys.exit(1)

    Scrapper.collect_hrefs()

