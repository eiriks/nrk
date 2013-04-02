#!/usr/bin/python
# coding: latin-1

#----------------------------------
#nrk-meta.py
#printer ut metadata fra html-filer
#som tabulatorseparerte verdier
#ihht. kodeskjema
#----------------------------------

import sys
import string
import BeautifulSoup
import re

filnavninn=sys.argv[1]
file = open(filnavninn)
fn = str(filnavninn)

#list of urls, used to return the url in which the filename occurs:

url_list = open('/prosjekt/nrk/url-lister/big_url_list')			
#url_list = open('/prosjekt/nrk/url-lister/all-urls-2009')			#all urls from 2009 (our selection)
#url_list = open('/prosjekt/nrk/url-lister/urls-okonomi-2009.txt')		#all okonomi-urls from 2006- (nrk's selection)
#urls_i_nrk13_men_ikke_i_uib14							#nrk complement to our 14day-selection

url = "NA"

#date variables

dateVal = 100	# Variable 1 (publ.dato, 14d)
date = ""	# Variable 1 (publ.dato, heile 2009)
time = ""	# Variable 2 (klokkeslett)
odate = ""	# Variable 3 (dato, & kl.slett?) 
otime = ""

#interactive variables:

interactive = 0 	# Variable 4 (antall element totalt)
comment = 0
commentVal = 0		# Variable 5
poll = 0
pollVAl = 0		# Variable 6
game = 0
gameVal = 0		# Variable 7
test = 0
testVal = 0		# Variable 8
video = 0
videoVal = 0		# Variable 9
thumbnail = 0
thumbnailVal = 0	# Variable 10
gallery = 0
galleryVal = 0		# Variable 11
flash = 0
flashVal = 0
oie = 0			# Other interactive element
oieVal = 0
		

# article variables:

h1 = ""
h2 = ""
ingress = ""
para = ""
text = ""
links = ""
linktext = ""
words = ""	
wc = 0			# number of words in article
url_count = 0		# number of links 
internal = 0
external = 0 		
lenkepraksis = 0	# 0=NA, 1=interne  2=eksterne 3=baade interne og eksterne
linklist = []


# other:

author = "NA"
newsagency = "NA"
cite = ""
citeVal = 0
kontekstboks = 0
kontekstVal = 0

# category variables:

publiseringssted = ""
publ_stedVerdi = 10000

programtilknytning = ""
progVerdi = 100000

hovedkategori = ""
hkVerdi = 100000

nyhetskategori= ""
nyhetVerdi = 100000

nyhetskategori =""
nyhetVerdi = 100000

#variable lists:

date_list = [
    "19.01.2009",
    "20.01.2009",
    "11.02.2009",
    "12.03.2009",
    "24.04.2009",
    "16.05.2009",
    "21.06.2009",
    "13.07.2009",
    "18.08.2009",
    "16.09.2009",
    "15.10.2009",
    "13.11.2009",
    "05.12.2009",
    "20.12.2009"]  

date_list2 = [
    "2009-01-19",
    "2009-01-20",
    "2009-02-11",
    "2009-03-12",
    "2009-04-24",
    "2009-05-16",
    "2009-06-21",
    "2009-07-13",
    "2009-08-18",
    "2009-09-16",
    "2009-10-15",
    "2009-11-13",
    "2009-12-05",
    "2009-12-20"]
 
 
#-------------
#coding start
#-------------
    

while 1:

	f = file.read()				#les heile fila som ein streng 
	
	from BeautifulSoup import BeautifulSoup
	soup = BeautifulSoup(f) 
	
	if not soup: 
		print "NB! No file content"
		break


#------
#URL
#------
		
	
	# match filename against filname list
	
	while 2:
	
		linje = url_list.readline().rstrip()
			
		if not linje:
			break
		
		else:
			fn=fn.replace("/prosjekt/nrk/innhausting/2009/stripfiler/", "") # remove paths from filename
			fn=fn.replace("/prosjekt/nrk/innhausting/sitemapindex3/okonomi/", "")
			fn=fn.replace("/prosjekt/nrk/innhausting/nrk13/nrk13unik/", "")
			fn=fn.replace("/prosjekt/nrk/innhausting/", "")
			fn=fn.replace("/prosjekt/nrk/python/testfiler/", "")		
			fn=fn.replace("testfiler/", "")
			
			fn=fn.replace(".htm.htm", "")
			fn=fn.replace(".strip", "")				  # remove added file extension
			fn=fn.replace(".1.strip", "")                             # remove duplicate file ext.
			fn=fn.rstrip()						  # remove trailing whitespace
			fn=fn.lstrip()					          # remove preceding whitespace
		
			urls = linje.lstrip()
			
			if urls.find(fn) > -1:
				url = urls
				break
	
	
	# search for filename in input file's html code if no match in list
	
	while 3:
		if url == "NA":
			from BeautifulSoup import BeautifulSoup
			soup = BeautifulSoup(f) 			
			if soup.find("legend") > -1: 
				for legend in soup.findAll("legend"):
					if legend.renderContents() == "Permalenke":
						url = legend.findNext('a').renderContents()
						break
		break

#--------------------------------
#Publishing: date and time
#--------------------------------		
		
	#Variables 1-3
		
	# Alt.1: <p class="published">Publisert 15.05.2008 10:49. Oppdatert 15.05.2008 10:59.</p>
	
	if soup.find("p", { "class" : "published" }) > -1:
		published = soup.find("p", { "class" : "published" })
		published = str(published)
		
		if published.find('Oppdatert') > -1:
			index = published.find('Oppdatert')
			oppdatert = published[index-2:]
			published = published[:index-2]
			
			published = published.replace("<p class=\"published\">Publisert", "")
			date = published[:11]
			time = published[11:]
			date = date.strip()
			time = time.strip()
			
			oppdatert = oppdatert.replace(". Oppdatert", "")
			oppdatert = oppdatert.replace(".</p>", "")
			odate = oppdatert[:12]
			otime = oppdatert[12:]
		
		else:
			published = published.replace("<p class=\"published\">Publisert", "")
			published = published.replace(".</p>", "")
			published = published.strip()
			date = published[:11]
			date = date.strip()
			time = published[11:]
			time = time.strip()
			odate = "NA"
			otime = "NA"
			
	
		for i in xrange(len(date_list)):
				if date in date_list[i]:
					dateVal = i + 1  
					break
				 		
				else:	
					dateVal = "NA" #date not in date list
		
			
	
	
	# Alt.2: <div class="published"> ... 
			#<em>Publisert 2009-06-18 17:16:43
			    #/ Oppdatert 2009-06-16 12:56:58
			#</em>
		#...</div>
	
	elif soup.find("div", {"class" : "published" }) > -1:
		published = soup.find("div", {"class" : "published" })
		for tag in published.findAll():
			if tag.name == 'em':
				em = tag.renderContents()  
				em = em.replace("\n", "")
				
				if em.find('Oppdatert'):
					index = em.find('/ Oppdatert')
					oppdatert = em[index:]
					publisert = em[:index]
				
					oppdatert = oppdatert.lstrip("/")
					oppdatert = oppdatert.replace("Oppdatert", "")
					oppdatert = oppdatert.lstrip()
					oppdatert = oppdatert.rstrip()
					
					oppdatert = oppdatert.replace(".</p>", "")
					odate = oppdatert[:11]
					otime = oppdatert[11:]
				
					publisert = publisert.replace("Publisert", "")
					publisert = publisert.lstrip()
					publisert = publisert.rstrip()
					date = publisert[:10]
					time = publisert[10:]
					time = time.strip()
					
					
				else:
					published = em.lstrip()
					published = published.rstrip()
					
					date = publisert[:11]
					date = date.strip()
					time = publisert[11:]
					time = time.strip()
					odate = "NA"
					otime = "NA"
	
				for i in xrange(len(date_list2)):
					if date in date_list2[i]:
						dateVal = i + 1  
						break
				 		
					else:	
						dateVal = "NA" #date not in date list
		
	
					
				
		
	else:
		dateVal = "NA"
		date = "NA"
		time = "NA"
		odate = "NA"
		otime = "NA"
		
	
	
#if odate == 'NA':
#	odate = 0
#else:
#	odate = 1

	

		
#-----------------------
#Interactive elements
#Variables 4-12 
#-----------------------
	
	
	
	##Kommentarfelt
	
	if soup.find("li", {"class" : "comment-article"}) > -1:
		comment = comment + 1
		interactive = interactive + 1	#counting interactive elements
	
	
	if comment == 1:
		commentVal = 1
	elif comment == 0:
		commentVal = 2
	else:
		commentVal = 0
	
					
	##Spoerreundersoekelse <div class="poll">
	
	for polls in soup.findAll("div", {"class" : "poll"}):
		poll = poll + 1	
		interactive = interactive + 1	#counting interactive elements
	
	if soup.find("div", { "class" : "article" }) > -1:
		article = soup.find("div", { "class" : "article" })
			
		#Alt. 1
		for tag in article.findAll():
			if tag.name == 'h3' and tag.renderContents() == "Gi din karakter:":
				poll = poll + 1
				interactive = interactive + 1
				
		
		#Alt. 2 (depricated)
		#for intro in article.findAll("div", { "class" : "intro-element" }):
		#	for tag in intro.findAll("p"):
		#		if tag.find("div", id=re.compile("so_targ_spiller-avstemning_")) > -1:
		#			poll = poll + 1
		
		
	
	if poll == 0:
		pollVal = 2
	elif poll == 1:
		pollVal = 1
	elif poll > 1:
		pollVal = 3
	else:
		pollVal = 0
	
		
	##Spillelement
		
	if soup.find('div', {'class' : 'article article-wide' }) > -1:
			aw = soup.find('div', {'class' : 'article article-wide' })
			#if aw.find('strong').findNext('script').renderContents().find('minigame') > -1:
			if aw.find('strong') > -1:
				strong = aw.find('strong')
				if strong.findNext('script') > -1:
					script = strong.findNext('script')
					if script.renderContents().find('minigame') > -1:
						game = game + 1
						interactive = interactive + 1
	
	if game == 0:
		gameVal = 2
	elif game == 1:
		gameVal = 1
	elif game > 1:
		gameVal = 3
	else:
		gameVal = 0
		
	
	##Egentesting
	
		
	if soup.find("div", { "class" : "article" }) > -1:
		article = soup.find("div", { "class" : "article" })
		for a in article.findAll("a", href=re.compile("redskap\/quiz")):
			test = test + 1
			interactive = interactive + 1	#counting interactive elements
		

		if test == 0:
			testVal = 2
		elif test == 1:
			testVal = 1
		elif test > 1:
			testVal = 3
		else:
			testVal = 0
	
	
	##Videofil
		
	#Alt.1
	for videos in soup.findAll("div", {"class" : "video"}):
		video = video + 1
		interactive = interactive + 1 #counting interactive elements
		
	#Alt.2
	if soup.find("div", { "class" : "article" }) > -1:
		article = soup.find("div", { "class" : "article" })
		for ph in article.findAll("div", { "class" : "placeholder"}):
			for vi in ph.findAll("embed", src=re.compile("brightcove")):
				video = video + 1
				interactive = interactive + 1
	#Alt.3				
	if soup.find("div", {"class" : "article article-wide"}) > -1:
		articlewide = soup.find("div", {"class" : "article article-wide"})
		for ph in articlewide.findAll("div", { "class" : "placeholder"}):
			#if ph.find("embed", src=re.compile("brightcove")) > -1:
				#print "articlewide-VIDEO"
			for vi in ph.findAll("embed", src=re.compile("brightcove")):
				video = video + 1
				interactive = interactive + 1
		
	if video == 0:
		videoVal = 2
	elif video == 1:
		videoVal = 1
	elif video > 1:
		videoVal = 3
	else:
		videoVal = 0
		
	
	##Bildekarusell
	
	for thumbnails in soup.findAll("div", { "class" : "thumbnails" }):
		thumbnail = thumbnail + 1
		interactive = interactive + 1
	
	if thumbnail == 0:
		thumbnailVal = 2
	elif thumbnail == 1:
		thumbnailVal = 1
	elif thumbnail > 1:
		thumbnailVal = 3
	else:
		thumbnailVal = 0
	
	##Galleriboks
	
	for galleries in soup.findAll("div", {"class" : "list-light list-image-gallery"}):
		gallery = gallery + 1
		interactive = interactive + 1
	
	if gallery == 0:
		galleryVal = 2
	elif gallery == 1:
		galleryVal = 1
	elif gallery > 1:
		galleryVal = 3
	else:
		galleryVal = 0
		
		
	##Flashfil (ikkje video):
	#<div class="article article-wide"><div class=""><script type="text/javascript">
		
	if soup.find("div", {"class" : "article article-wide" }) > -1:
		aw = soup.find("div", {"class" : "article article-wide"})
		for f in aw.findAll("div", {"class" : ""}):
			if f.find("script", type="text/javascript") > -1:
				flash = flash + 1
				interactive = interactive + 1
		
	if flash == 0:
		flashVal = 2
	elif flash == 1:
		flashVal = 1
	elif flash > 1:
		flashVal = 3
	else:
		flashVal = 0
	
	##Twitterboks - under "article elements" 
			
	
	##interactive = poll + game + test + thumbnail + gallery + video + flash
	
	
#--------------------
#get article elements	
#--------------------
	
	# Main headline (h1) and ingress
		
	if soup.find("div", {"class" : "intro-element-article"}) > -1:
		intro = soup.find("div", {"class" : "intro-element-article"})
					
		for tag in intro.findAll():
			if tag.name == 'h1':
				text = text + "\n" + tag.renderContents() 
				h1 = tag.renderContents()
		
			if tag.name == 'p':
				text = text + "\n" + tag.renderContents() 
				ingress = tag.renderContents()			
		
	else:
		h1 = "NA"
		ingress = "NA"
		p = "NA"
	
	
	
	# Article content (sub-headlines and p-elements)
		
	
	if soup.find("div", { "class" : "article" }) > -1:
		article = soup.find("div", { "class" : "article" })
		
		
		##Twitterbox - register as 'other interactive element', extract link and add to links, extract linktext and add to text
		if article.find("div", {"class" : "article-twitterbox" }) > -1:
			twb = article.find("div", {"class" : "article-twitterbox" })
			if twb.find('b') > -1:
				ltext = "@"+twb.b.renderContents()
				linktext = linktext + "\n" + ltext
				text = text + linktext
			if twb.find("iframe") > -1:
				l = twb.find("iframe")
				link = l['src']
				links = links + "\n" + link 
				oie = oie + 1
				interactive = interactive + 1	
		
		if oie == 0:
			oieVal = 2
		elif oie == 1:
			oieVal = 1
		elif oie > 1:
			oieVal = 3
		else:
			oieVal = 0 
		
		
		#Factbox - include heading and text in text variable
		if article.find("div", {"class" : "facts-right" }) > -1:
			fr = article.find("div", {"class" : "facts-right" }) 
			#for strong in fr.findAll("strong"):			#captured by article-strong
			#	strong.replaceWith(strong.renderContents())
			for h3 in fr.findAll("h3"):
				text = text + "\n" + h3.renderContents()
			#for p in fr.findAll("p"):
			#	text = text + "\n" + p.renderContents()		#captured by article-p
			for li in fr.findAll("li"):
				text = text + "\n" + li.renderContents()
				

		#Regular text elements (<h2> and <p> with tag extractions and link-tag replacement)
		for tag in article.findAll():	
						
			if tag.name == 'h2':
	
				
				for link in tag.findAll("a"): 
											
					ltext = tag.find("a").renderContents()	
					linktext = linktext + "\n" + ltext 	# assign value to linktext-variable
						
					attr = link['href']
					links = links + "\n" + attr 		# assign value to link-variable
								
					link.replaceWith("@"+link.renderContents())	# remove link-element <a> from h2,
											# tag linktext as link elements
											# with preceding '@'
											
				if tag.find('strong') > -1:
					h2 = h2 + "\n" + tag.find('strong').renderContents()
					text = text + "\n" + tag.find('strong').renderContents()
				else:
					if tag.renderContents() != "&nbsp;":
						h2 = h2 + "\n" + tag.renderContents() 
						text = text + "\n" + tag.renderContents() 
					
			
			# keep name of cited person (address tag), but remove embedded (empty) cite tag
			
			#if tag.name == 'address':
			#	if not tag.parent("div", {"class" : "intro-element"}): 
			#		for c in tag.findAll('cite'):
			#			c.extract()
			#		text = text + "\n" + tag.renderContents()
				
				
			
			if tag.name == 'p':
				
				# remove 'a' tags, but keep its content and store to variable p 
					
				for link in tag.findAll("a"): 
					
					ltext = tag.find("a").renderContents()	
					linktext = linktext + "\n" + ltext 	# assign value to linktext-variable
						
					attr = link['href']
					links = links + "\n" + attr 			
						
					link.replaceWith("@"+link.renderContents())	
					
				# remove 'strong', 'img' and 'address' tags
					
				for strong in tag.findAll("strong"):
					strong.replaceWith(strong.renderContents())	
					
				for img in tag.findAll("div", {"class" : "img-left"}):
					img.extract()
						
				for img in tag.findAll("div", {"class" : "img-right"}):
					img.extract()
						
				for img in tag.findAll("div", {"class" : "img-center"}):
					img.extract()
				
				for img in tag.findAll("img"):
					img.extract()
					
				for address in tag.findAll("address"):
					address.extract()
				
				for script in tag.findAll("script", { "type" : "text/javascript" }):
					script.extract()
				
				for div in tag.findAll("div"):
					div.extract()
	
				if tag.renderContents() == " " or "" or None:
					para = para
				else:	
					para = para + "\n" + tag.renderContents()  	 	# write p-content to variable p 
					text = text + "\n" + tag.renderContents() 	# write p-content to variable text
			
			
			if tag.name == 'ul':
				for link in tag.findAll("a"): 
									
					ltext = tag.find("a").renderContents()	
					linktext = linktext + "\n" + ltext 	# assign value to linktext-variable
										
					attr = link['href']
					links = links + "\n" + attr 		# assign value to link-variable
										
					link.replaceWith("@"+link.renderContents())
					#text = text + "\n" + tag.li.renderContents()
					text = text + "\n" + tag.renderContents()
							
			
			
		
											
	else:
		text = "NA"
		h2 = "NA"
		break
		
	
		
				
#------------------------
#Calculate article length
#------------------------
	
	# refinement (doesn't work with BeautifulSoup)
	
	text = text.replace("<br />", "")
	text = text.replace("<br/>", "")
	text = text.replace("&nbsp;", " ")
	
	ingress = ingress.replace("<br />", "")
	ingress = ingress.replace("<br/>", "")
	
	# word count
	
	words = str(text)
	words = words.replace(" - ", " ")
	words = words.replace("- ", "")
	words = words.replace(" -", "")
	words = words.replace(".", "")
	words = words.replace(", ", " ")
	words = words.replace("(", "")
	words = words.replace(")", "")
	words = words.replace(",&nbsp;", ", ")
	words = words.split()
	
	wc = len(words)
	
	
#-------------
#Link count
#-------------
	
	linklist = links.split()
	url_count = len(linklist)
	
	linklist = str(linklist)
	linklist = linklist.replace("u'", "")
	linklist = linklist.replace("', ", ", ")
	linklist = linklist.replace("']", "]")
	
	for i in xrange(url_count):
		if linklist[i].find("nrk") > -1: 		
			internal = internal + 1						
		elif linklist[i].find("http://www") == -1:
			internal = internal + 1
		else:
			external = external + 1
	
	
	
	
# Assign value to variable 'lenkepraksis': 0=NA, 1=interne  2=eksterne 3=baade interne og eksterne
	
	
	if internal == 0 and external == 0:
		lenkepraksis = 0
	elif internal > 0 and external == 0:
		lenkepraksis = 1
	elif internal == 0 and external > 0:
		lenkepraksis = 2
	elif	internal > 0 and external > 0:
		lenkepraksis = 3
	else:
		lenkepraksis = 10000
		
	
	
#-----------
#News agency
#-----------
					


	for c in article.findAll('cite'):
		if c.parent.name == 'div':
			cite = c
			if cite.renderContents() == "":
				cite = "NA"
			else:
				cite = cite.renderContents()
				cite = cite.replace("(", "")
				cite = cite.replace(")", "")
				
	if cite == "NA":
		citeVal = 0
	elif cite == "NTB":
		citeVal = 1
	elif cite == "ANB":
		citeVal = 2
	elif cite == "Reuters":
		citeVal = 3
	elif cite == "AP":
		citeVal = 4
	elif cite == "AFP":
		citeVal = 5
	elif cite == "NRK":
		citeVal = 6
	elif cite.find("/") > -1: #More agencies
		citeVal = 8
	else:
		citeVal = 7	  #Other agencies, such as BBC News, DN, etc.	
							


		

#-------------------------------
#Publishing and news categories
#Variables 15-18
#-------------------------------


# Variable 15: 'publiseringssted'
	
	if url.find('hedmark_og_oppland') > -1:
		publiseringssted = "NRK Hedmark og Oppland"
		publ_stedVerdi = 2
	
	elif url.find('hordaland') > -1:
		publiseringssted = "NRK Hordaland"
		publ_stedVerdi = 3
	
	elif url.find('more_og_romsdal') > -1:
		publiseringssted = "NRK Møre og Romsdal"
		publ_stedVerdi = 4
		
	elif url.find('nordland') > -1:
		publiseringssted = "NRK Nordland"
		publ_stedVerdi = 5
		
	elif url.find('rogaland') > -1:
		publiseringssted = "NRK Rogaland"
		publ_stedVerdi = 6
		
	elif url.find('nrk_sogn_og_fjordane') > -1:
		publiseringssted = "NRK Sogn og Fjordane"
		publ_stedVerdi = 7
		
	elif url.find('sorlandet') > -1:
		publiseringssted = "NRK Sørlandet"
		publ_stedVerdi = 8
	
	elif url.find('troms_og_finnmark') > -1:
		publiseringssted = "NRK Troms og Finnmark"	
		publ_stedVerdi = 9
		
	elif url.find('trondelag') > -1:
		publiseringssted = "NRK Trøndelag"
		publ_stedVerdi = 10
		
	elif url.find('ostafjells') > -1:
		publiseringssted = "NRK Østafjells"
		publ_stedVerdi = 11

	elif url.find('ostfold') > -1:
		publiseringssted = "NRK Østfold"
		publ_stedVerdi = 12
	
	elif url.find('ostlandssendingen') > -1:
		publiseringssted = "NRK Østlandssendingen"
		publ_stedVerdi = 13
		
	elif url.find('sami_radio') > -1:
		publiseringssted = "NRK Samí Radio"	
		publ_stedVerdi = 14
	
	else:
		publiseringssted = "Riks"
		publ_stedVerdi = 1
		
	#elif url.find('nyheter') > -1:	#andre kriterie? 'nrk'?
		#publiseringssted = "Riks"
		#publ_stedVerdi = 1
		
	#else:
	#	publiseringssted = "NA"
	#	publ_stedVerdi = 0
	
	
# Variable 16:	'programtilknytning'
	
	if url.find('puls') > -1:
		programtilknytning = "Puls"
		progVerdi = 1
		
	elif url.find('fbi') > -1:
		programtilknytning = "Forbrukerinspektørene FBI"
		progVerdi = 2
		
	elif url.find('juntafil') > -1:
		programtilknytning = "Juntafil"
		progVerdi = 3
	
	elif url.find('norgesglasset') > -1:
		programtilknytning = "Norgesglasset"
		progVerdi = 4		
		
	
	elif url.find('migrapolis') > -1:
		programtilknytning = "Migrapolis"
		progVerdi = 5
		
	
	elif url.find('radiodokumentaren') > -1:
		programtilknytning = "Radiodokumentaren"
		progVerdi = 6
		
	
	elif url.find('schrodinger') > -1:
		programtilknytning = "Schrödingers katt"
		progVerdi = 7
		
	
	elif url.find('studio_sokrates') > -1:
		programtilknytning = "Studio Sokrates"
		progVerdi = 8
		
	
	elif url.find('p2-akademiet') > -1:
		programtilknytning = "P2 Akademiet"
		progVerdi = 9
		
	
	elif url.find('newton') > -1:
		programtilknytning = "Newton"
		progVerdi = 10
		
	
	elif url.find('kurer') > -1:
		programtilknytning = "Kurer"
		progVerdi = 11
		
	
	elif url.find('kunstreisen') > -1:
		programtilknytning = "Kunstreisen"
		progVerdi = 12
		
	
	elif url.find('nitimen') > -1:
		programtilknytning = "Nitimen"
		progVerdi = 13
		
	
	elif url.find('p3') > -1:
		programtilknytning = "P3.no (flere programmer)"
		progVerdi = 14
		
	
	elif url.find('spiller') > -1:
		programtilknytning = "Spiller.no"
		progVerdi = 15
		
	
	elif url.find('yr.no/nyhende') > -1:
		programtilknytning = "Vær (yr.no/nyhende)"
		progVerdi = 16
		
	
	elif url.find('lydverket') > -1:
		programtilknytning = "Lydverket"
		progVerdi = 17
		
	
	else:
		programtilknytning = "NA"
		progVerdi = 0
		


# Variable 17:	NRKs hovedkategorier nyheter

	if url.find('forsiden') > -1:
			hovedkategori = "forsiden"
			hkVerdi = 1
								
	elif url.find('norge') > -1:
		hovedkategori= "Norge"
		hkVerdi = 2
		
	elif url.find('verden') > -1:
		hovedkategori= "Verden"
		hkVerdi = 3
		
	elif url.find('okonomi') > -1:
		hovedkategori= "Økonomi"
		hkVerdi = 4		
		
	elif url.find('sport') > -1:
		hovedkategori= "Sport"
		hkVerdi = 5
		
	elif url.find('kultur') > -1:
		hovedkategori= "Kultur og underholdning"
		hkVerdi = 6
		
	elif url.find('underholdning') > -1:
		hovedkategori= "Kultur og underholdning"
		hkVerdi = 6
		
	elif url.find('puls') > -1:
		hovedkategori= "Helse og livsstil (puls)"
		hkVerdi = 7
		
	elif url.find('schrodinger') > -1:
		hovedkategori= "Teknologi og vitenskap (katta)"
		hkVerdi = 8
		
	elif url.find('yr.no/nyhende') > -1:
		hovedkategori= "Vær (yr)"
		hkVerdi = 9
		
	else:
		hovedkategori= "NA"
		hkVerdi = 0
			

# Variable 18:	NRKs nyhetskategorier

	if url.find('distrikt') > -1 and url.find('valg_2009') == -1 and url.find('sport') == -1:
		nyhetskategori= "Distrikt"
		nyhetVerdi = 7
		
	elif url.find('distrikt') > -1 and url.find('valg_2009') > -1 and url.find('sport') == -1:
		nyhetskategori= "Distrikt, Valg 09"
		nyhetVerdi = 0
			
	elif url.find('distrikt') > -1 and url.find('valg_2009') == -1 and url.find('sport') > -1:
		nyhetskategori= "Distrikt, Sport"
		nyhetVerdi = 0
		
	elif url.find('siste_nytt') > -1:
		nyhetskategori= "Siste nytt"
		nyhetVerdi = 1
								
	elif url.find('norge') > -1:
		nyhetskategori ="Norge"
		nyhetVerdi = 2
		
	#elif url.find('verden') or url.find('utenriks') > -1:
	elif url.find('verden') > -1:
		nyhetskategori ="Verden"
		nyhetVerdi = 3
			
	elif url.find('okonomi') > -1:
		nyhetskategori ="Økonomi"
		nyhetVerdi = 4		
		
	elif url.find('nobels_fredspris') > -1:
		nyhetskategori ="Nobels fredspris"
		nyhetVerdi = 5
		
	elif url.find('klima') > -1:
		nyhetskategori ="Klima"
		nyhetVerdi = 6
					
	elif url.find('valg_2009') > -1:
		nyhetskategori ="Valg 09"
		nyhetVerdi = 8

	elif url.find('kultur') > -1:
		nyhetskategori ="Kultur og underholdning"
		nyhetVerdi = 9
		
	elif url.find('underholdning') > -1:
		nyhetskategori ="Kultur og underholdning"
		nyhetVerdi = 9

	elif url.find('sport') > -1:
		nyhetskategori ="Sport"
		nyhetVerdi = 10
		
	else:
		nyhetskategori ="NA"
		nyhetVerdi = 0
	
	
#-------------------------------
#Context boxes
#-------------------------------

	for ll in soup.findAll("div", { "class" : "list-light" }):
		for tag in ll.findAll("h3"):
			if tag.renderContents() == "Les":
				kontekstboks = kontekstboks + 1
			if tag.renderContents() == "Les også":
				kontekstboks = kontekstboks + 1
			if tag.renderContents() == "Lenker":
				kontekstboks = kontekstboks + 1
	
	if kontekstboks == 0:
		kontekstVal = 2
	else:
		kontekstVal = 1
		
			
##----
	

	break
	
	
#print url, "\t", dateVal, "\t", date, "\t", time, "\t", odate, "\t", otime, "\t", interactive, "\t", comment, "\t", poll, "\t", game, "\t", test, "\t", video, "\t", thumbnail,  "\t", gallery, "\t", flash, "\t", oie, "\t", commentVal, "\t", pollVal, "\t", gameVal, "\t", testVal, "\t", videoVal, "\t", thumbnailVal, "\t", galleryVal, "\t",  flashVal, "\t", oieVal, "\t", wc, "\t", url_count, "\t", lenkepraksis, "\t", linklist, "\t", publ_stedVerdi, "\t", publiseringssted,  "\t", progVerdi, "\t", programtilknytning, "\t", hkVerdi, "\t", hovedkategori, "\t", nyhetVerdi, "\t", nyhetskategori, "\t", citeVal, "\t", cite, "\t", kontekstVal, "\t", kontekstboks

print url, "\t", dateVal, "\t", time, "\t", odate, "\t", interactive, "\t", commentVal, "\t", pollVal, "\t", gameVal, "\t", testVal, "\t", videoVal, "\t", thumbnailVal, "\t", galleryVal, "\t",  flashVal, "\t", oieVal, "\t", wc, "\t", url_count, "\t", lenkepraksis, "\t", publ_stedVerdi, "\t", progVerdi, "\t", hkVerdi, "\t", nyhetVerdi, "\t", citeVal, "\t", kontekstVal

#print text
