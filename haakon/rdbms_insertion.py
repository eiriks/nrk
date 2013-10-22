# coding: utf-8

import MySQLdb as mdb
import tldextract
import logging
import sys
from time import mktime
from datetime import datetime
from settings import rdbms_hostname, rdbms_username, rdbms_password

## RDBMS dependent code
def add_to_db(dict):
    # create logger with 'tldextract'
    logger = logging.getLogger('tldextract')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('spam.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    with open('insertion.sql', 'r') as f:
        insertion = f.read()
    with open('insertion_link.sql', 'r') as f:
        insertion_link = f.read()
    with open('insertion_author.sql', 'r') as f:
        insertion_author = f.read()
    with open('insertion_factbox.sql', 'r') as f:
        insertion_factbox = f.read()

    # connect    
    try:
        # Set up a database cursor:
        # Added charset='utf8' to default to utf8 for text to/from db
        connection = mdb.connect(host=rdbms_hostname, user=rdbms_username, passwd=rdbms_password, db="nrk", charset='utf8')
        #connection = mdb.connect(unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock", user=rdbms_username, passwd=rdbms_password, db="nrk", charset='utf8')
        cur = connection.cursor()
        cur.execute("USE nrk;")
        logger.info("koblet til databasen")
    except:
        logger.error("kunne ikke logge på databasen")



    try:
        # Vi må være forsiktige med forfattere, siden ikke NRK alltid klarer å huske på dem.
        # Se td. http://www.nrk.no/livsstil/test-av-norges-mest-solgte-brod-1.8352163, med tre forfattere.
        for author in dict['authors']:
            authorName = author[0]
            if(authorName):
                authorName = authorName
            else:
                authorName = u"Ukjent"
                
            authorMail = author[1]
            if(authorMail):
                authorMail = authorMail
            else:
                authorMail = u"Ukjent"
                
            authorRole = author[2]
            if(authorRole):
                authorRole = authorRole
            else:
                authorRole = u"Ukjent" 
                
            cur.execute(insertion_author,
                        (dict['url_self_link'],
                         authorName,
                         authorMail,
                         authorRole))
                        
        for box in dict['factbox']:
            cur.execute(insertion_factbox,
                        (dict['url_self_link'],
                         len(box['links']),
                         box['wordcount'],
                         box['text'].encode('utf-8')))
                
                
        for link in dict['internal_links']:
            extr = tldextract.extract(link)
            cur.execute(insertion_link.encode('utf-8'),
                        (dict['url_self_link'].encode('utf-8'),
                         link.encode('utf-8'),
                         u"html",
                         extr[0].encode('utf-8'),
                         extr[1].encode('utf-8'),
                         extr[2].encode('utf-8'),
                         '1'.encode('utf-8')))
            
        for link in dict['external_links']:
            extr = tldextract.extract(link)
            cur.execute(insertion_link.encode('utf-8'),
                        (dict['url_self_link'].encode('utf-8'),
                        link.encode('utf-8'),
                        u"html",
                        extr[0].encode('utf-8'),
                        extr[1].encode('utf-8'),
                        extr[2].encode('utf-8'),
                        '0'.encode('utf-8')))

        published = dict['published']
        if(published != "NULL") :
               published = datetime.fromtimestamp(mktime(dict['published'])).strftime("%Y-%m-%d %H:%M:%S")
        updated = ""
        timestamp = dict['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        if dict['updated'] != "NO UPDATES":
            updated = (" ".join(elem for elem in dict['updated'])).replace('.', '-') + ":00"
        else:
            updated = published


        # print "*"*50
        # print type(dict['body']), dict['body']
        # print "*"*50

        cur.execute(insertion,
                    (dict['url'],
                     dict['url_self_link'],
                     dict['headline'], #.encode('utf-8'),
                     dict['body'], #.encode('utf-8'),
                     published,
                     updated,
                     timestamp,
                     dict['fb_like'],
                     dict['fb_share'],
                     dict['googleplus_share'],
                     dict['twitter_share'],
                     dict['others_share'],
                     dict['language'], #.encode('utf-8'),
                     dict['lesbahet'],
                     "NA", # Får ikke fatt på nyhetsbyrå enda.
                     len(dict['external_links']),
                     len(dict['internal_links']),
                     dict['word_count'],
                     dict['line_count'],
                     dict['char_count'],
                     len(dict['factbox']),
                     dict['comment_fields'],
                     dict['comment_number'],
                     dict['interactive_elements'], #"interactive_elements IS NOT DONE",
                     dict['poll'], #"NOT DONE",
                     dict['game'], #"NOT DONE",
                     dict['video_files'],
                     dict['video_files_nrk'],
                     dict['flash_file'],
                     dict['image_collection'],
                     dict['images'],
                     dict['image_captions'],# .encode('utf-8'),
                     dict['related_stories'],
                     dict['related_stories_box_thematic'], #"related_stories_box_thematic IS NOT DONE",
                     dict['related_stories_box_les'],           #"related_stories_box_les IS NOT DONE",
                     dict['map'],  # map IS NOT DONE
                     dict['publiseringssted'],
                     dict['programtilknytning'],
                     dict['hovedkategori'],
                     dict['iframe']))

        connection.commit()
        return

    except mdb.Error, e:
        connection.rollback()
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)      

        
    finally:
        if connection:
            connection.close()
        
