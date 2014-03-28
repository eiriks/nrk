# coding: utf-8
import re, logging
#################################################################################
# Instillinger for scraperen.                                                   #
# Den absolutt enkleste måten å lagre instillinger på er å gjøre det som dette. #
# Da kan vi enkelt stille inn ting på scraperen uten å måtte kjøre grep -r. ^_^ #
# Andre som ser på dette må gjerne legge til flere instillinger og slikt,       #
# Bare ikke overkjør ting som allerede er definert.                             #
#################################################################################


##        [Scraper]
# Hvor sikker i prosent må vi være på at et språk er det det utgir seg for å være før vi akspeterer svaret, fra 0.0 til 1.0, hvor 1.0 er 100% sikker
language_identification_threshold = 0.40 #dvs, 40% sikker. Ganske lavt, men det funker for nå.

scraping_request_stagger =  0.45 # 1100 # 1100 i sekunder, aka 1.1 sec

# Dersom vi ikke vet hva språk vi har, hvilken streng skal vi bruke til å identifisere med?
uncertain_language_string = "NA"

# set up logging
# CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
logger_level = logging.ERROR

# Examples from nrk.no: (NTB), (©NTB), (NRK/Reuters), (NTB/Reuters), etc.
syndicators = [
    'NTB', '©NTB', 'NRK/Reuters', '©NRK','AFP', 'NRK/Reuters/AFP/AP', 
    'NTB-AFP','NRK-NTB-AFP-Reuters'
    ]
# Other known agencies: http://en.wikipedia.org/wiki/News_agency
syndicators.extend([
    'ANSA','APA', 'Xinhua', 'ITAR-TASS','ABC', 'ACN', 'EPA','Fox News',
    'FOX','Reuters','PA','AP','DPA', 'UPI','BNO','AHN','ANSA','NYT', 
    'NBC','BBC'
    ])
# Should not match: (FBI), (ORHA), (SAS)

def matches_pattern(s, pats):
    pat = "|".join("(\(.?%s.?\w*\))" % p for p in pats)     # print pat
    mObj = re.search(pat, s, re.I)                          # print mObj.group()
    if bool(mObj):
        #print u"Nyhetabyrå: %s" % mObj.group()
        return mObj.group()
    else: 
        return None



##        [Database]
# Ting som vi må vite om databasen vi skal snakke til. 
rdbms_hostname = "localhost"
rdbms_username = "scraper"
rdbms_password = "reparcs"

# local
rdbms_hostname = "localhost"
rdbms_username = "root"
rdbms_password = "root"



# Planen er å legge ut SQL-kommandoene i seperate filer vi kan deretter lese fra og redigere uten å måtte tenke på Python

