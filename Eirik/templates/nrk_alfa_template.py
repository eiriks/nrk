# coding: utf-8
import langid
import re
from time import strptime
from itertools import izip
from Lix import Lix
from datetime import datetime
from fetch_disqus_comments import num_comments
from functions import *
from settings import *
import logging


new_logger = logging.getLogger('nrk2013.alfatemplate')
## This function does the Right Thing™ when given a beautifulsoup object created over an 
## nrk page with their new template
## This is mostly stolen from the old functions.
def get(soup, data, dictionary):
    """Tar et BeautifulSoup objekt og returnerer et map av data
    Modifiserer dictionary argumentet du gir inn."""

    # Steg 1: Ting som alltid er sant:
    dictionary['fb_like']          = None #0
    dictionary['others_share']     = None #0
    dictionary['fb_share']         = len(soup.select(".share-facebook"))
    dictionary['googleplus_share'] = len(soup.select(".share-googleplus"))
    dictionary['twitter_share']    = len(soup.select(".share-twitter"))
    dictionary['email_share']      = len(soup.select(".share-mail"))

    # tror ikke disse har noen aside...
    dictionary['related_stories_box_les']      = len(soup.select("aside.articlewidgets article"))

    # related thematic (found in footer part of page)
    dictionary['related_stories_box_thematic'] = 0
    # grab that footer part with data-relation-limit attr
    related_thematic = soup.find_all(has_data_relation_limit)
    # loop
    for el in related_thematic:
        #check divs
        for div in el.select("div"):
            if has_data_id(div):
                dictionary['related_stories_box_thematic'] +=1

    # re related stories is the combined previous two
    dictionary['related_stories']  = dictionary['related_stories_box_les'] + dictionary['related_stories_box_thematic']
    

    # antall js dokumenter
    dictionary['js'] = count_js(soup, data, dictionary) #  = len(re.findall("<iframe src=", data)) # .js
    # remove javascript.
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
        new_logger.warn("Ingen forfattere \"{0}\". Oppgir \"<UKJENT>\" som forfatter".format(dictionary['url']))
        #print 
        authors.append([None, None, None])
    dictionary['authors'] = authors
    
    # Find published datetime
    try:
        dictionary['published'] = strptime(soup.time['datetime'][0:19], "%Y-%m-%dT%H:%M:%S")
    except TypeError:
        new_logger.info("finner ikke publiseringsdato")
        dictionary['published'] = None

    new_logger.debug("published: %s", type(dictionary['published']))
    # Find update datetime
    try:
        updated = soup.find('span', 'update-date')
        dictionary['updated'] = datetime.strptime(updated.time['datetime'][0:19], "%Y-%m-%dT%H:%M:%S")
    except:
        new_logger.info("finner ikke oppdateringsdato")
        dictionary['updated'] = None

    # Find headline
    try:
        dictionary['headline'] = soup.body.article.find('h1').text.strip()
        #dictionary['headline'] = soup.header.find('div', 'articletitle').h1.text # .text gived unicode, .string gives 'bs4.element.NavigableString'
    except AttributeError:
        new_logger.debug( "NB: bruker doc-title..." )
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

    new_logger.debug("faktabokser: %s", len(dictionary['factbox']))

    # Find full text 
    # article MINUS .universes OR is it .lp_related ?
    # remove the related section
    # try:
    #     soup.body.article.find('section', 'lp_related').decompose()
    # except:
    #     pass
    # # remove div.published (the top-bar)
    # soup.body.article.find('div', 'published').decompose()
    # # remove div.shareurl (the sharebar)
    # soup.body.article.find('div', 'sharing').decompose()

    # Find self declared url # get this before decomposing the header this is found in..
    dictionary['url_self_link'] = soup.select("time > a")[0]['href']

    # remove header with sharing links and date
    soup.select(".bulletin-header")[0].decompose()
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
        new_logger.error("Kunne ikke kjøre lix", dictionary['body']) 
        dictionary['line_count'] = None
        dictionary['word_count'] = None
        dictionary['char_count'] = None
        dictionary['lesbahet'] = -1.0

    # look through the last part of the body text to find news bureau
    # add more in settings.py
    dictionary['news_bureau'] = matches_pattern(dictionary['body'].strip()[-200:], syndicators)


    # Find language. Defaults can be tampered with in settings.py
    (language, certainty) = langid.classify(soup.body.article.text)
    new_logger.debug( "(language, certainty) (%s, %s)" % (language, certainty))
    language_code = uncertain_language_string
    if (certainty > language_identification_threshold):
        language_code = language

    dictionary['language'] = language_code


    get_video(soup.body.article, data, dictionary)

    # flash (untested)
    dictionary['flash_file'] = get_flash(soup.body.article, data, dictionary)

    # Tell opp iframe. 
    dictionary['iframe'] = count_iframes(soup, data, dictionary)
    
    # Tell opp css (karakterer)
    dictionary['css'] = count_css(soup, data, dictionary)


    # Finnes det en form for kommentarer her? I de nyere NRK sidene er det tydeligvis kun det på Ytring.
    # Men vi søker generelt nå, og håper på det beste. I verste fall vil et interessant krasj fortelle meg at dette ikke er tilfellet. –Haakon
    dictionary['comment_fields'] = 0
    dictionary['comment_number'] = 0
    if len(re.findall('<div id="disqus_thread"', data)) != 0:
        dictionary['comment_fields'] = 1
        dictionary['comment_number'] = None # -9999#num_comments(dictionary)
    
    # tar seg av lenker i siden
    count_links(soup, data, dictionary)

    # antall bilder.
    # Beautiful Soup teller feil her og. Noe er galt.
    # Regex matching gir riktig resultat så vi får gå for det.
    #result = soup.article.find_all('figure', 'image')
    #print len(result)
    #new_logger.debug( "antall bilder: %s", len(re.findall("<img src=\"http:", data)) )
    
    dictionary['images'] = count_images(soup.body.article, data, dictionary)
    
    # bildesamlinger
    dictionary['image_collection'] = len(soup.select(".slideshow")) # er dette nok?
    # Som diskutert med Eirik, dette henter ut bildetekstene og deler dem med pipe symboler.

    imgtagger = re.findall(u"<img src=\"http.*\n.*", str(soup.body.article) )
    bildetekst = ""
    for imgtag in imgtagger:
        funn = re.findall("alt=\".*\"", imgtag)
        if len(funn) > 0:
            bildetekst += ((funn[0])[5:-1] + " | ")
    bildetekst = bildetekst[:-3] # Fjerner siste pipen
    dictionary['image_captions'] = bildetekst



    dictionary['map'] = count_map(soup.body.article, data, dictionary)
    dictionary['poll'] = None # -9999
    dictionary['game'] = None # -9999
    
    dictionary['interactive_elements'] = count_interactive( \
                                            dictionary['comment_fields'] , dictionary['image_collection'] , \
                                            dictionary['video_files'] , dictionary['video_files_nrk'] , \
                                            dictionary['fb_like'] , dictionary['fb_share'] , \
                                            dictionary['googleplus_share'] , dictionary['twitter_share'] , \
                                            dictionary['others_share'] , dictionary['email_share'] , \
                                            dictionary['map'] , dictionary['poll'] , dictionary['game'])
    




    return dictionary
