#!/usr/bin/python
# encoding: utf-8

# from ikke_ferdig import *

from Lix import Lix



# test 1
# url = "http://www.nrk.no/sport/proffboksing-skal-bli-lov-i-norge-1.11277618"
# dictionary = {"url":url, "timestamp":datetime.datetime.now()}
# dictionary = dispatch_on_template(soup_from_live_url(url), dictionary)
# lix = Lix(dictionary['body'])
# print lix.get_lix_score() # skulle ha returnert lix scoren

# dette burde funke, men koden er ikke ferdig nok enda

# jeg luker derfor vekk alt jeg kan

print "*" *50

# test 2
test_text = u"""Proffboksing skal bli lov i Norge
Den nye regjeringen er blitt enige om å oppheve forbudet mot proffboksing, men en annen lov vil fortsatt gjøre det vanskelig for Cecilia Brækhus å bokse i Norge.

Send epost
 Publisert i dag, for 30 minutter siden  Oppdatert i dag, for ett minutt siden
– Vi gleder oss over at de folkevalgte partiene har gjennomslagskraft og at de står for sakene de har oppført i partiprogrammet sitt, sier generalsekretær i Norges Bokseforbund, Erik Nilsen, til NRK.no.

Det var Frp-leder Siv Jensen som kunngjorde lovendringen på en pressekonferanse torsdag ettermiddag.

Hun beskriver den som del av en større «avbyråkratiseringsreform».

– Vi skal fjerne forbud, påbud og reguleringer som ikke er i samsvar med hvordan folk opplever at virkeligheten bør være. Vi skal forenkle og flytte beslutningene nærmere folk, sa Jensen.

– Like langt
NRK.no har tidligere skrevet at de borgerlige partiene ønsker å oppheve proffbokseforbudet.

Men selv om det gjennomføres, er det foreløpig ikke selvsagt at Cecilia Brækhus eller andre kan bokse i Norge uten hjelm.

Den såkalte «knockoutloven» har en rekke begrensninger for proffboksingen, men først og fremst sier den at boksere må bære hjelm.

Denne loven har hverken Høyre eller Idrettsforbundet planer om å avskaffe.

– I teorien er vi like langt. På grunn av knockoutloven vil ikke Cecilia Brækhus få bokse i Norge. Hun bokser nemlig 20-minutters kamper, knockoutloven tillater bare 12-minutters kamper. I tillegg sier knockoutloven at du må bokse med hjelm, og det gjør ikke Cecilia, forklarer Nilsen.

Kan søke om dispensasjon
Boksere kan imidlertid søke om dispensasjon fra knockoutloven, og dermed gir opphevingen av proffbokseforbudet en teoretisk mulighet for Brækhus til å bokse i Norge.

– Det hadde vært helt enormt. Det hadde vært en utrolig avslutning på en bra karriere. Men om det skjer i min tid, gjenstår å se. Det hadde vært norsk idrettshistorie, sa Brækhus til NRK.no i september.

Brækhus har bokset 23 proffkamper i løpet av karrieren - alle er vunnet og alle sammen er gjennomført utenfor Norges grenser.

Hennes tre siste kamper har foregått i Frederikshavn i Danmark.

NRK.no oppdaterer saken"""

lix = Lix(test_text) 			# oppretter instans
print lix.get_lix_score()		# printer LIX score

# NB: her kan du også få ordtellin og setningstelling, hvis ønskelig.
# se 
import pprint
pp = pprint.PrettyPrinter()
pp.pprint(lix.analyzeText(test_text)) # det er kanskje unødvendig at denne funksjonen også ta råteksten som input, men putt pytt
