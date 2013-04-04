from analyser import Analyser, Author
from tldextract import extract
from itertools import izip
from urllib2 import unquote
from re import split

class  NewPageAnalyser(Analyser):

    def __init__(self, url=None):
        super(NewPageAnalyser, self).__init__(url)
        self.article = self.soup.find('article')
        self._published = None
        self._external = 0
        self._internal = 0

    def url(self):
        return self._url

    def title(self):
        return self.article.header.find('div', 'articletitle').h1.string

    def published(self):
        published = self.soup.find('div', 'published').find('span', 'publish-date')['title']
        return published[:10], published[16:21].replace('.', ':')

    def updated(self):
        updated = self.soup.find('div', 'published').find('span', 'update-date')
        if updated:
            updated = updated['title']
            return updated[:10], updated[16:21].replace('.', ':')
        return

    def authors(self):
        byline = self.soup.find('div', 'byline')
        # for some reason the mail is not connected to the
        # name, but we can fix that.
        authors = []
        for address, li in izip(byline.find_all('address'),
                                byline.find_all('li', 'icon-email')):
            author = Author()
            author.name = address.find(class_='fn').string
            # NRK is still trying to hide the email address
            # from spammers.
            href = li.a['href']
            author.mail = unquote(href[21:-1])[7:]
            author.role = address.find(class_='role').string.strip()

            authors.append(author)

        return authors

    def _links(self):
        header = self.article.header
        body = self.article.find(class_='articlebody')
        for link in header.find_all('a') + body.find_all('a'):
            domain = extract(link['href']).domain
            if domain == 'nrk':
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
        header = self.article.header
        body = self.article.find(class_='articlebody')
        imgs = header.find_all('img') + body.find_all('img')

        return len(imgs)


    def word_count(self):
        text = self.article.header.text
        text += self.article.find(class_='articlebody').text
        text = split(r'\s+', text.strip())
        return len(text)

    def factbox(self):
        fb = self.article.find(class_='fact')
        if fb:
            return len(split(r'\s+', fb))
        return

    def news_agency(self):
        em = self.soup.select("p > em")[0]
        return em.text.replace('(', '').replace(')', '') if em else None

    def videos(self):
        article = self.soup.find(class_='article')
        intro = self.soup.find(class_='intro-element-article')
        vids = article.find_all(class_='video-hud') + intro.find_all(class_='video-hud'))
        return len(vids)
