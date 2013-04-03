from abc import ABCMeta, abstractmethod
from urllib2 import build_opener, unquote
from bs4 import BeautifulSoup, Comment

class Author:
    def __init__(self):
        self.name = None
        self.email = None
        self.role = None

class Analyser(object):
    __metaclass__ = ABCMeta

    def headers = [('User-agent',
                    'UiB NRK Proj (Contact: Eirik.Stavelin@infomedia.uib.no)')]

    def __init__(self, url):
        self.pagereader = build_opener()
        self.pagereader.addheaders(headers)
        doc = pagereader.open(url, None, 15)
        self.soup = BeautifulSoup(doc)

        #Remove all comments
        comments = soup.findAll(text=lambda text:isinstance(text, Comment))
        [comment.extract() for comment in comments]

    @abstractmethod
    def url(self):
        """
        Return URL for page.

        """
        return

    @abstractmethod
    def title(self):
        """
        Returns the title of the article.

        """
        return

    @abstractmethod
    def published(self):
        """
        Returns a map containing date and time for when
        the article was published.

        """
        return

    @abstractmethod
    def updated(self):
        """
        Returns a map containing date and time for when
        the article was updated.

        """
        return

    @abstractmethod
    def authors(self):
        """
        Returns a list of the authors of the article.

        """
        return

    @abstractmethod
    def external_links(self):
        """
        Returns the number of external links in the article.

        """
        return

    @abstractmethod
    def internal_links(self):
        """
        Returns the number of external links in the article

        """
        return

    @abstractmethod
    def images(self):
        """
        Returns the number of images in the article.

        """
        return

    def word_count(self):
        """
        Returns the number of words in the article.

        """
        return

    def factbox(self):
        """
        Returns the number of words in the factbox if
        applicable.

        """
        return
