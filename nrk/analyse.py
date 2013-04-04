#!/usr/bin/python
# coding: utf-8

from argparse import ArgumentParser
from OldPageAnalyser import OldPageAnalyser
from NewPageAnalyser import NewPageAnalyser
from re import match

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
        return OldPageAnalyser(url)
    else:
        return NewPageAnalyser(url)

if __name__ == '__main__':
    parser = ArgumentParser(description='Analyse nrk url.')
    parser.add_argument('url', metavar='URL')
    args = parser.parse_args()
    analyse(url=args.url.strip())
