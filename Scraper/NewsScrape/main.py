from Scraper.NewsScrape import cleaner
import scrapy
from scrapy.crawler import CrawlerProcess
from NewsScrape.spiders import parker
import time
import os

print(f'\n########Σύστημα συγκομιδής και δεικτοδότησης σελίδων########\n')
print(f'####Project Γλωσσικής Τεχνολογίας - Σεπτέμβρης 2021####\n')

user_in = input(f'Run spider? Y/N: ')
if user_in.upper() == 'Y':
    t1_start = time.process_time()
    os.chdir('NewsScrape\spiders')
    os.system('scrapy crawl parker')
    print(f'Spider finished, scraping took {time.process_time()-t1_start} seconds\n')
    print(f'The scraped content can be found under Results')
    os.chdir('../../')


user_in = input('Run parser? Y/N: ')
if user_in.upper() == 'Y':
    cleaner.get_html_text()
