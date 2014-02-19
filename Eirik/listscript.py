#!/usr/bin/python2.7
# coding: utf-8

import time
from ikke_ferdig import main as start

urls = []
with open("../nrklenker.minimalt.txt") as f:
    urls = f.readlines()

for url in urls:
    print url.strip()
    start(url.strip())
    print ""
    time.sleep(1)

#start("http://www.nrk.no/livsstil/test-av-norges-mest-solgte-brod-1.8352163")
