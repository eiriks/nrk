#!/usr/bin/python
# coding: utf-8

from bs4 import BeautifulSoup
from argparse import ArgumentParser
from urllib2 import build_opener
from re import match

class Page:
    def __init__(self, url=None):
        self.url = url
        self.published = {'date':'na', 'time':'na'}
        self.updated = {'date':'na', 'time':'na'}
        self.authors = []
        self.links = {'internal':0, 'external':0}

class Author:
    def __init__(self):
        self.name = None
        self.email = None

class Analyser:
    """
    Analyser for NRK articles.

    """

    def headers = [('User-agent',
                    'UiB NRK Proj (Contact: Eirik.Stavelin@infomedia.uib.no)')]
    def __init__(self):
        self.pagereader = build_opener()
        self.pagereader.addheaders(headers)
    def _analyse_old(url=None):
        doc = pagereader.open(url, None, 15)
        soup = BeautifulSoup(doc)
        page = Page(url)
        return page

    def _analyse_new(url=None):
        doc = pagereader.open(url, None, 15)
        soup = BeautifulSoup(doc)
        page = Page(url)
        return page

    def analyse(url=None):
        """
        Analyses NRK pages and returns a Page object ready
        for database serialization.

        Keyword argument:
        url -- the url from NRK to analyse

        returns a Page object.

        """
        if not url:
            raise TypeError("analyse needs 1 argument.")

        if match('^.*/\d\.\d+$', url):
            return analyse_old(url)
        else:
            return analyse_new(url)

if __name__ == '__main__':
    parser = ArgumentParser(description='Analyse nrk url.')
    parser.add_argument('url', metavar='URL')
    args = parser.parse_args()
    analyser = Analyser()
    analyser.analyse(url=args.url.strip())
