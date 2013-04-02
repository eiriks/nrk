#!/usr/bin/python
# coding: utf-8

from bs4 import BeautifulSoup
from argparse import ArgumentParser

class Page:
    def __init__(self, url):
        self.url = url

def analyse(url=''):
    page = Page(url)

if __name__ == '__main__':
    parser = ArgumentParser(description='Analyse nrk url.')
    parser.add_argument('url', metavar='URL')
    args = parser.parse_args()
    analyse(url=args.url)
