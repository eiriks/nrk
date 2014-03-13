#!/usr/bin/python2.7
# coding: utf-8

from bs4 import BeautifulSoup
import requests
import re
from ghost import Ghost # hva med Ghost.py - http://jeanphix.me/Ghost.py/
import time
import logging
import json

logger = logging.getLogger('disqus')
# by using Ghost I can get the url
# http://disqus.com/embed/comments/?base=default&amp;disqus_version=b86e4cc3&amp;f=nrk-ytring&amp;t_i=1.11580300&amp;t_u=http%3A%2F%2Fwww.nrk.no%2Fytring%2Fhandlekraftig-eller-handlingslamma_-1.11580300&amp;t_d=Handlekraftig%20eller%20handlingslamma%3F&amp;t_t=Handlekraftig%20eller%20handlingslamma%3F&amp;s_o=default#2

def get_disqus_comments_by_ghost(dictionary):
    '''Uses Ghost to trigger url for iframe,
    then requests to fetch that html,
    and finally get the json from failed-page from disqus.. 
    '''
    ghost = Ghost(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:25.0) Gecko/20100101 Firefox/25.0', viewport_size = (1349, 765), log_level=logging.ERROR)
    # user_agent='Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7', viewport_size = (320, 480) 
    page, resources = ghost.open(dictionary['url'])
    assert page.http_status == 200      # make use we get data back..
    ghost.wait_for_page_loaded()        # probably does no harm..

    # comment loaded on scroll hack cred goes to Hammer et al. (2013)
    secs = 0.50
    time.sleep(secs)
    ghost.evaluate("window.scroll(0, 700);")
    ghost.capture_to('scroll_before.png')       # do not get why this fails if i remove this image-capture function...
    time.sleep(secs)
    ghost.evaluate("window.scroll(0, 1400);")
    time.sleep(secs)
    ghost.evaluate("window.scroll(0, 2100);")
    time.sleep(secs)
    ghost.evaluate("window.scroll(0, 4000);")
    time.sleep(secs)
    ghost.wait_for_page_loaded()                #ghost.capture_to('scroll_after.png')
    logger.info("waiting for selector IFRAME")
    ghost.wait_for_selector("iframe") ##post-list

#    print ghost.content
    soup = BeautifulSoup(ghost.content)
    try:
        comments_iframe_url = soup.select("iframe#dsq-2")[0]['src'] # only one of these...
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:25.0) Gecko/20100101 Firefox/25.0',
        #     'X-UA-Compatible': 'IE=edge'
        # }
        comments_html = requests.get(comments_iframe_url) # , headers=headers
        #print comments_html.text
        iframe_soup = BeautifulSoup(comments_html.text)
        posts = iframe_soup.select("#disqus-threadData")
        data = json.loads(posts[0].text)
        
        #print type(data)
        return data['response']['thread']['posts']
    except:
        # fetching comments failed
        return -9999

def get_disqus_comments(dictionary):
	# http://disqus.com/embed/comments/?f=nrk-ytring&amp;t_i=1.11177825&amp;t_u=http%3A%2F%2Fwww.nrk.no%2Fytring%2Ffrihet-i-fellesskap-1.11177825&amp;t_d=Frihet%20i%20fellesskap&amp;t_t=Frihet%20i%20fellesskap&amp;s_o=default&amp;disqus_version=1381535643#2
	# http://disqus.com/embed/comments/
	#?f=nrk-ytring
	#&amp;t_i=1.11177825
	#&amp;t_u=http%3A%2F%2Fwww.nrk.no%2Fytring%2Ffrihet-i-fellesskap-1.11177825
	#&amp;t_d=Frihet%20i%20fellesskap
	#&amp;t_t=Frihet%20i%20fellesskap
	#&amp;s_o=default
	#&amp;disqus_version=1381535643#2

	# http://disqus.com/embed/comments/
	#?base=default
	#&disqus_version=242c4cf2
	#&f=nrk-ytring
	#&t_i=1.11580300
	#&t_u=http%3A%2F%2Fwww.nrk.no%2Fytring%2Fhandlekraftig-eller-handlingslamma_-1.11580300
	#&t_d=Handlekraftig%20eller%20handlingslamma%3F
	#&t_t=Handlekraftig%20eller%20handlingslamma%3F
	#&s_o=default#2
    format_string = "http://disqus.com/embed/comments/?f={}&t_i={}"
    saksnummer = re.findall("[0-9]\.[0-9]*$", dictionary['url']) # Dette henter ut id-tallet på slutten av url-en.
    saksnummer = saksnummer[0]
    print saksnummer
    hvem = "nrk-ytring"
    
    url = format_string.format(hvem, saksnummer)
    print url
    req = requests.get(url)
    print req

    return req

def num_comments(dictionary):
	return get_disqus_comments_by_ghost(dictionary)
	#print "NÅ ER VI FPR LANGT"
	# req = get_disqus_comments(dictionary)
	# return len(re.findall('"author":{"username":', req.text))

#dict = {'url':"http://www.nrk.no/ytring/lukkete-valg-i-en-apen-verden-1.11275011"}
    
