# coding: utf-8

from sqlite3 import connect
from os import environ
from time import strftime, strptime

class Store():

    def __init__(self):
        self._store = environ['HOME']+'/nrk/page.sqlite'

    def _datetime(self, date_time):
        if not date_time:
            # In case date_time is None we just return None back.
            return
        date, time = date_time
        # change to sqlite3 datetime format
        date = strftime('%Y-%m-%d', strptime(date, '%d.%m.%Y'))

        return date + ' ' + time

    _page_insert_stmt = """
        INSERT INTO page (url, title, published, updated, external_links,
                          internal_links, images, word_count, factbox,
                          news_agency, videos, comment_fields)
               VALUES
                         (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

    def _insert_page(self, url, title, published, updated,
                     external_links, internal_links, images,
                     word_count, factbox, news_agency, videos,
                     comment_fields):
        self._cursor.execute(self._page_insert_stmt,
                             (url,
                              title,
                              self._datetime(published),
                              self._datetime(updated),
                              external_links,
                              internal_links,
                              images,
                              word_count,
                              factbox,
                              news_agency,
                              videos,
                              comment_fields))

    _author_insert_stmt = """
        INSERT INTO author (name, email, role)
               VALUES
                           (?   , ?    , ?   )
        """

    def _insert_author(self, author):
        self._cursor.execute(self._author_insert_stmt,
                             (author.name, author.email, author.role))

    _author_page_insert_stm = """
        INSERT INTO author_page (author, page) VALUES (?, ?)
        """

    def _insert_author_page(self, author_id, page_id):
        pass

    def store(self, analyser):
        conn = connect(self._store)
        self._cursor = conn.cursor()
        self.analyser = analyser

        self._insert_page(self.analyser.url(),
                          self.analyser.title(),
                          self.analyser.published(),
                          self.analyser.updated(),
                          self.analyser.external_links(),
                          self.analyser.internal_links(),
                          self.analyser.images(),
                          self.analyser.word_count(),
                          self.analyser.factbox(),
                          self.analyser.news_agency(),
                          self.analyser.videos(),
                          self.analyser.comment_field())

        for author in self.analyser.authors():
            self._insert_author(author)
        conn.commit()
        conn.close()
