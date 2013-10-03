#!/usr/bin/python
# encoding: utf-8

## Tatt fra https://github.com/eiriks/samstemmer/blob/master/fylkesperspektiv/models.py

from nltk.tokenize import RegexpTokenizer, sent_tokenize
#from nltk import *

class  Lix():
    """
    LIX pr person basert på den teksten vi finner
    - http://sv.wikipedia.org/wiki/LIX
    - http://www.sprakrad.no/nb-NO/Toppmeny/Publikasjoner/Spraaknytt/Arkivet/2005/Spraaknytt_1-2_2005/Avisspraak/
    < 30 Mycket lättläst, barnböcker
    30 - 40 Lättläst, skönlitteratur, populärtidningar
    40 - 50 Medelsvår, normal tidningstext
    50 - 60 Svår, normalt värde för officiella texter
    > 60 Mycket svår, byråkratsvenska

    """
    def __init__(self, text):
        self.text = text
        # perhaps we should centralize tokenization?
        # I'll use this temporarily (Eirik)
        self.tokenizer = RegexpTokenizer('(?u)\W+|\$[\d\.]+|\S+')
        self.special_chars = ['.', ',', '!', '?']

    def get_lix_score(self):
        orda = self.analyzeText(self.text)    #print orda
        analyzedVars = orda         #.analyzedVars      #print analyzedVars
        score = 0.0
        longwords = 0.0
        for word in analyzedVars['words']:
            if len(word) >= 7:
                longwords += 1.0
        score = analyzedVars['wordCount'] / analyzedVars['sentenceCount'] + float(100 * longwords) / analyzedVars['wordCount']
        return score

    def analyzeText(self, text=''):
        if text != '':
            words = self.getWords(self.text)
            wordCount = len(words)
            sentenceCount = len(self.getSentences(self.text))
            #print "%s setninger" % sentenceCount
            analyzedVars = {}
            analyzedVars['words'] = words
            analyzedVars['wordCount'] = float(wordCount)
            analyzedVars['sentenceCount'] = float(sentenceCount)
            return analyzedVars

    def getWords(self, text=''):
        words = []                  #print type(text)    # should be unicode 
        words = self.tokenizer.tokenize(text)
        filtered_words = []
        for word in words:
            if word in self.special_chars or word == " ":
                pass
            else:
                new_word = word.replace(",","").replace(".","")
                new_word = new_word.replace("!","").replace("?","")
                filtered_words.append(new_word)
        return filtered_words

    def getSentences(self, text=''):
        sentences = []
        sentences = sent_tokenize(text)
        return sentences

