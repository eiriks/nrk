#!/usr/bin/python2.7
# coding: utf-8

## Imports from other files (and libraries). This keeps the scriptfile lean, mean, and clean.
## It also lets me write tests, embellishments, helper functions, and more and stuff it there.

import urllib2
from bs4 import BeautifulSoup
import datetime 
import requests    # Brukes til å laste ned fra internettene med. Akkurat nå som den bruker samme file om igjen hver gang brukes den ikke.
from nrk_new_template import nrk_2013_template
from rdbms_insertion import add_to_db
from analyze_url import analyze_url
import re

# Dette skulle hjelpe?
# En ekte glob!
request = False

### Hjelpefunksjoner
def soup_from_url(url):
    """Tar en URL og returnerer et BeautifulSoup objekt
       Nå som vi er under utvikling returnerer vi en suppe basert på en html-fil vi allerede har lagret."""
    try:
        request  = requests.get(url)
        data = request.text # Dette er det vi egentlig skal gjøre
        request.close() # Forhåpentligvis fikser dette problemet med at vi har for mange filer oppe
    except requests.exceptions.TooManyRedirects: # Dette skjedde på noen radiokanaler eller noe.
        print "{} has does not evaluate properly, and we will infinitely redirect".format(url)
        return False
    #data = open("testhtml/ny.template.html", "r").read() # Dette er bare nå som vi tester for NRK ny.
    bs = BeautifulSoup(data)
    return [bs, data]

def soup_from_live_url(url):
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    return soup

def dispatch_on_template(soup, data, dictionary):
    # en kjapp hack: Det nye templatet bruker html5, den gamle bruker xhtml, så vi sjekker bare hvilken det er snakk om.
    # Vi vet også at den nye har en adresse til seg selv nederst, i motsetning til de gamle.
    if re.match("<!doctype html>", data) and len(re.findall('<input type="text" value=".*" readonly="readonly"', data)) == 1:
        return nrk_2013_template(soup, data, dictionary)
    elif re.match('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">', data):
        print "GAMMELT TEMPLATE, IKKE STØTTET ENDA."
        return False
    else:
        print "Uvisst hvilken template, vi hopper over denne."
        return False

  ### Hovedfunksjoner

## Entry points
def main(url):           
    dictionary = {'url':url, 'timestamp':datetime.datetime.now()}     # Oppretter første dictionary, med url og datetime for når vi laster ned.
    dictionary = analyze_url(dictionary)                              # Analyserer URL med hensyn på ting vi ville ha med.
    souplist = soup_from_url(url)
    if souplist == False: # If something went horribly wrong, we just return
        return
    soup = souplist[0]
    data = souplist[1]
    dictionary = dispatch_on_template(soup, data, dictionary)         # Henter ut data som må hentes ut spesifikt fra hver side.
    if(dictionary != False):
        add_to_db(dictionary)                                         # Hiver hele herligheten inn i databasen vår.
        return dictionary                                             # Returnerer det vi har laget i tilfelle det skulle være interessant. (til dømes, dersom et annet program skulle kalle denne funksjonen)
    else:
        return False

def mains(url_collection):
    for url in url_collection:
        analyze_url(url)
    return "DONE"

## Running the code (Alt her er bare testing og ting.)
url = "http://www.nrk.no/livsstil/hvordan-bli-den-ultimate-jegeren-1.11286386" # Dette er ren juks, bare så det er sagt. Denne strengen er bare her for testingens skyld.
main(url)

#print requests.get("http://www.nrk.no/valg2013/1.11290083").url
