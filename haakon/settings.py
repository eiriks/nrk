# coding: utf-8

#################################################################################
# Instillinger for scraperen.                                                   #
# Den absolutt enkleste måten å lagre instillinger på er å gjøre det som dette. #
# Da kan vi enkelt stille inn ting på scraperen uten å måtte kjøre grep -r. ^_^ #
# Andre som ser på dette må gjerne legge til flere instillinger og slikt,       #
# Bare ikke overkjør ting som allerede er definert.                             #
#################################################################################


##        [Scraper]
# Hvor sikker i prosent må vi være på at et språk er det det utgir seg for å være før vi akspeterer svaret, fra 0.0 til 1.0, hvor 1.0 er 100% sikker
language_identification_threshold = 0.40

# Dersom vi ikke vet hva språk vi har, hvilken streng skal vi bruke til å identifisere med?
uncertain_language_string = "NA"



##        [Database]
# Ting som vi må vite om databasen vi skal snakke til. 
rdbms_hostname = "localhost"
rdbms_username = "scraper"
rdbms_password = "reparcs"

# Planen er å legge ut SQL-kommandoene i seperate filer vi kan deretter lese fra og redigere uten å måtte tenke på Python
