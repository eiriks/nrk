#!/bin/bash

##

while read p; do
    python -W ignore runme.py $p
done < ~/pythonjobb/nrk/nrklenker.minimalt.txt
