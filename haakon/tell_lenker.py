#coding: utf-8

import re
import tldextract
import logging

def tell(soup, data, dictionary):
    # create logger with 'tldextract'
    logger = logging.getLogger('tldextract')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('spam.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    a = soup.find_all("a")
    lenker = []
    for lenke in a:
        href = lenke.get('href')
        if href != None:
            lenker.append(href)
    domain = (tldextract.extract(dictionary['url']))[1]
    
    interne_lenker = []
    eksterne_lenker = []
    for lenke in lenker:
        if domain in lenke:
            interne_lenker.append(lenke)
        else:
            eksterne_lenker.append(lenke)

    dictionary['external_links'] = eksterne_lenker
    dictionary['internal_links'] = interne_lenker
    return
