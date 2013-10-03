# coding: utf-8
from bs4 import BeautifulSoup
from time import strptime
from itertools import izip
from urllib2 import unquote
import langid
from settings import language_identification_threshold
from settings import uncertain_language_string

## This function does the Right Thing™ when given a beautifulsoup object created over an nrk page with their new template
## This is mostly stolen from the old functions.
def nrk_2013_template(soup, dictionary):
    """Tar et BeautifulSoup objekt og returnerer et map av data
    Modifiserer dictionary argumentet du gir inn."""
    
    # Finn forfatter(e)
    byline = soup.find('div', 'byline')
    authors = []
    
    # wrapper denne i en try/except midlertidig for å komme fram til tekst jeg kan kjøre LIX på. (Eirik)
    try:
        for address, li in izip(byline.find_all('address'), byline.find_all('li', 'icon-email')):
            authorName = address.find(class_='fn').string
            # NRK is still trying to hide the email address
            # from spammers.
            href = li.a['href']
            authorMail = unquote(href[21:-1])[7:]
            authorRole = address.find(class_='role').string.strip()
            author = [authorName, authorMail, authorRole]
            authors.append(author)
    except AttributeError:
        # og adder denne som en påminndelse om at vi må skrive dette noe mer robust for variasjoner (Eirik)
        print "unntakshåndtering må på plass"

    dictionary['authors'] = authors
    # Finn publiseringsdato
    dictionary['published'] = strptime(soup.time['datetime'][0:19], "%Y-%m-%dT%H:%M:%S")

    # Finn overskrift
    dictionary['headline'] = soup.header.find('div', 'articletitle').h1.text # .text gived unicode, .string gives 'bs4.element.NavigableString'


    updateString = "NO UPDATES"
    updated = soup.find('div', 'published').find('span', 'update-date')
    if updated:
        updateString = updated['title']
        updateString = updateString[:10], updateString[16:21].replace('.', ':')
        
    dictionary['updated'] = updateString

    # Finn brødtekst
    body = "";
    for para in soup.find_all('p'):
        body += (para.text + "\n")


    dictionary['body'] = body

    (language, certainty) = langid.classify(body)
    language_code = uncertain_language_string
    if (certainty > language_identification_threshold):
        language_code = language

    dictionary['language'] = language_code

    return dictionary

def import_virker():
    print "importing works for nrk_2013_template.py"

