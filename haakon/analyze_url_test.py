#! /usr/bin/python2.7
# coding: utf-8
from analyze_url import analyze_url

with open ("/home/haakon/pythonjobb/nrk/haakon/testhtml/url.txt") as lenkekilde:
    lenker = lenkekilde.readlines()

for lenke in lenker:
    oppslag = analyze_url({'url':lenke})
    if oppslag['programtilknytning'] == "Juntafil":
        print "junta"
