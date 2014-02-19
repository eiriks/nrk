#!/usr/bin/python2.7
# coding: utf-8

from bs4 import BeautifulSoup
import requests
import re

# http://disqus.com/embed/comments/?f=nrk-ytring&amp;t_i=1.11177825&amp;t_u=http%3A%2F%2Fwww.nrk.no%2Fytring%2Ffrihet-i-fellesskap-1.11177825&amp;t_d=Frihet%20i%20fellesskap&amp;t_t=Frihet%20i%20fellesskap&amp;s_o=default&amp;disqus_version=1381535643#2
def get_disqus_comments(dictionary):
    format_string = "http://disqus.com/embed/comments/?f={}&t_i={}"
    saksnummer = re.findall("[0-9]\.[0-9]*$", dictionary['url']) # Dette henter ut id-tallet på slutten av url-en.
    saksnummer = saksnummer[0]
    hvem = "nrk-ytring"
    
    url = format_string.format(hvem, saksnummer)
    req = requests.get(url)
    
    return req

def num_comments(dictionary):
    req = get_disqus_comments(dictionary)
    return len(re.findall('"author":{"username":', req.text))

dict = {'url':"http://www.nrk.no/ytring/lukkete-valg-i-en-apen-verden-1.11275011"}
    
