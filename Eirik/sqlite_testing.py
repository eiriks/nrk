 #!/usr/bin/env python
"""
SYNOPSIS
    TODO helloworld [-h,--help] [-v,--verbose] [--version]

DESCRIPTION
    TODO This describes how to use this script. This docstring
    will be printed by the script if there is an error or
    if the user requests help (-h or --help).

EXAMPLES

    TODO: Show some examples of how to use this script.

EXIT STATUS

    TODO: List exit codes

AUTHOR

    TODO: Eirik <eirik@stavelin.com>

LICENSE

    This script is in the public domain, free from copyrights or restrictions.

VERSION

    $Id$
"""

import sys, os, traceback, optparse
import time
#import re
#from pexpect import run, spawn
import sqlite3 as lite



def sqlstuff():
    #print lite.version 			#pysqlite version
    #print lite.sqlite_version 	#sqlite version
    con = None
    try:
        con = lite.connect('nrk2013.db')    
        cur = con.cursor()    
        sql = 'SELECT * FROM links LIMIT 10'
        cur.execute(sql) # 'SELECT SQLITE_VERSION()'
        
        rows = cur.fetchall()   #fetchone()
        for row in rows:
            print row[0], row[1], row[2] # 1 er url, 2 er tidspunkt for innsamling 
        

        # sjekk om url er scrapet i mysql db'n

        # hvis ikke, finn ut hvilken tamplate som er i bruk

        # scrape & lagre i mysql

        
    except lite.Error, e:
        
        print "Error %s:" % e.args[0]
        sys.exit(1)
        
    finally:
        
        if con:
            con.close()

# SELECT *, count(page) c FROM links GROUP BY page ORDER BY c DESC;


def main ():

    global options, args
    # TODO: Do something more interesting here...
    print 'Hello world!'
    sqlstuff()


if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), usage=globals()['__doc__'], version='$Id$')
        parser.add_option ('-v', '--verbose', action='store_true', default=False, help='verbose output')
        (options, args) = parser.parse_args()
        #if len(args) < 1:
        #    parser.error ('missing argument')
        if options.verbose: print time.asctime()
        main()
        if options.verbose: print time.asctime()
        if options.verbose: print 'TOTAL TIME IN MINUTES:',
        if options.verbose: print (time.time() - start_time) / 60.0
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)

