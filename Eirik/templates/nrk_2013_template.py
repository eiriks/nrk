# coding: utf-8
import langid
import re
from time import strptime
from itertools import izip
from Lix import Lix
from datetime import datetime
from fetch_disqus_comments import num_comments
from functions import * #count_links, count_js, count_css, count_iframes, get_video, get_flash, count_map, has_data_id, has_data_relation_limit
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
    dictionary['fb_like']          = None #len(soup.select(".pluginButtonLabel"))
    dictionary['others_share']     = None
    dictionary['fb_share']         = len(soup.select(".share-facebook"))
    dictionary['googleplus_share'] = len(soup.select(".share-googleplus"))
    dictionary['twitter_share']    = len(soup.select(".share-twitter"))
    dictionary['email_share']      = len(soup.select(".share-mail"))
    

    # "les også" føljetong (sidebar) om om dette presise
    # dette må gjøres før vi fjerner js (ser det ut til..)
    # den første her ligger alltid inni .articlewrapper 
    dictionary['related_stories_box_les'] = len(soup.select("aside.articlewidgets article"))     #-9999 

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
    # remove javascript. it is spread through the site like spots on a Dalmatian
    # I believe this is what creates the somewhat awkward line-breaks in the soup
    [s.decompose() for s in soup.body.article('script')]

    # Find author(s)
    byline = soup.find('div', 'byline')
    authors = []
    try:
        for address in byline.find_all('address'):

            authorName = address.find('a', 'fn').text # alternatively .find('a', 'email') #address.a.text 
            authorMail = None # midlertidig gitt opp

            # not all have a span role
            if (address.find('span', 'role')):
                authorRole = address.find('span', 'role').text #address.span.text
            else:
                authorRole = None

            author = [authorName, authorMail, authorRole]
            authors.append(author)
            # address does not always come with figure, if it does, decompose
            # check http://www.nrk.no/ho/nekter-for-at-hun-var-med-pa-ran-1.11415954
            if (address.figure):
                address.figure.decompose() # remove tag cos it contains imgs we do not want to count later.
    except:
        new_logger.info("Ingen forfatter, oppgir ukjent, url: %s", dictionary['url'])
        authors.append([None, None, None]) # this is not very slick..

    dictionary['authors'] = authors
    #print dictionary['authors']


    # # dette failer
    # try:
    #     for address, li in izip(byline.find_all('address'), byline.find_all('li', 'icon-email')):
    #         authorName = address.strong.text #address.find(class_='fn').string.encode('utf-8')
    #         # NRK is still trying to hide the email address from spammers. #href = li.a['href']
    #         authorMail = None # 'abandon this? too hard?'#unquote(href[21:-1])[7:] # Antakelsen er at epost vil holde seg til ASCII. 
    #         authorRole = address.span.text #address.find(class_='role').string.strip().encode('utf-8')
    #         author = [authorName, authorMail, authorRole]
    #         authors.append(author)

    #         # and remove author image (so not to count it later..) 
    #         address.figure.decompose()
    # except AttributeError:
    #     # Finner ingen forfatter(e)
    #     new_logger.error("fant ingen forfatter, oppgir ukjent, url: %s", dictionary['url'])
    #     #print "[ERROR]: Kunne ikke finne forfattere for artikkel \"{0}\". Oppgir \"<UKJENT>\" som forfatter".format(dictionary['url'])
    #     authors.append([None, None, None])
    # dictionary['authors'] = authors
    
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



    # Find full text 
    # article MINUS stuff..
    try:
        # remove the related section
        soup.body.article.find('section', 'lp_related').decompose()
    except:
        pass
    # remove div.published (the top-bar)
    soup.body.article.find('div', 'published').decompose()
    # remove div.shareurl (the sharebar)
    soup.body.article.find('div', 'sharing').decompose()
    # store body text
    dictionary['body'] = soup.body.article.text.strip() 

    # Debugg fact-boxes:
    # print dictionary['url']    
    # print dictionary['body']
    # if soup.find_all("section", class_="facts"):
    #     print "*" *70
    #     import sys
    #     sys.exit(0)

    # .stripped_strings option?     # soup.get_text("|", strip=True) perhaps?

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

    # Find fact-boxes :
    # Should be included in both word-count, LIX, image-count, video-count, etc.
    faktabokser = []
    #for boks in soup.find_all("section", class_="articlewidget cf facts lp_faktaboks"):
    for boks in soup.find_all("section", class_="facts"):
        text = boks.text.strip()
        lix = Lix(text)
        analysis = lix.analyzeText(text)
        faktabokser.append({"text":text, "links":boks.find_all("a"), "wordcount":analysis['wordCount']})
        # and remove from soup
        # boks.decompose() # fact-boxes should be includes, so not removed.
        # NB, this also removes pictures if any in the fact-box
    dictionary['factbox'] = faktabokser










    # look through the last part of the body text to find news bureau
    # add more in settings.py
    dictionary['news_bureau'] = matches_pattern(dictionary['body'].strip()[-200:], syndicators)


    # Find language. Defaults can be tampered with in settings.py
    (language, certainty) = langid.classify(soup.body.article.text)
    language_code = uncertain_language_string
    if (certainty > language_identification_threshold):
        language_code = language

    dictionary['language'] = language_code

    # video
    # sets  dictionary['video_files'], dictionary['video_files_nrk'] 
    # only send the stuff in article-tag as soup
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
        dictionary['comment_number'] = None #-9999#num_comments(dictionary)
    
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
    img_from_header = count_images(soup.body.article.header, data, dictionary)
    img_from_article_text = count_images(soup.select(".articlebody")[0], data, dictionary)
    dictionary['images'] = img_from_header+img_from_article_text # -9999# len(re.findall("<img src=\"http:", data))

    #print "images: %s og %s og tilsammen: %s" % (img_from_header,img_from_article_text, img_from_header+img_from_article_text) 


    # på videoer gjør vi slik: soup.select('figure.video') Kanskje det er noe også her, (tror dette loades via js)

    # bildesamlinger
    dictionary['image_collection'] = len(soup.select(".slideshow")) # er dette nok?

    # Som diskutert med Eirik, dette henter ut bildetekstene og deler dem med pipe symboler.
    imgtagger = re.findall(u"<img src=\"http.*\n.*", data)
    bildetekst = ""
    for imgtag in imgtagger:
        funn = re.findall("alt=\".*\"", imgtag)
        if len(funn) > 0:
            bildetekst += ((funn[0])[5:-1] + " | ")
    bildetekst = bildetekst[:-3] # Fjerner siste pipen
    dictionary['image_captions'] = bildetekst

    
    # !!! trenger flere eksempler på dette
    dictionary['map'] = count_map(soup.body.article, data, dictionary)
    dictionary['poll'] = None #-9999
    dictionary['game'] = None #-9999





    # sum interactive     
    # dictionary['interactive_elements'] = dictionary['comment_fields'] + dictionary['image_collection'] + \
    #                                         dictionary['video_files'] + dictionary['video_files_nrk'] + \
    #                                         dictionary['fb_like'] + dictionary['fb_share'] + \
    #                                         dictionary['googleplus_share'] + dictionary['twitter_share'] + \
    #                                         dictionary['others_share'] + dictionary['email_share'] + \
    #                                         dictionary['map'] + dictionary['poll'] + dictionary['game']

    dictionary['interactive_elements'] = count_interactive( \
                                            dictionary['comment_fields'] , dictionary['image_collection'] , \
                                            dictionary['video_files'] , dictionary['video_files_nrk'] , \
                                            dictionary['fb_like'] , dictionary['fb_share'] , \
                                            dictionary['googleplus_share'] , dictionary['twitter_share'] , \
                                            dictionary['others_share'] , dictionary['email_share'] , \
                                            dictionary['map'] , dictionary['poll'] , dictionary['game'])


    return dictionary
