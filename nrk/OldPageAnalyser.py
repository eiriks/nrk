from bs4 import BeautifulSoup
from analyser import Analyser, Author
from tldextract import extract
from urllib2 import unquote
from re import split, search

class OldPageAnalyser(Analyser):

    def __init__(self, url=None):
        super(OldPageAnalyser, self).__init__(url)
        self._external = None
        self._internal = None

    def url(self):
        return self._url

    def title(self):
        return self.soup.find(class_='intro-element-article').h1.text

    def published(self):
        published = self.soup.find('p', 'published').string
        return published[10:20], published[21:26]

    def updated(self):
        published = self.soup.find('p', 'published').string
        if search('Oppdatert', published):
            return published[38:48], published[49:54]
        else:
            return

    def authors(self):
        byline = self.soup.find('ul', 'byline')
        authors = []
        for address in byline.find_all('address'):
            author = Author()
            author.name = address.span.string
            # To find the mail we need to to do some unquoting
            # as nrk is trying to protect the mail address
            # from spammers behind a quoted string.
            if address.script:
                script = address.script.string
                m = search(".*?'(.*)'.*$", script)
                m = search(".*?'(.*)'.*$", unquote(m.group(1)))
                html = BeautifulSoup(m.group(1))
                author.email = html.a.string

            authors.append(author)

        return authors

    def _links(self):
        article = self.soup.find(class_='article')
        intro = self.soup.find(class_='intro-element-article')
        self._external = 0
        self._internal = 0
        for link in article.find_all('a') + intro.find_all('a'):
            domain = extract(link['href']).domain
            if domain is 'nrk':
                self._internal += 1
            else:
                self._external += 1

    def external_links(self):
        if self._external:
            return self._external
        self._links()
        return self._external

    def internal_links(self):
        if self._internal:
            return self._internal
        self._links()
        return self._internal

    def images(self):
        article = self.soup.find(class_='article')
        intro = self.soup.find(class_='intro-element-article')
        imgs = article.find_all('img') + intro.find_all('img')

        return len(imgs)


    def word_count(self):
        article = self.soup.find(class_='article').text
        intro = self.soup.find(class_='intro-element-article').text
        return len(split(r'\s+', article+intro))

    def factbox(self):
        factbox = self.soup.find(class_='facts-right')
        if factbox:
            return len(split(r'\s+', factbox))
        return
