# coding: utf-8

from unittest import TestCase, main
from NewPageAnalyser import NewPageAnalyser
from analyser import Author

class TestNewPageAnalyser(TestCase):

    def setUp(self):
        self.url = 'http://www.nrk.no/sport/fotball/real-madrid-knuste-galatasaray-1.10972794'
        self.analyser = NewPageAnalyser(self.url)

    def test_url(self):
        self.assertEquals(self.url, self.analyser.url())

    def test_title(self):
        title = u'Vondt Mourinho-gjensyn for Drogba – Real Madrid knuste Galatasaray'
        self.assertEquals(title, self.analyser.title())

    def test_published(self):
        published = ('03.04.2013', '22:36')
        self.assertEquals(published, self.analyser.published())

    def test_updated(self):
        updated = ('03.04.2013', '22:58')
        self.assertEquals(updated, self.analyser.updated())

    def test_authors(self):
        author = Author()
        author.name = u'Håkon Rysst Heilmann'
        author.mail = u'hakon.rysst.heilmann@nrk.no'
        author.role = u'Journalist'
        self.assertEquals(author, self.analyser.authors()[0])

    def test_external_links(self):
        self.assertEquals(0, self.analyser.external_links())

    def test_internal_links(self):
        self.assertEquals(4, self.analyser.internal_links())

    def test_images(self):
        self.assertEquals(3, self.analyser.images())

    def test_word_count(self):
        self.assertEquals(460, self.analyser.word_count())

    def test_factbox(self):
        self.assertEquals(None, self.analyser.factbox())

if __name__ == '__main__':
    main()
