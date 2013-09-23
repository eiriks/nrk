# coding: utf-8
from bs4 import BeautifulSoup
from time import strptime


## This function does the Right Thing™ when given a beautifulsoup object created over an nrk page with their new template
def nrk_2013_template(soup, dictionary):
    """Tar et BeautifulSoup objekt og returnerer et map av data
    Modifiserer dictionary argumentet du gir inn."""

    # Finn forfatter(e)
    # Finn dato

    # TODO: FIKS ↓
    # En massiv kludge ↓, som ikke skal sees av noen med sarte sjeler. Bytter ut NRKs representasjoner av sommer og vintertid med Pythons.
    published = strptime(soup.time['datetime'][0:19], "%Y-%m-%dT%H:%M:%S")
    print published
    # timestamp = nrk_ny_dato_til_timestamp(published)
    #print timestamp
    
    # Finn overskrift

    # Finn brødtekst
    #body = "";
    #for para in soup.find_all('p'):
    #body += (para.text + "\n")
    #dictionary['body'] = body
    return dictionary

def import_virker():
    print "importing works for nrk_2013_template.py"

