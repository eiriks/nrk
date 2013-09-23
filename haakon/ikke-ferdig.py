#!/usr/bin/python2.7
# coding: utf-8

## Imports from other files (and libraries). This keeps the scriptfile lean, mean, and clean.
## It also lets me write tests embellishments, helper functions and more and stuff it there.
 
from bs4 import BeautifulSoup
import datetime 
import requests
from nrk_new_template import nrk_2013_template
from rdbms_insertion import add_to_db


### Hjelpefunksjoner
def soup_from_url(url):
    "Tar en URL og returnerer et BeautifulSoup objekt"
    return BeautifulSoup(requests.get(url).text)

def dispatch_on_template(soup, dictionary):
    print "WARNING: Unimplemented method."
    print "Will naively assume that it's the new NRK-template"
    return nrk_2013_template(soup, dictionary)

### Hovedfunksjoner

## Entry points
def analyze_url(url):
    dictionary = {"url":url, "text":"TEKST VILLE EKSISTERT HER", "timestamp":9001}
    dictionary = dispatch_on_template(soup_from_url(url), dictionary)
    # add url to dictionary
#    add_to_db(dictionary)
    return dictionary

def analyze_urls(url_collection):
    for url in url_collection:
        analyze_url(url)
    return "DONE"

## Running the code
url = "http://www.nrk.no/valg2013/1.11193015"

#analyze_url(url)

