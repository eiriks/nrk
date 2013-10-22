# coding: utf-8
import langid
import re
from bs4 import BeautifulSoup
from time import strptime
from itertools import izip
from urllib2 import unquote
from Lix import Lix
from fetch_disqus_comments import num_comments
from settings import language_identification_threshold
from settings import uncertain_language_string
from tell_lenker import tell
## This function does the Right Thing™ when given a beautifulsoup object created over an nrk page with their new template
## This is mostly stolen from the old functions.
def nrk_2013_template(soup, data, dictionary):
    """Tar et BeautifulSoup objekt og returnerer et map av data
    Modifiserer dictionary argumentet du gir inn."""

    # Steg 1: Ting som alltid er sant:
    dictionary['fb_like']          = 1
    dictionary['fb_share']         = 1
    dictionary['googleplus_share'] = 1
    dictionary['twitter_share']    = 1
    dictionary['others_share']     = 0
    dictionary['email_share']      = 1
    dictionary['related_stories']  = 6

    # Steg 3: Finn forfatter(e)
    byline = soup.find('div', 'byline')
    authors = []
    
    # wrapper denne i en try/except midlertidig for å komme fram til tekst jeg kan kjøre LIX på. (Eirik)



    try:
        for address, li in izip(byline.find_all('address'), byline.find_all('li', 'icon-email')):
            authorName = address.strong.text #address.find(class_='fn').string.encode('utf-8')
            # NRK is still trying to hide the email address
            # from spammers.
            #href = li.a['href']
            authorMail = 'abandon this? too hard?'#unquote(href[21:-1])[7:] # Antakelsen er at epost vil holde seg til ASCII. 
            authorRole = address.span.text #address.find(class_='role').string.strip().encode('utf-8')
            author = [authorName, authorMail, authorRole]
            authors.append(author)
    except AttributeError:
        # og adder denne som en påminndelse om at vi må skrive dette noe mer robust for variasjoner (Eirik)
        # Men dette er måten templaten gjør det på. Dersom vi kommer hertil og forfatterene ikke er her, så har vi feilidentifisert templaten.
        # Hva fornuftig kan en gjøre dersom dokumentet er feilhåndtert, annet enn å krasje høylytt?
        # Det enkleste akkurat nå er å si eksplisitt i fra om at vi ikke finner noen forfatter, og setter inn en placeholder for nå.
        # Dersom dette ikke gjelder noen, så er saken grei, dersom det gjelder 10 er det mulig å hente ut informasjonen for hånd,
        # og dersom det gjelder mange, må noe gjøres om. Men dette er funksjonen fra i fjor, og den ser ut til å fungere fint.
        # Men gode ideer til å håndtere dette er selvsagt verdsatt. ^_^ (Haakon)
        print "[ERROR]: Kunne ikke finne forfattere for artikkel \"{0}\". Oppgir \"<UKJENT>\" som forfatter".format(dictionary['url'])
        authors.append(["Ukjent", "Ukjent", "Ukjent"])

    dictionary['authors'] = authors
    # Finn publiseringsdato
    try:
        dictionary['published'] = strptime(soup.time['datetime'][0:19], "%Y-%m-%dT%H:%M:%S")
    except TypeError:
        dictionary['published'] = "NULL"

    # Finn overskrift
    try:
        dictionary['headline'] = soup.header.find('div', 'articletitle').h1.text # .text gived unicode, .string gives 'bs4.element.NavigableString'
    except AttributeError:
        dictionary['headline'] = soup.title.text

    updateString = "NO UPDATES"
    updated = soup.find('div', 'published')
    if updated:
        updated = updated.find('span', 'update-date')

    if updated:
        updateString = updated['title']
        updateString = updateString[:10], updateString[16:21].replace('.', ':')
               
    dictionary['updated'] = updateString

    # Finn brødtekst
    body = "";
    for para in soup.find_all('p'):
        body += (para.text + "\n")
    body = body
    dictionary['body'] = body

    # Finn ut av antall tegn, linjer og ord, og kjør lesbarhetsindekstesten.
    lix = Lix(body) # .encode('utf-8')
    analyse = lix.analyzeText(body)
    try:
        dictionary['char_count'] = len(body)
        dictionary['word_count'] = analyse['wordCount']
        dictionary['line_count'] = analyse['sentenceCount']
        dictionary['lesbahet'] = lix.get_lix_score()
    except TypeError:
        print "[ERROR] Kunne ikke opprette analyse."
        print "[DEBUG] Body:"
        print body.encode('utf-8')
        print "[DEBUG] /Body"
        dictionary['line_count'] = -1
        dictionary['word_count'] = -1 
        dictionary['char_count'] = -1
        dictionary['lesbahet'] = -1.0

    # Finn ut av språket. Merk at du kan stille inn innstillinger i settings.py.ta
    (language, certainty) = langid.classify(body)
    language_code = uncertain_language_string
    if (certainty > language_identification_threshold):
        language_code = language

    dictionary['language'] = language_code

    # Finn ut av medieting de har. (Se lang kommentar)
    '''
    Så her er greien: Når vi laster ned via pythons requests, får vi ikke den "ferdige" nettsiden. Vi får rå html med javascript kall som evt. setter inn videoer.
    Da kan vi ikke bare løpe gjennom den vakre suppen vår, men må istedenfor finne ut av hva NRK kaller for å få ut en ny videofil.
    Heldigvis har NRK vært grusomt greie mot oss og ikke fjernet unødvendig whitespace fra javascriptkoden sin.
    Og siden de som koder for NRK er flinke, er det lett å lese hva som gjør hva.
    Da blir det enkelt å telle videoer og bilder.
    Artig nok blir share-button tingene deres også laget derifra. For de nye sidene er dette statisk, så vi trenger ikke ta noe hensyn til hva som gjør hva, og vi slipper dermed å gjøre noe: Vet vi at det er en ny side, vet vi også hva som kan deles og hvordan. ^_^
    Det store problemet jeg har er at Beautiful Soup ikke ser ut til å få med seg hele siden, alltid.
    Se eksempelet http://www.nrk.no/valg2013/se-partiledernes-foredrag-1.11168181, beautiful soup tar ikke med hele siden.

    – Haakon
    '''
    # Tell opp videoer:
    dictionary['video_files_nrk'] = len(re.findall('<div class="video-player">', data))
    dictionary['flash_file'] = len(re.findall('class="youtube-player"', data))
    dictionary['video_files'] = dictionary['flash_file'] + dictionary['video_files_nrk']

    # Tell opp iframe. BeautifulSoup teller feil på "http://www.nrk.no/mr/enorm-nedgang-i-antall-filmbutikker-1.11261850", så vi bruker en regex her istedenfor.
    # Hvis noen finner ut hvordan jeg bruker BS istedenfor, gi meg en lyd. (soup.find_all("iframe") hvirket ikke) – Haakon
    dictionary['iframe'] = len(re.findall("<iframe src=", data)) 
    
    # Finnes det en form for kommentarer her? I de nyere NRK sidene er det tydeligvis kun det på Ytring.
    # Men vi søker generelt nå, og håper på det beste. I verste fall vil et interessant krasj fortelle meg at dette ikke er tilfellet. –Haakon
    dictionary['comment_fields'] = 0
    dictionary['comment_number'] = 0
    if len(re.findall('<div id="disqus_thread"', data)) != 0:
        dictionary['comment_fields'] = 1
        dictionary['comment_number'] = num_comments(dictionary)
    
    # tar seg av lenker i siden
    tell(soup, data, dictionary)

    # url_self_link Vi jukser litt her. vi VET at input boksen den kommer fra ser SLIK ut:
    # <input value="[lenke]" readonly="readonly" type="text">
    # Dermed håper vi at det ikke er noen andre ting som ser like ut, og kjører på.
    # Dersom det ER andre ting som ser like ut er det ikke noe vi kan gjøre uansett.
    # Da får vi gi en feilmelding i alle fall.
    # – Haakon
    search = re.findall('<input type="text" value=".*" readonly="readonly"', data)
    if len(search) > 1:
        print "ERROR: MORE THAN ONE SELF-LINK"
    dictionary['url_self_link'] = (search[0])[26:-21]


    # antall bilder.
    # Beautiful Soup teller feil her og. Noe er galt.
    # Regex matching gir riktig resultat så vi får gå for det.
    dictionary['images'] = len(re.findall("<img src=\"http:", data))

    imgtagger = re.findall(u"<img src=\"http.*\n.*", data)

    # Som diskutert med Eirik, dette henter ut bildetekstene og deler dem med pipe symboler.
    # Måtte den som kommer etterpå ikke himle så altfor mye med øynene når de ser dette... :o
    bildetekst = ""
    for imgtag in imgtagger:
        funn = re.findall("alt=\".*\"", imgtag)
        if len(funn) > 0:
            bildetekst += ((funn[0])[5:-1] + " | ")
    bildetekst = bildetekst[:-3] # Fjerner siste pipen
    dictionary['image_captions'] = bildetekst

    # eventuelle faktabokser:
    faktabokser = []
    for boks in soup.find_all("section", class_="articlewidget cf facts lp_faktaboks"):
        text = boks.text
        lix = Lix(text)
        analysis = lix.analyzeText(text)
        faktabokser.append({"text":text, "links":boks.find_all("a"), "wordcount":analysis['wordCount']})
        
    dictionary['factbox'] = faktabokser


    # Dette er de data jeg ikke har fått til enda.
    # Dersom noen kan peke meg i retning av noen eksempler på sider med slike data på seg, blir jeg kjempeglad.
    # Jeg har sittet i flere timer på let, så jeg er litt frustrert over disse... ^_^
    dictionary['map'] = -1
    dictionary['image_collection'] = -1
    dictionary['poll'] = -1
    dictionary['game'] = -1
    
    # Jeg trenger litt hjelp til å finne gode eksempler på disse.
    # Send meg gjerne lenker!
    dictionary['interactive_elements'] = dictionary['iframe']
    

    # Disse rakk jeg rett og slett ikke å bli ferdig med.
    # Beklager! ;_;
    dictionary['related_stories_box_les']      = -1
    dictionary['related_stories_box_thematic'] = -1

    return dictionary
