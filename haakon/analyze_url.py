# coding: utf-8
import re # Regexp matcher

## Analyserer en URL (fra et oppslagsverk) og legger til dataene inn i oppslagsverket vårt.
def analyze_url(dictionary):
    url = dictionary['url']
    
    #Steg 1: Hvor i landet er dette fra?
    if re.match(".+/norge/.+", url):
        dictionary["publiseringssted"] = u"NRK Norge"
    elif re.match(".+/ho/.+", url):
        dictionary["publiseringssted"] = u"NRK Hedmark og Oppland"
    elif re.match(".+/hordaland/.+", url):
        dictionary["publiseringssted"] = u"NRK Hordaland"
    elif re.match(".+/mr/.+", url):
        dictionary["publiseringssted"] = u"NRK Møre og Romsdal"
    elif re.match(".+/nordland/.+", url):
        dictionary["publiseringssted"] = u"NRK Nordland"
    elif re.match(".+/rogaland/.+", url):
        dictionary["publiseringssted"] = u"NRK Rogaland"
    elif re.match(".+/sognogfjordane/.+", url):
        dictionary["publiseringssted"] = u"NRK Sogn og Fjordane"
    elif re.match(".+/sorlandet/.+", url):
        dictionary["publiseringssted"] = u"NRK Sørlandet"
    elif re.match(".+/nordnytt/.+", url):
        dictionary["publiseringssted"] = u"NRK Troms og Finnmark"
    elif re.match(".+/trondelag/.+", url):
        dictionary["publiseringssted"] = u"NRK Trøndelag"
    elif re.match(".+/ostafjells/.+", url):
        dictionary["publiseringssted"] = u"NRK Østafjells"
    elif re.match(".+/ostfold/.+", url):
        dictionary["publiseringssted"] = u"NRK Østfold"
    elif re.match(".+/ostlandssendingen/.+", url):
        dictionary["publiseringssted"] = u"NRK Østlandssendingen"
    elif re.match(".+/sapmi/.+", url):
        dictionary["publiseringssted"] = u"NRK Sápmi"
    else:
        dictionary["publiseringssted"] = u"NA"
# re.match('.+/sapmi/.+', url) returnerer et objekt
## Abere til listen.
#1.  Puls –– Har ikke egne sider lengre, nå sløyfet. ––
#34. nrk.no/livsstil puls + andre?
# Forbrukerinspektørene FBI går nå under livsstil, og har ikke eget design. Må testes i egne sider. Jej.
    #Steg 2: Hører dette til noe program hos NRK?
#### VIKTIG! OMMØBLER DISSE, SLIK AT MEST SPESIFIKK ER FØRST! ####        
    if re.match(".+/juntafil/.+", url):
        dictionary['programtilknytning'] = u"Juntafil"
    elif re.match(".+/norgesglasset/.+", url): # NB: Legges snart ned!
        dictionary['programtilknytning'] = u"Norgesglasset"
    elif re.match(".+/migrapolis/.+", url):
        dictionary['programtilknytning'] = u"Migrapolis"
    elif re.match(".+/radiodokumentaren/.+", url):
        dictionary['programtilknytning'] = u"Radiodokumentaren"
    elif re.match(".+/schrodingers_katt/.+", url):
        dictionary['programtilknytning'] = u"Schrödingers katt"
    elif re.match(".+/studio_sokrates/.+", url):
        dictionary['programtilknytning'] = u"Studio Sokrates"
    elif re.match(".+/p2_akademiet/.+", url):
        dictionary['programtilknytning'] = u"P2 Akademiet"
    elif re.match(".+/newton/.+", url): # newton ser ut til å ligge på NRK Super
        dictionary['programtilknytning'] = u"Newton"
    elif re.match(".+/kurer/.+", url):
        dictionary['programtilknytning'] = u"Kurer"
    elif re.match(".+/kunstreisen/.+", url):
        dictionary['programtilknytning'] = u"Kunstreisen"
    elif re.match(".+/nitimen/.+", url): # NB: Legges snart ned!
        dictionary['programtilknytning'] = u"Nitimen"
    elif re.match(".+/p3.no/filmpolitiet/.+", url):
        dictionary['programtilknytning'] = u"Filmpolitiet" # Spiller.no er flyttet over til filmpolitiet.
    elif re.match(".+/p3.no/.+", url):
        dictionary['programtilknytning'] = u"P3.no (flere programmer)"
    elif re.match(".+/yr.no/nyheter/.+", url):
        dictionary['programtilknytning'] = u"Yr.no (Nyheter)"
    elif re.match(".+/lydverket/.+", url):
        dictionary['programtilknytning'] = u"Lydverket"
    elif re.match(".+/valg2013/.+", url):
        dictionary['programtilknytning'] = u"Valg"
    elif re.match(".+/nrksuper.no/super/.+", url): # NRK Super, men ikke tv-siden
        dictionary['programtilknytning'] = u"NRK Super"
    elif re.match(".+/tv.nrksuper.no/.+", url): # Strømmingen
        dictionary['programtilknytning'] = u"BarneTV strømming"
    elif re.match(".+/viten/.+", url):
        dictionary['programtilknytning'] = u"Viten og teknologi"
    elif re.match(".+/fordypning/.+", url):
        dictionary['programtilknytning'] = u"Fordypning"
    elif re.match(".+/sport/fotball/.+", url):
        dictionary['programtilknytning'] = u"Fotball"
    elif re.match(".+/mgp/.+", url):
        dictionary['programtilknytning'] = u"Melodi Grand Prix"
    elif re.match(".+/sapmi/.+", url):
        dictionary['programtilknytning'] = u"Sapmi"
    elif re.match(".+/ytring/.+", url):
        dictionary['programtilknytning'] = u"Ytring"
    elif re.match(".+/yr.no/.+", url):
        dictionary['programtilknytning'] = u"Yr.no"
    elif re.match(".+/ut.no/.+", url):
        dictionary['programtilknytning'] = u"Ut.no"
    elif re.match(".+/dit.no/.+", url):
        dictionary['programtilknytning'] = u"Dit.no"
    elif re.match(".+/nrkbeta.no/[0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9]/.+", url):  # Antagelsen her er at det er nyheter fra beta.nrk.no
        dictionary['programtilknytning'] = u"Nyheter Beta" # Dvs. innlegg fra NRK Beta.
    elif re.match(".+/nrk.no/nyheter/klima/.+", url):
        dictionary['programtilknytning'] = u"Klima"
    elif re.match(".+/nrk.no/kultur/.+", url):
        dictionary['programtilknytning'] = u"Kultur"
    else:
        dictionary['programtilknytning'] = u"NA"

    #Steg 3: Hører denne artikkelen til noe nyhetskategori hos NRK?
    # Forsiden Er ikke mulig å hente ut fra URL.
    # Siste nytt Er ikke mulig å hente ut fra URL.
    if re.match(".+/norge/.+", url):
        dictionary['hovedkategori'] = u"Norge"
    elif re.match(".+/verden/.+", url):
        dictionary['hovedkategori'] = u"Verden"
    elif re.match(".+/okonomi/.+", url):
        dictionary['hovedkategori'] = u"Økonomi"
    elif re.match(".+/sport/.+", url):
        dictionary['hovedkategori'] = u"Sport"
    elif re.match(".+/kultur/.+", url):
        dictionary['hovedkategori'] = u"Kultur og underholdning"
    elif re.match(".+/livsstil/.+", url):
        dictionary['hovedkategori'] = u"Helse og livsstil"
    elif re.match(".+/viten/.+", url):
        dictionary['hovedkategori'] = u"Teknologi og vitenskap"
    elif re.match(".+/yr.no/.+", url):
        dictionary['hovedkategori'] = u"Vær"
    elif re.match(".+/norge/.+", url):
        dictionary['hovedkategori'] = u"Norge"
    elif re.match(".+/verden/.+", url):
        dictionary['hovedkategori'] = u"Verden"
    elif re.match(".+/nobel/.+", url):
        dictionary['hovedkategori'] = u"Nobels fredspris"
    elif re.match(".+/klima/.+", url):
        dictionary['hovedkategori'] = u"Klima"
    elif re.match(".+/p2_akademiet/.+", url):
        dictionary['hovedkategori'] = u"P2 akademiet"
    elif re.match(".+/distrikt/.+", url):
        dictionary['hovedkategori'] = u"Distrikt"
    elif re.match(".+/valg09/.+", url):
        dictionary['hovedkategori'] = u"Valg 09"
    elif re.match(".+/valg2013/.+", url):
        dictionary['hovedkategori'] = u"Valg 2013"
    else:
        dictionary['hovedkategori'] = u"NA"
    return dictionary

