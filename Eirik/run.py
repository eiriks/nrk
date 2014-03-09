#!/usr/bin/python2.7
# coding: utf-8


import urllib2
from bs4 import BeautifulSoup
import datetime 
import requests  # requests.readthedocs.org 
from templates import nrk_2013_template, nrk_alfa_template
from rdbms_insertion import add_to_db
from analyze_url import analyze_url
import re, sys
import sqlite3 as lite

from connect_mysql import connect

# set up logging
# CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET

import logging
from rainbow_logging_handler import RainbowLoggingHandler
# create logger with 'tldextract'
logger = logging.getLogger('nrk2013')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('spam.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
#ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG) # logging.ERROR # til skjerm, antagelig vis.
rainbow_handler = RainbowLoggingHandler(sys.stderr, color_funcName=('black', 'yellow', True))
rainbow_handler.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
# logging.Formatter() '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter("[%(asctime)s] %(name)s %(funcName)s():%(lineno)d\t%(message)s")

#


#rainbow_handler.setLevel(logging.DEBUG)


fh.setFormatter(formatter)
#ch.setFormatter(formatter)
rainbow_handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(rainbow_handler)
logger.addHandler(fh)
#logger.addHandler(ch)


# Dette skulle hjelpe?
# En ekte glob!
request = False

### Hjelpefunksjoner
def soup_from_url(url):
    """Tar en URL og returnerer et BeautifulSoup objekt
       Nå som vi er under utvikling returnerer vi en suppe basert på en html-fil vi allerede har lagret."""
    try:
        request  = requests.get(url)
        data = request.text
        #request.close() # Forhåpentligvis fikser dette problemet med at vi har for mange filer oppe
    except requests.exceptions.TooManyRedirects: # Dette skjedde på noen radiokanaler eller noe.
        print "{} has does not evaluate properly, and we will infinitely redirect".format(url)
        logger.error("Could'n get the url from server")
        return False
    #data = open("testhtml/ny.template.html", "r").read() # Dette er bare nå som vi tester for NRK ny.
    bs = BeautifulSoup(data)
    return [bs, data]

# def soup_from_live_url(url):
#     soup = BeautifulSoup(urllib2.urlopen(url).read())
#     return soup

def dispatch_on_template(soup, data, dictionary):
    # en kjapp hack: Det nye templatet bruker html5, den gamle bruker xhtml, så vi sjekker bare hvilken det er snakk om.
    # Vi vet også at den nye har en adresse til seg selv nederst, i motsetning til de gamle.
    if re.match("<!doctype html>", data) and len(re.findall('<input type="text" value=".*" readonly="readonly"', data)) == 1:
        dictionary['template'] = 'ny2013'
        #logger.info("template: %s", dictionary['template'] ) 
        return nrk_2013_template.get(soup, data, dictionary)
    elif re.match('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">', data):
        dictionary['template'] = 'gammel2013'
        #logger.info("template: %s", dictionary['template'] ) 
        print "GAMMELT TEMPLATE, IKKE STØTTET ENDA."
        return False
    elif re.match("<!doctype html>", data) and len(soup.select("article.teaser")) == 1:
        dictionary['template'] = 'nrk_alfa'
        #logger.warn("template: %s url = %s" % (dictionary['template'],dictionary['url']))
        return nrk_alfa_template.get(soup, data, dictionary) 
    else:
        dictionary['template'] = 'ukjent'
        logger.info("template: Uvisst hvilken template, vi hopper over denne.") 
        #print "Uvisst hvilken template, vi hopper over denne."
        print soup.select("article.teaser"), len(soup.select("article.teaser"))
        print dictionary
        return False
    
    # tror at article.teaser er indikasjon på "alfa"-template



### Hovedfunksjoner

## Entry points
def create_dictionary(url):
    logger.info("prover med url: %s \n", url)          
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


def run_from_sqlite():
    con = None
    try:
        lite_con = lite.connect('nrk2013.db')    
        lite_cur = lite_con.cursor()    
        lite_sql = 'SELECT * FROM links ORDER BY date DESC LIMIT 10'
        lite_cur.execute(lite_sql) # 'SELECT SQLITE_VERSION()'        
        rows = lite_cur.fetchall()   #fetchone()

        # sjekk om url er scrapet i MYSQL db'n
        connection, cur = connect()

        # loop through SQLite set
        for row in rows:
            #print row[0], row[1], row[2] # 1 er url, 2 er tidspunkt for innsamling 
            # check if url is in mysql as url or url_self_link (either is fine)
            query = "SELECT * FROM page WHERE url = '%s' OR url_self_link = '%s'" % (row[1], row[1])
            cur.execute(query)
            rows = cur.fetchall()
            #print len(rows), row[1] # 1 full url hvis finnes i mysql
            if not len(rows):
                logger.info( "finnes, ikke, må settes inn" )
                create_dictionary(row[1])
    
                # hvis ikke, finn ut hvilken tamplate som er i bruk

        # scrape & lagre i mysql

        
    except lite.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)
    finally:
        if con:
            con.close()


def run_test_urlz():
    for url in test_urlz:
        create_dictionary(url)
        #import webbrowser
        #webbrowser.open(url=url,new=2)

test_urlz = [   'http://www.nrk.no/verden/opp-mot-80-batflyktninger-druknet-1.11277059',
    'http://www.nrk.no/ytring/boligprisene-faller.-og-hva-sa_-1.11387030','http://www.nrk.no/viten/enno-hap-for-ison-1.11386243',
    'http://www.nrk.no/ostlandssendingen/_-jeg-sa-nei-og-stopp-flere-ganger-1.11311493', 'http://www.nrk.no/livsstil/hvordan-bli-den-ultimate-jegeren-1.11286386',
    'http://www.nrk.no/verden/sju-av-ti-usa-spioner-permittert-1.11276333',
    'http://www.nrk.no/verden/williams-kritiserer-nobelkomiteen-1.11246780',
    'http://www.nrk.no/nordnytt/oppsiktsvekkende-blomsterfunn-1.11276684',
    'http://www.nrk.no/norge/drosjesjafor-domt-for-trakassering-1.11276262',
    'http://www.nrk.no/ytring/den-vanskelige-tvilen-1.11275460',
    'http://www.nrk.no/kultur/tom-clancy-er-dod-1.11275817',
    'http://www.nrk.no/kultur/intervju-med-forfatter-siri-hustved-1.11273929',
    'http://www.nrk.no/kultur/litteratur/jakter-pa-ulost-mysterium-1.11272464',
    'http://www.nrk.no/kultur/bridget-jones-oppfolger-sjokkerer-1.11271322',
    'http://www.nrk.no/programmer/tv/melodi_grand_prix/1.11251925',
    'http://www.nrk.no/programmer/tv/melodi_grand_prix/1.11122386',
    'http://www.nrk.no/fordypning/studentersamfundet-200-ar-1.11236099',
    'http://www.nrk.no/fordypning/lydband-fra-studentersamfundet-1.11248706',
    'http://p3.no/filmpolitiet/2013/10/rush/',
    'http://p3.no/filmpolitiet/2013/09/breaking-bad-er-ferdig-kva-no/',
    'http://www.nrk.no/livsstil/maten-som-holder-lengre-enn-angitt-1.11271204',
    'http://www.nrk.no/livsstil/test-av-barneyoghurt-1.11229993',
    'http://www.nrk.no/verden/kerry_-_-rapporten-er-nok-en-vekker-1.11267264',
    'http://www.nrk.no/hordaland/heftig-nordlys-pa-voss-i-natt-1.11276620',
    'http://www.nrk.no/norge/flere-forteller-om-trakassering-1.11276009',
    'http://www.nrk.no/kultur/freddy-fairhair-skaper-reaksjoner-1.11275174',
    'http://www.nrk.no/kultur/nrk-vil-sette-strikkerekord-1.11271394',
    'http://www.yr.no/nyheter/1.11274371',
    'http://www.nrk.no/magasin/natur/1.6952526',
    'http://www.nrk.no/livsstil/kaffekalkulator-1.11266219',
    'http://www.nrk.no/livsstil/lykketest/',
    'http://www.nrk.no/sapmi/stotter-samer-ved-a-demonstere-1.11276024',
    'http://www.nrk.no/sapmi/samegillii/sami-daidda-mielde-kultur_iehtadusa-1.11276898',
    'http://www.nrk.no/sapmi/sametinget-2013-2017-1.11239832',
    'http://www.nrk.no/valg2013/se-partiledernes-foredrag-1.11168181',
    'http://www.nrk.no/valg2013/slik-blir-stemmene-vare-fordelt-1.11228395',
    'http://www.nrk.no/valg2013/mandatfordelingen-2013-1.11225451',
    'http://www.nrk.no/valg2013/valgomat/',
    'http://www.nrk.no/sport/fotball/disse-lagene-er-vm-klare-1.11047107',
    'http://www.nrk.no/nyheter/innenriks/valg/valg2011/1.7790668',
    'http://www.nrk.no/direkte/',
    'http://p3.no/filmpolitiet/2013/10/gaten-ragnarok/',
    'http://www.yr.no/nyheter/1.11274768',
    'http://www.nrk.no/nordnytt/oppsiktsvekkende-blomsterfunn-1.11276684',
    'http://www.nrk.no/mat/1.11275477',
    'http://www.nrk.no/verden/_-usa-avlyttet-millioner-samtaler-1.11322481','http://www.nrk.no/kultur/pfu-avviser-bokbehandling-1.11388032',
    'http://www.nrk.no/verden/kamper-om-bagdad-1.677611','http://www.nrk.no/sport/anand-snakker-ut-etter-tapet-1.11388050',
    'http://www.nrk.no/livsstil/hvordan-bli-den-ultimate-jegeren-1.11286386','http://www.nrk.no/ostlandssendingen/_-jeg-sa-nei-og-stopp-flere-ganger-1.11311493',
    'http://www.nrk.no/valg2013/se-partiledernes-foredrag-1.11168181', 'http://www.nrk.no/sport/her-scorer-han-en-utrolig-touchdown-1.11389972']


if __name__ == '__main__':
    #run_from_sqlite()
    #run_test_urlz()
    #
    #create_dictionary("http://www.nrk.no/trondelag/brannsjefer-jubler-for-regn-1.11587449") # 6 relaterte.. 
    create_dictionary("http://www.nrk.no/trondelag/kongeorna-hekker-for-lite-1.11587021") # relatert-test
    #create_dictionary("http://www.nrk.no/nrksommer/kart/") # uklart template, uvanlig kartløsning
    #create_dictionary("http://www.nrk.no/sognogfjordane/navarsete-og-e16-i-laerdal-1.11457001") # nrk-intern kartløsning
    #create_dictionary("http://www.nrk.no/ytring/handlekraftig-eller-handlingslamma_-1.11580300") # komentarer
    #create_dictionary("http://www.nrk.no/viten/fra-harvard-til-verdensdominans-1.11509770")
    #create_dictionary("http://www.nrk.no/livsstil/natur-i-fort-film-_-_timelapse_-1.6542463")
    #create_dictionary("http://www.nrk.no/mr/moldes-uoffisielle-cupfinalesang-1.11372823")
    #create_dictionary("http://www.nrk.no/sport/her-scorer-han-en-utrolig-touchdown-1.11389972") # youtube
    #create_dictionary("http://www.nrk.no/valg2013/se-partiledernes-foredrag-1.11168181") # mange NRK-videoer
    # create_dictionary("http://www.nrk.no/kultur/tom-clancy-er-dod-1.11275817") # twitter 
    # create_dictionary("http://www.nrk.no/ostlandssendingen/_-jeg-sa-nei-og-stopp-flere-ganger-1.11311493") # faktaboks
    # create_dictionary("http://www.nrk.no/mat/1.11275477") # mat-template? 
    #create_dictionary("http://www.nrk.no/nordnytt/oppsiktsvekkende-blomsterfunn-1.11276684") # bildegalleri + bilder
    #create_dictionary("http://www.nrk.no/livsstil/norske-sjofugler-dor-ut-1.6952526") # bildegalleri og videoer 
    # create_dictionary("http://www.yr.no/nyheter/1.11274768") # yr-template, gammel?
    # create_dictionary("http://www.nrk.no/programmer/tv/melodi_grand_prix/1.11122386") # gammel template?
    # create_dictionary("http://p3.no/filmpolitiet/2013/10/gaten-ragnarok/") # p3-tamplate?
    # create_dictionary("http://p3.no/filmpolitiet/2013/09/breaking-bad-er-ferdig-kva-no/") # p3 + youtube
    # create_dictionary("http://p3.no/filmpolitiet/2013/10/rush/") # p3 + nrk-video + youtube
    # create_dictionary("http://www.nrk.no/direkte/") # alfa-portal, hva gjør vi her?   
    # create_dictionary("http://www.nrk.no/nyheter/innenriks/valg/valg2011/1.7790668") # gammel template?
    # create_dictionary("http://www.nrk.no/sport/fotball/disse-lagene-er-vm-klare-1.11047107") # mange faktabokser
    # create_dictionary("http://www.nrk.no/valg2013/valgomat/") # multimedia-greier
    # create_dictionary("http://www.nrk.no/valg2013/mandatfordelingen-2013-1.11225451") # multimedia-greier
    # create_dictionary("http://www.nrk.no/sapmi/samegillii/sami-daidda-mielde-kultur_iehtadusa-1.11276898") # samisk tekst
    # create_dictionary("http://www.nrk.no/livsstil/lykketest/") # interaktiv sak..
    # create_dictionary("http://www.nrk.no/livsstil/kaffekalkulator-1.11266219") # kalkulator.. (form = interaktivt element?)
    # create_dictionary("http://www.nrk.no/kultur/freddy-fairhair-skaper-reaksjoner-1.11275174") # twitter + youtube
    # create_dictionary("http://www.nrk.no/norge/flere-forteller-om-trakassering-1.11276009")   # twitter + nrk-video
    # create_dictionary("http://www.nrk.no/hordaland/heftig-nordlys-pa-voss-i-natt-1.11276620") # youtube 
    # create_dictionary("http://www.nrk.no/fordypning/lydband-fra-studentersamfundet-1.11248706") # nrk-lydfiler
    # create_dictionary("http://www.nrk.no/viten/enno-hap-for-ison-1.11386243") # interaktiv grafikk 

    #create_dictionary("http://www.nrk.no/magasin/_-som-a-sitte-i-et-fengsel-1.11570572") # snowfall style



