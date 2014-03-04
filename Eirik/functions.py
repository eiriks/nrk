#coding: utf-8

import re
import tldextract
import logging
import requests
#from bs4 import BeautifulSoup

logger = logging.getLogger('nrk2013.nrk_new_tamplate')

def get_video(soup, data, dictionary):
    video_markup = [] 
    VIDEOS_TAGS = ['iframe', 'embed', 'object', 'video']
    VIDEO_PROVIDERS = ['youtube', 'vimeo', 'dailymotion', 'kewego']
    #print ",".join(VIDEOS_TAGS)
    for t in VIDEOS_TAGS:
        if soup.find_all(t):
            for vid in soup.find_all(t):
                # youtube og vimeo kan avsløres ver src atributt til iframe tag
                for prov in VIDEO_PROVIDERS:
                    if prov in vid['src']:
                        video_markup.append(vid)

    #print video_markup 
    print "antall videoer (ikke nrk): ", len(video_markup)

    # nrk-videoer (lastet via js, og må trikses med)
    # ser ut som eksistensen av en data-video-id="118648" kan være en bedre indikator.. 
    nrk_videoer = soup.select('figure.video')
    print "antall nrk-videoer: ", len(nrk_videoer)


    dictionary['video_files'] = len(video_markup)
    dictionary['video_files_nrk'] = len(nrk_videoer)
    return 


def count_iframes(soup, data, dictionary):
    # Tell opp iframe. BeautifulSoup teller feil på "http://www.nrk.no/mr/enorm-nedgang-i-antall-filmbutikker-1.11261850", så vi bruker en regex her istedenfor.
    # Hvis noen finner ut hvordan jeg bruker BS istedenfor, gi meg en lyd. (soup.find_all("iframe") hvirket ikke) – Haakon
    return len(re.findall("<iframe src=", data))

def count_js(soup, data, dictionary):
    '''As js can be internal and external, a char count is perhaps a good indicator?'''
    count = 0

    logger.debug("antall script-tagger: %s", len(soup.select("script")) )
    #print soup.select("script")
    a = "".join([l.text for l in soup.select("script")])

    logger.debug( "antall karakterer i script %s: ", len(a) )
    count+=len(a)
    # then external scripts
    for doc in soup.select("script[src]"):
        if doc['src'].startswith("http") or doc['src'].startswith("www"): # lurt med "or"?
            js_url = doc['src']
        else:
            ext = tldextract.extract(dictionary['url'])
            js_url = 'http://'+'.'.join(ext[:3])+doc['src']
        logger.info(js_url)
        r = requests.get(js_url)
        logger.debug( "lengde på eksternt js: %s", len(r.text) )
        count+=len(r.text)
        #print "count: ", count
    return count        


def count_css(soup, data, dictionary):
    count = 0
    # add internal css
    count += len("".join([l.text for l in soup.select("style")]))
    logger.debug( "antall css-karakterer %s", count )
    # then external 
    for doc in soup.select("link[rel^stylesheet]"):
        if doc['href'].startswith("http"):
            css_url = doc['href']
        else:
            ext = tldextract.extract(dictionary['url'])
            css_url = 'http://'+'.'.join(ext[:3])+doc['href']
        r = requests.get(css_url)
        count += len(r.text)
    return count

def count_links(soup, data, dictionary):

    # new_logger = logging.getLogger('nrk2013.nrk_new_tamplate')
    # only a's inside the article tag (not the menus and stuff)
    a = soup.article.find_all("a")

    lenker = []

    # these links we do not want to include..
    not_published_links = soup.select(".published a")
    not_sharing_links = soup.select(".sharing a")
    not_byline_links = soup.select(".byline a")
    # should we remove the whole aside-element? (I want to include the fack-box, but not "related stories")
    # we should remove all links that have a[href] javascript:location....
    # remove those..
    a = set(a) - set(not_published_links + not_sharing_links + not_byline_links)

    for lenke in a:
        href = lenke.get('href')
        if href != None:
            lenker.append(href)

    internal_domains = ['nrk','dit', 'ut', 'yr', 'p3', 'nrkaktivum', 'nrkbeta', 'nrkbutikken', 'nrksuper']
    # javascript ? mailto? 
    
    interne_lenker = []
    eksterne_lenker = []
    for lenke in lenker:
        # her må det en sjekk om url'n finnes i en liste av domener...
        ext = tldextract.extract(lenke)     # https://pypi.python.org/pypi/tldextract
        if ext.domain in internal_domains:
            interne_lenker.append(lenke)
        else:
            eksterne_lenker.append(lenke)

    dictionary['external_links'] = eksterne_lenker
    dictionary['internal_links'] = interne_lenker
    return
