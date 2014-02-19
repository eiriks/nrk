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


too_high_lix = """Omtrent 13 000 soldater deltar i øvelsen fra 11.-21. februar med deltakere fra syv land: Thailand, USA, Singapore, Indonesia, Japan Sør-Korea og Malaysia deltar i Cobra Gold 2013, som er en multinasjonal militærøvelse.

Cobra Gold fokuserer på å vedlikeholde og forbedre forhold mellom militæret i nasjoner som har felles mål og forpliktelser når det gjelder sikkerhet i Asia-/Stillehavsregionen.

Multinasjonal øvelse
Det er en årlig øvelse som foregår rundt om i hele Thailand. Soldatene som deltar får være med på alt fra kamptrening til katastrofehjelp under øvelsen som avsluttes 21. februar.

Vil oppnå fred og stabilitet
Under åpningsseremonien sa admiral Samuel Locklear, sjef i styret for den amerikanske Stillehavskysten, at den årlige øvelsen viser et engasjement fra de deltakende nasjonene for å oppnå fred og stabilitet i regionen.

Slik som hvert år, omfatter øvelsene i år krigføring i jungelen, sivil evakuering og tiltak mot kjemiske, biologiske og kjernefysiske angrep. Soldatene lærer også hvordan de skal bidra i humanitære og kommunale bistandsprosjekter.

20 nasjoner observerer for første gang
I år føyer Myanmar seg i rekken av 20 nasjoner som observerer øvelsene for første gang. USA sendte ut invitasjonen til landet som et incentiv for å få president Thein Stein og hans regjering til å fortsette med reformene som allerede pågår.

Cobra Gold startet i 1982 som en tosidig militærøvelse mellom USA og og Thailand. I 2000 ble det imildertid utvidet da Singapore også ble invitert til å delta."""

lix2 = Lix(too_high_lix) 			# oppretter instans
print "Lix på too_high_lix: %s" % lix2.get_lix_score()



# NB: her kan du også få ordtellin og setningstelling, hvis ønskelig.
# se 
import pprint
pp = pprint.PrettyPrinter()
pp.pprint(lix.analyzeText(test_text)) # det er kanskje unødvendig at denne funksjonen også ta råteksten som input, men putt pytt




# målform kan jo også testes på denne dataen..
print "*"*50
import langid
print "denne teksten har språk (burde være norsk bokmål):"
print langid.classify(test_text)

# hva med en nynorsk tekst?

test_text2 = u"""Eit steg med den eine foten like utfor stien, og brått begynte Dagny å søkke ned i gjørma. – Jo meir ho kjempa, jo raskare sank ho ned, fortel mora.
ELI FOSSDAL VAAGE
eli.fossdal.vaage@nrk.no
Publisert 02.10.2013 17:41.
Lagre i mine favoritter
– Eg hadde akkurat komme av eit fly på Gardermoen, då eg fekk ein telefon frå mannen min, fortel Inger Roll-Matthiesen, mor til den uheldige elleveåringen.
– Han sa: Berre så du veit det, så står Dagny fast i ei myr på Hardangervidda og ventar på å bli redda! 
Då mora fekk beskjeden, var fleire redningshelikopter alt på veg, og elleveåringen sjølv hadde fortalt til faren at ho ikkje lenger sank lenger ned.
– Så no er det jo nestein ein solskinshistorie, smiler Roll-Matthiesen, som er imponert over kor fort hjelpa kom på plass.
Sank berre lenger ned
Ifølgje Roll-Matthiesen gjekk dottera berre bortover stien og prata, då ho trådde utfor med den eine foten. Der sette beinet seg fast i eit hol. Men då jenta skulle dra foten til seg, gjekk det ikkje.
– Ho sat bom fast. Og jo meir ho kjempa i mot, jo lenger ned sank ho.
Politiet opplyser til NRK.no at dei fekk beskjed om den noko uvanlege hendinga klokka 15. Berre ein time seinare hadde mannskap frå det eine redningshelikopteret lukkast med å grave Dagny laus.
Var ikkje redd
To helikopter, eit frå Bergen og eit frå Ål, var alt på veg til Dagny og turfølgjet då mor Inger fekk vite om kva som stod på. Ho fortel at dottera tok det heile nokså roleg.
– Ho sa til meg like etter at ho kom laus: Eg var ikkje redd, mamma! Og eg græt ikkje.
– Ho sa at dei hadde nok av klede, og selskap var der jo, så alt i alt var dei rolege og berre glade for at hjelpa var så raskt ute, avsluttar Roll-Matthiesen."""

print "og en tekst vi vet er nynorsk:"
print langid.classify(test_text2)


# så var det de urlene da.
# her burde vi kunne kjøre gjennom url for url
with open('test_urls.txt') as f:
    content = f.readlines()
    for url in content[0:5]: # kun de fem første for nå...
        print url,
        #print soup_from_live_url(url)

