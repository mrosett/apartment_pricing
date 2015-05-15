__author__ = 'Max Rosett'

from bs4 import BeautifulSoup
import requests
import random
import time
import pandas as pd

'''
def clean_housing(housing_str):
    return housing_str
result = open("sf_apts.html","r").read()
soup = BeautifulSoup(result)'''

next = 'https://sfbay.craigslist.org/search/sfc/apa'

listings = []

while next is not None:
    print(next)

    result = requests.get(next)
    soup = BeautifulSoup(result.content)
    #result = open("sf_apts.html","r").read()
    #soup = BeautifulSoup(result)
    next = soup.find('link', rel='next')['href']

    for listing in soup.find_all("p", "row"):
        list_dict = {}
        list_dict['data-pid'] = listing['data-pid']
        if listing.has_key('data-repost-of'):
            list_dict['data-repost-of'] = listing['data-repost-of']
        list_dict['href'] = listing.find("a", "hdrlnk")['href']
        list_dict['description'] = listing.find("a", "hdrlnk").get_text().strip()
        if listing.find("span", "price") is not None:
            list_dict['price'] = listing.find("span", "price").get_text().strip()
        if listing.find("span", "housing") is not None:
            list_dict['housing'] = listing.find("span", "housing").get_text().strip()
        if listing.find("span", "pnr").find("small") is not None:
            list_dict['neighborhood'] = listing.find("span", "pnr").find("small").get_text().strip()
        list_dict['time'] = listing.find("time")['datetime']
        listings.append(list_dict)

    time.sleep(random.randint(5,10))

df = pd.DataFrame(listings)

df.to_csv('sf_scrape.csv')

'''saved_html= open("sf_apts.html","w")
saved_html.write(str(soup.prettify()))
saved_html.close()'''