#!/usr/bin/python2.7
# coding: utf-8
from bs4 import BeautifulSoup
import datetime 
import requests

### Hjelpefunksjoner
def nrk_ny_dato_til_timestamp(pubstring):
    """Creates a timestamp from quote-unquote parsing NRK's date format.
    The format assumed is: [DD.MM.YYYY, kl. HH.MM.]"""
    year   = int(pubstring[6:10])
    month  = int(pubstring[3:5])
    day    = int(pubstring[0:2])
    hour   = int(pubstring[16:18])
    minute = int(pubstring[19:21])
    return datetime.datetime(year, month, day, hour, minute).strftime("%s")

def soup_from_url(url):
    "Tar en URL og returnerer et BeautifulSoup objekt"
    return BeautifulSoup(requests.get(url).text)

def dispatch_on_template(soup):
    print "WARNING: Unimplemented method."
    print "Will naively assume that it's the new NRK-template"
    return nrk_2013_template(soup)

### Hovedfunksjoner

## Entry points
def analyze_url(url):
#    dict = dispatch_on_template(soup_from_url)
    dict = {"url":url, "text":"TEKST VILLE VÆRT HER", "timestamp":9001}
    # add url to dict
    add_to_db(dict)
    return True

def analyze_urls(url_collection):
    for url in url_collection:
        analyze_url(url)
    return True

## Template dependent functions to dispatch to
def nrk_2013_template(soup):
    """Tar et BeautifulSoup objekt og returnerer et map av data
    Har ingen bieffekter."""

    # Finn forfatter(e)
    # Finn dato
    published = soup.find('div', 'published').find('span', 'publish-date')['title']
    timestamp = nrk_ny_dato_til_timestamp(published)
    #print timestamp

    # Finn overskrift

    # Finn brødtekst
    body = "";
    for para in soup.find_all('p'):
        body += (para.text + "\n")
    #return a dictionary, or pass control to the RDB entering function
    return "DONE"
    
## RDBMS dependent code
def add_to_db(dict):
    print "Warning: add_to_db(dict) is unimplemented"
    print "This function does nothing, and merely returns control after printing this message"
    db_conf = read_db_configuration()
    
    return

def read_db_configuration():
    """Reads the database configuration from the file database.conf in the same folder as the execution environment resides in.
    For now it is assumed that the type will ALWAYS be sqlite."""
    conf_dict = {}

    for line in open("database.conf", "r").read().split("\n"):
        if line == "":
            #EMPTY LINE SKIP ITERATION
            print "EMPTY LINE"
        else:
            print line
            pair = line.split(":")
            print pair
            print type(pair[0])
            {
            
        print conf_dict
    return conf_dict

## Running the code
url = "http://www.nrk.no/valg2013/1.11193015"

analyze_url(url)

