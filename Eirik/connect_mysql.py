# coding: utf-8

#import MySQLdb as mdb # moved to Oracle bindings: dev.mysql.com/downloads/connector/python/
import mysql.connector
import logging
import sys
from settings import rdbms_hostname, rdbms_username, rdbms_password


connect_logger = logging.getLogger('nrk2013.rdbms_connect')

def connect():
    try:
        # Set up a database cursor:
        # Added charset='utf8' to default to utf8 for text to/from db
        #connection = mdb.connect(host=rdbms_hostname, user=rdbms_username, passwd=rdbms_password, db="nrk", charset='utf8')
        #connection = mdb.connect(unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock", user=rdbms_username, passwd=rdbms_password, db="nrk", charset='utf8')
        connection = mysql.connector.connect(unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock",user=rdbms_username, passwd=rdbms_password, db="nrk", charset='utf8')
        cur = connection.cursor()
        cur.execute("USE nrk;")
        connect_logger.info("koblet til MySQL")
        return connection, cur
    except:
        connect_logger.error("kunne ikke logge på databasen")


def disconnect(connection):
    if connection:
        connection.close()
        connect_logger.info("koblet av mysql")
        
