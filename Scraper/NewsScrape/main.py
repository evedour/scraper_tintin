from Scraper.NewsScrape import cleaner
from Scraper.NewsScrape import tokenizer
from Scraper.NewsScrape import indexer
import scrapy
from scrapy.crawler import CrawlerProcess
from NewsScrape.spiders import parker
import connect_to_db
import os
import index_query
import time


print(f'\n########Σύστημα συγκομιδής και δεικτοδότησης σελίδων########\n')
print(f'####Project Γλωσσικής Τεχνολογίας - Σεπτέμβρης 2021####\n')
print('##########################################################')

def make_query():
    flag = True
    while flag:
        print('You can type \"END\" to exit')
        inputs = input('Enter your query: ')
        if inputs.upper() == 'END':
            flag = False
            break
        as_list = inputs.split(" ")
        query_as_list = []
        for i in as_list:
            query_as_list.append(i)
        timer_start = time.time()
        index_query.query(query_as_list)
        print(f'Query \"{inputs}\" took {time.time()-timer_start} seconds')



user_in = input(f'Run spider? Y/N: ')
if user_in.upper() == 'Y':
    t1_start = time.process_time()
    os.chdir('NewsScrape\spiders')
    os.system('scrapy crawl parker')
    print(f'Spider finished, scraping took {time.process_time()-t1_start} seconds\n')
    print(f'The scraped content can be found under Results')
    os.chdir('../../')

print('Before continuing, remember to open wamp server')
user_in = input('Run parser? Y/N: ')
if user_in.upper() == 'Y':
    cleaner.get_html_text()

user_in = input('Run tokenizer? Y/N: ')
if user_in.upper() == 'Y':
    tokenizer.tokenize()

user_in = input('Run vector representation? Y/N: ')
if user_in.upper() == 'Y':
    links = connect_to_db.get_all()
    indexer.indexer(links)

make_query()
