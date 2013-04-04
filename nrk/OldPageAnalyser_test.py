# coding: utf-8

from unittest import TestCase, main
from OldPageAnalyser import OldPageAnalyser
from analyser import Author

class TestOldPageAnalyser(TestCase):

    def setUp(self):
        self.url = 'http://www.nrk.no/nyheter/distrikt/nordland/1.10973327'
        self.analyser = OldPageAnalyser(self.url)

    def test_url(self):
        self.assertEquals(self.url, self.analyser.url())

    def test_title(self):
        title = u'– Jeg så at det kom til å gå galt. Så hørte vi et kraftig dunk'
        self.assertEquals(title, self.analyser.title())

    def test_published(self):
        published = ('04.04.2013', '10:45')
        self.assertEquals(published, self.analyser.published())

    def test_updated(self):
        updated = ('04.04.2013', '11:56')
        self.assertEquals(updated, self.analyser.updated())

    def test_authors(self):
        author = Author()
        author.name = u'Susanne Lysvold'
        author.email = u'Susanne.Lysvold@nrk.no'
        author.role = None
        author2 = Author()
        author2.name = u'Emil Indsetviken'
        author2.email = None
        author2.role = None
        authors = self.analyser.authors()
        self.assertEquals(author, authors[0])
        self.assertEquals(author2, authors[1])

    def test_external_links(self):
        self.assertEquals(0, self.analyser.external_links())

    def test_internal_links(self):
        self.assertEquals(0, self.analyser.internal_links())

    def test_images(self):
        self.assertEquals(4, self.analyser.images())

    def test_word_count(self):
        self.assertEquals(490, self.analyser.word_count())

    def test_factbox(self):
        self.assertEquals(None, self.analyser.factbox())

if __name__ == '__main__':
    main()
