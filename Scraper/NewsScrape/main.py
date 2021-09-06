from Scraper.NewsScrape import cleaner
from Scraper.NewsScrape import tokenizer
from Scraper.NewsScrape import vector_representation
import scrapy
from scrapy.crawler import CrawlerProcess
from NewsScrape.spiders import parker
import time
import connect_to_db
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

user_in = input('Run tokenizer? Y/N: ')
if user_in.upper() == 'Y':
    tokenizer.tokenize()

user_in = input('Run vector representation? Y/N: ')
if user_in.upper() == 'Y':
    user_in = input('Please type "all" to run the program for the entire database or "one" to select an article by title: ')
    if user_in.lower() == 'all':
        links = connect_to_db.get_all()
    else:
        links = []
        user_in = 'Please insert a title: '
        links.append(connect_to_db.get_link_from_title(user_in))

    vector_representation.vectorize(links)
