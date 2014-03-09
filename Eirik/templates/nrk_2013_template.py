# coding: utf-8
import langid
import re
from time import strptime
from itertools import izip
from Lix import Lix
from datetime import datetime
from fetch_disqus_comments import num_comments
from functions import count_links, count_js, count_css, count_iframes, get_video, get_flash, count_map
from settings import *
import logging


new_logger = logging.getLogger('nrk2013.nrk_2013_tamplate')
## This function does the Right Thing™ when given a beautifulsoup object created over an 
## nrk page with their new template
## This is mostly stolen from the old functions.
def get(soup, data, dictionary):
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


    # "les også" føljetong (sidebar) om om dette presise
    # dette må gjøres før vi fjerner js (ser det ut til..)
    relaterte = soup.select("aside.articlewidgets article") # a.autonomous ser ut til å gio riktig svar.. # article.brief
    dictionary['related_stories_box_les']      = len(relaterte)     #-9999 

    # "les mer" (i bunnen) om om generelt dette området.
    # pga ulike typer saker (f.eks. live video) er kanskje select("container .brief") en løsning her?
    dictionary['related_stories_box_thematic'] = -9999  

    # remove javascript.
    # hvorfor fjerner vi js? Er det noen god grunn til det?
    # if we want to measure amount of js or numbers of .js docs, do it here.
    # antall js dokumenter
    dictionary['js'] = count_js(soup, data, dictionary) #  = len(re.findall("<iframe src=", data)) # .js

    [s.decompose() for s in soup.body.article('script')]
    # I believe this is what creates the somewhat awkward line-breaks in the soup

    # Find author(s)
    byline = soup.find('div', 'byline')
    authors = []
    try:
        for address, li in izip(byline.find_all('address'), byline.find_all('li', 'icon-email')):
            authorName = address.strong.text #address.find(class_='fn').string.encode('utf-8')
            # NRK is still trying to hide the email address from spammers. #href = li.a['href']
            authorMail = None # 'abandon this? too hard?'#unquote(href[21:-1])[7:] # Antakelsen er at epost vil holde seg til ASCII. 
            authorRole = address.span.text #address.find(class_='role').string.strip().encode('utf-8')
            author = [authorName, authorMail, authorRole]
            authors.append(author)
            # and remove author image (so not to count it later..) 
            address.figure.decompose()
    except AttributeError:
        # Finner ingen forfatter(e)
        new_logger.error("fant ingen forfatter, oppgir ukjent")
        #print "[ERROR]: Kunne ikke finne forfattere for artikkel \"{0}\". Oppgir \"<UKJENT>\" som forfatter".format(dictionary['url'])
        authors.append([None, None, None])
    dictionary['authors'] = authors
    
    # Find published datetime
    try:
        dictionary['published'] = strptime(soup.time['datetime'][0:19], "%Y-%m-%dT%H:%M:%S")
    except TypeError:
        dictionary['published'] = None

    # Find update datetime
    try:
        updated = soup.find('span', 'update-date')
        dictionary['updated'] = datetime.strptime(updated.time['datetime'][0:19], "%Y-%m-%dT%H:%M:%S")
    except:
        dictionary['updated'] = None

    # Find headline
    try:
        dictionary['headline'] = soup.body.article.find('h1').text.strip()
        #dictionary['headline'] = soup.header.find('div', 'articletitle').h1.text # .text gived unicode, .string gives 'bs4.element.NavigableString'
    except AttributeError:
        new_logger.warn("NB: bruker doc-title...")
        dictionary['headline'] = soup.title.text

    # Find fact-boxes :
    # Should be removes from body, but includes in LIX. Right?
    faktabokser = []
    #for boks in soup.find_all("section", class_="articlewidget cf facts lp_faktaboks"):
    for boks in soup.find_all("section", class_="facts"):
        text = boks.text.strip()
        lix = Lix(text)
        analysis = lix.analyzeText(text)
        faktabokser.append({"text":text, "links":boks.find_all("a"), "wordcount":analysis['wordCount']})
        # and remove from soup
        boks.decompose()
        # NB, this also removes pictures if any in the fact-box
    dictionary['factbox'] = faktabokser


    # Find full text 
    # article MINUS .universes OR is it .lp_related ?
    # remove the related section
    try:
        soup.body.article.find('section', 'lp_related').decompose()
    except:
        pass
    # remove div.published (the top-bar)
    soup.body.article.find('div', 'published').decompose()
    # remove div.shareurl (the sharebar)
    soup.body.article.find('div', 'sharing').decompose()
    # store body text
    dictionary['body'] = soup.body.article.text.strip() 
    # .stripped_strings option?
    # soup.get_text("|", strip=True) perhaps?

    # Find char count, line count, word count and Lix
    lix = Lix(dictionary['body']) 
    analyse = lix.analyzeText(dictionary['body'])
    try:
        dictionary['char_count'] = len(dictionary['body'])
        dictionary['word_count'] = analyse['wordCount']
        dictionary['line_count'] = analyse['sentenceCount']
        dictionary['lesbahet'] = lix.get_lix_score()
    except TypeError:
        new_logger.error( "Kunne ikke kjøre lix", dictionary['body'] )
        dictionary['line_count'] = None
        dictionary['word_count'] = None
        dictionary['char_count'] = None
        dictionary['lesbahet'] = -1.0



    # look through the last part of the body text to find news bureau
    # add more in settings.py
    dictionary['news_bureau'] = matches_pattern(dictionary['body'].strip()[-200:], syndicators)


    # Find language. Defaults can be tampered with in settings.py
    (language, certainty) = langid.classify(soup.body.article.text)
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
    # only send the stuff in article-tag as soup
    # sets  dictionary['video_files'], dictionary['video_files_nrk'] 
    get_video(soup.body.article, data, dictionary)

    dictionary['flash_file'] = get_flash(soup.body.article, data, dictionary)

    # Tell opp iframe. 
    dictionary['iframe'] = count_iframes(soup, data, dictionary)
    
    # antall css dokumenter
    dictionary['css'] = count_css(soup, data, dictionary)



    # Finnes det en form for kommentarer her? I de nyere NRK sidene er det tydeligvis kun det på Ytring.
    # Men vi søker generelt nå, og håper på det beste. I verste fall vil et interessant krasj fortelle meg at dette ikke er tilfellet. –Haakon
    dictionary['comment_fields'] = 0
    dictionary['comment_number'] = 0
    if len(re.findall('<div id="disqus_thread"', data)) != 0:
        dictionary['comment_fields'] = 1
        dictionary['comment_number'] = num_comments(dictionary)
    
    # tar seg av lenker i siden
    count_links(soup, data, dictionary)

    # Find self declared url
    search = re.findall('<input type="text" value=".*" readonly="readonly"', data)
    if len(search) > 1:
        print "ERROR: MORE THAN ONE SELF-LINK"
    dictionary['url_self_link'] = (search[0])[26:-21]


    # antall bilder.
    # Beautiful Soup teller feil her og. Noe er galt.
    # Regex matching gir riktig resultat så vi får gå for det.
    #print len(re.findall("<img src=\"http:", data))
    
    # se nærmere på denne..
    #print soup.article.find_all('figure') # includes img of author...
    
    #result = soup.article.find_all('figure', 'image')
    #print len(result)
    dictionary['images'] = len(re.findall("<img src=\"http:", data))

    # på videoer gjør vi slik: soup.select('figure.video') Kanskje det er noe også her, (tror dette loades via js)

    # bildesamlinger
    dictionary['image_collection'] = len(soup.select(".slideshow")) # er dette nok?

    # Som diskutert med Eirik, dette henter ut bildetekstene og deler dem med pipe symboler.
    # Måtte den som kommer etterpå ikke himle så altfor mye med øynene når de ser dette... :o
    imgtagger = re.findall(u"<img src=\"http.*\n.*", data)
    bildetekst = ""
    for imgtag in imgtagger:
        funn = re.findall("alt=\".*\"", imgtag)
        if len(funn) > 0:
            bildetekst += ((funn[0])[5:-1] + " | ")
    bildetekst = bildetekst[:-3] # Fjerner siste pipen
    dictionary['image_captions'] = bildetekst


    # Dette er de data jeg ikke har fått til enda.
    # Dersom noen kan peke meg i retning av noen eksempler på sider med slike data på seg, blir jeg kjempeglad.
    # Jeg har sittet i flere timer på let, så jeg er litt frustrert over disse... ^_^
    
    # !!! trenger flere eksempler på dett
    dictionary['map'] = count_map(soup.body.article, data, dictionary)
    dictionary['poll'] = -9999
    dictionary['game'] = -9999


    # Jeg trenger litt hjelp til å finne gode eksempler på disse.
    # Send meg gjerne lenker!

    # comment, map, game, image_collection
    
    dictionary['interactive_elements'] = dictionary['comment_fields'] + dictionary['image_collection'] + \
                                            dictionary['video_files'] + dictionary['video_files_nrk'] + \
                                            dictionary['fb_like'] + dictionary['fb_share'] + \
                                            dictionary['googleplus_share'] + dictionary['twitter_share'] + \
                                            dictionary['others_share'] + dictionary['email_share'] + \
                                            dictionary['map'] + dictionary['poll'] + dictionary['game']






    return dictionary
