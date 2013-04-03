from bs4 import BeautifulSoup
from analyser import Analyser, Author
from re import match, search, sub
from tldextract import extract

class OldPageAnalyser(Analyser, Base):

    def __init__(self, url=None):
        super(OldPageAnalyser, self).__init__(url)
        self.url = url
        self._external = None
        self._internal = None

    def url(self):
        return self.url

    def title(self):
        return soup.find(class_='intro-element-article').h1.text

    def published(self):
        pub = self.soup.find('p', 'published').string
        return published[10:20], published[21:26]

    def updated(self):
        pub = self.soup.find('p', 'published').string
        if search(pub, 'Oppdatert'):
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
        _external = 0
        _internal = 0
        for link in article.find_all('a') + intro.find_all('a'):
            domain = extract(link['href']).domain
            if domain is 'nrk':
                _internal += 1
            else:
                _external += 1

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
        factbox - soup.find(class_='facts-right').text
        return len(split(r'\s+', factbox))

class NewPageAnalyser(Page, Base):
        def __init__(self, url=None):
        super(NewPageAnalyser, self).__init__(url)
        self.url = url
        self.article = soup.find('article')
        self._published = None
        self._external = 0
        self._internal = 0

    def url(self):
        return self.url

    def title(self):
        return self.article.header.find('div', 'articletitle').h1.string

    def published(self):
        published = soup.find('div', 'published').find('span', 'publish-date')['title']
        page.published['date'] = published[:10]
        page.published['time'] = published[15:21]

    def updated(self):
        updated = soup.find('div', 'published').find('span', 'update-date')
        if updated:
            updated = updated['title']
            page.updated['date'] = updated[:10]
            page.updated['time'] = updated[15:21]

    def authors(self):
        byline = soup.find('div', 'byline')
        # for some reason the mail is not connected to the
        # name, but we can fix that.
        authors = []
        for address, li in izip(byline.find_all('address'),
                                byline.find_all('li', 'icon-mail')):
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
        header = article.header
        body = article.find(class_='articlebody')
        for link in header.find_all('a') + body.find_all('a'):
            domain = extract(link['href']).domain
            if domain is 'nrk':
                self._internal += 1
            else:
                self._external += 1

    def external_links(self):
        if _external:
            return _external
        self._links()
        return _external

    def internal_links(self):
        if _internal:
            return _internal
        self._links()
        return _internal

    def images(self):
        header = article.header
        body = article.find(class_='articlebody')
        imgs = header.find_all('img') + body.find_all('img')

        return len(imgs)


    def word_count(self):
        text = article.header.text
        text += article.find(class_='articlebody').text
        text = split(r'\s+', text.strip())
        page.wc = len(text)

    def factbox(self):
        fb = article.find(class_='fact')
        return len(split(r'\s+', fb))
