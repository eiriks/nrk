# coding: utf-8

# Bare et sted å legge kommentarer



15. okt, går igjennom første resultatset fra scrapingen.

page-tabellen:
- 49.344 enheter basert på data for halve året kan stemme.
- url og url_self_link kolonnene ser bra ut
- title of full_text har encoding issues (tekst i filer skal være utf8 og programinterne skal det være unicode)
- dato-feltene ser riktige nokså ut 
	(SELECT * FROM page WHERE `publication_date` = "0000-00-00 00:00:00") gir 307 resultater, hvorav de jeg har 
	sjekket har dato i det som ser ut til å være et forutsigbart format,

	(SELECT * FROM page WHERE `update_date` = "0000-00-00 00:00:00") gir 9454 resultater, som variere mellom å være
	tekster uten oppdateringstidspunkt og tekster som faktisk har det...

- share-variablene ser alle ut til å være 1 hele veien (SELECT * FROM page WHERE `share_fb_like` != '1' gir 0 resultater)
	dette er jo templaten, så det virker rimelig.

- språk-sistribusjon: (SELECT COUNT(*), `article_language` from page group by `article_language`)
	ser ok ut? men etter en rask test er jeg litt usikker på om dette funker som forventet...
	1	da (denne er feil)
	1	en (denne er feil)
	16	NA (hvorfor vi får NA på disse er vanskelig å si, her er tekst..)
	62	nb
	4054	nn (her er det mye bokmål)
	45208	no
	1	se 
	1	sv (denne er feil, men forståelig)

- lesbarhet (SELECT count(*) c,`lesbahet`, url FROM page group by `lesbahet` order by lesbahet desc)
	distribusjonen går mellom 21 og 183, hvorav det meste ligger innefor det forventede (30-60).
	Ved å prøve de værste unntakene manuellt får jeg ulike verdier enn forventet. Hva slags innput brukes her?
	(skal være overskrift+full_text)


- nyhetsbyrå: (SELECT count(*),news_bureau FROM page group by `news_bureau`)
	49344	NA
	kan det stemme? Neppe..


- eksterne lenker (SELECT count(*),`external_links` FROM page group by `external_links`)
	COUNT 	amount
	62	16
	144	17
	544	18
	2875	19
	5140	20
	28775	21
	2771	22
	1354	23
	826	24
	1192	25
	884	26
	396	27
	1304	28
	1414	29
	985	30
	423	31
	158	32
	50	33
	11	34
	16	35
	8	36
	3	37
	4	39
	1	40
	1	46
	3	56
her hentes lenker ut i fra hele siden, ikke kun innefor artikkelen. tallene over er nødvendigvis veldig feil.

- interne lenker: samme proble som over, alt for høye verdier.

- ordtelling (SELECT count(*) c,`word_count`, url FROM page group by `word_count` order by word_count desc)
distribusjonen ligger mellom -1 og 215. 
dette er helt klart feil. Her må vi ha en alternativ måte. 
F.eks. har NLTK dette som en del av tf-idf impelemteringen sin.

- line count & char count er ditto off

- faktaboks (SELECT count(*) c,`factbox`, url FROM page group by `factbox` order by factbox desc)
count 	n 	url-eksempel
27689	1	http://www.nrk.no/livsstil/hvordan-bli-den-ultimate-jegeren-1.11286386
21655	0	http://nrk.no/17mai/17.-mai-i-norges-storste-byer-1.11015040

ser riktig ut.

- kommentarfelt (SELECT count(*) c,`comment_fields`, url FROM page group by `comment_fields` order by comment_fields desc)
count 	n 	url
3906	1	http://nrk.no/17mai/17.-mai-i-norges-storste-byer-1.11015040
45438	0	http://www.nrk.no/livsstil/hvordan-bli-den-ultimate-jegeren-1.11286386

7,9% har kommentarfelt. Det kan kanskje stemme?

- antall kommentarer (SELECT count(*) c,`comment_number`, url FROM page group by `comment_number` order by comment_number desc)
 varierer mellom 0 og 50. ser riktig ut, men kan 50 være en begrensning i API til discuss eller andre steder?
 det er rart at en max verdi har hele 18 enheter

 - interaktive elementer (SELECT count(*) c,`interactive_elements`, url FROM page group by `interactive_elements` order by interactive_elements desc)
count 	n 	test-url
1		3	http://nrk.no/nordnytt/hun-blogger-for-livet-1.11022017
5		2	http://nrk.no/nyheter/distrikt/nrk_sogn_og_fjordane/1.11042812
1603	1	http://nrk.no/ho/1.10970815
47735	0	http://www.nrk.no/livsstil/hvordan-bli-den-ultimate-jegeren-1.11286386

3,2 % har interaktivt element.
Ser dette rimelig ut?


- poll (SELECT count(*) c,`poll`, url FROM page group by `poll` order by poll desc)
alle har -1 aka det finnes ikke. det kan vel ikke stemme?

- game
ditto. alle har -1


- videofiler (SELECT count(*) c,`video_files`, url FROM page group by `video_files` order by video_files desc)
bortsett fra at merkelig mange har 5 videoer, så ser ikke dette helt umulig ut:
count 	n 	url-eksempel
1		35	http://nrk.no/nyheter/distrikt/rogaland/1.7426764
1		24	http://nrk.no/nyheter/distrikt/nrk_trondelag/1.10848644
1		19	http://nrk.no/nyheter/distrikt/nrk_sogn_og_fjordane/1.10879237
2		16	http://nrk.no/nyheter/distrikt/nrk_sogn_og_fjordane/1.7672401
4		14	http://nrk.no/nyheter/distrikt/hedmark_og_oppland/1.11037577
2		13	http://nrk.no/ho/historien-om-arhundrets-stemme-1.11066091
1		12	http://nrk.no/nyheter/distrikt/nordland/1.8392119
8		11	http://nrk.no/nyheter/distrikt/nrk_sogn_og_fjordane/1.8718195
20		10	http://nrk.no/fordypning/sju-au-pair-historier-1.10992858
143		9	http://nrk.no/kultur-og-underholdning/1.10975029
21		8	http://nrk.no/nyheter/distrikt/nordland/1.10863159
214		7	http://nrk.no/fordypning/viktigheten-av-dna---60-ar-etter-1.10929795
713		6	http://nrk.no/fordypning/40-ar-med-frp-1.10971798
24000	5	http://www.nrk.no/livsstil/hvordan-bli-den-ultimate-jegeren-1.11286386
1885	4	http://nrk.no/fordypning/1.10864983
6535	3	http://nrk.no/fordypning/1.10773020
682		2	http://nrk.no/ho/1.10970815
3287	1	http://nrk.no/ho/1.10893554
11824	0	http://nrk.no/17mai/17.-mai-i-norges-storste-byer-1.11015040

Vell, kun 24% har IKKE video. er ikke det litt rart?

- videofiler fra nrk (SELECT count(*) c,`video_files_nrk`, url FROM page group by `video_files_nrk` order by video_files_nrk desc)
c 	n 	url
1	35	http://nrk.no/nyheter/distrikt/rogaland/1.7426764
1	24	http://nrk.no/nyheter/distrikt/nrk_trondelag/1.10848644
1	19	http://nrk.no/nyheter/distrikt/nrk_sogn_og_fjordane/1.10879237
2	16	http://nrk.no/nyheter/distrikt/nrk_sogn_og_fjordane/1.7672401
4	14	http://nrk.no/nyheter/distrikt/hedmark_og_oppland/1.11037577
2	13	http://nrk.no/ho/historien-om-arhundrets-stemme-1.11066091
1	12	http://nrk.no/nyheter/distrikt/nordland/1.8392119
8	11	http://nrk.no/nyheter/distrikt/nrk_sogn_og_fjordane/1.8718195
20	10	http://nrk.no/fordypning/sju-au-pair-historier-1.10992858
142	9	http://nrk.no/kultur-og-underholdning/1.10975029
20	8	http://nrk.no/nyheter/distrikt/nordland/1.10863159
207	7	http://nrk.no/fordypning/viktigheten-av-dna---60-ar-etter-1.10929795
705	6	http://nrk.no/fordypning/40-ar-med-frp-1.10971798
23933	5	http://www.nrk.no/livsstil/hvordan-bli-den-ultimate-jegeren-1.11286386
1592	4	http://nrk.no/fordypning/1.10864983
6903	3	http://nrk.no/fordypning/1.10773020
654	2	http://nrk.no/ho/1.10970815
3236	1	http://nrk.no/ho/1.10893554
11912	0	http://nrk.no/17mai/17.-mai-i-norges-storste-byer-1.11015040

overlapper som forventet neste helt med tabellen over, virker rimelig. (men kanskje er ikke tabellen over rimelig)

- flash filer (SELECT count(*) c,`flash_file`, url FROM page group by `flash_file` order by flash_file desc)
c 	flash 	url-eksempel
1	6	http://nrk.no/kultur-og-underholdning/1.10864575
1	5	http://nrk.no/vitenskap-og-teknologi/1.10992229
2	4	http://nrk.no/nyheter/distrikt/nrk_sogn_og_fjordane/1.8308014
12	3	http://nrk.no/kultur-og-underholdning/1.10875149
60	2	http://nrk.no/kultur-og-underholdning/1.10849175
449	1	http://nrk.no/helse-forbruk-og-livsstil/1.10457342
48819	0	http://www.nrk.no/livsstil/hvordan-bli-den-ultimate-jegeren-1.11286386


virker rimelig, men her finnes youtube blandt eksemplene, youtube burde vært under video, vi leiter etter 
alternative flash-filer her. f.eks. små-spill, animasjoner, osv som ikke fanges opp under andre variabler.

- bildekaruseller (SELECT count(*) c,`image_collection`, url FROM page group by `image_collection` order by image_collection desc)
ingen funnet. dette er en feil.

- bilder (SELECT count(*) c,`images`, url FROM page group by `images` order by images desc)
distribusjon i 70 puljer mellom 0 og 790. enn så sprøtt det høres ut med 790 bilder, så stemme dette. urlen 
med 790 bilder inneholder en bråte med store bildekaruseller. Dette minner om at bildekaruseller burde ha 
blitt plukket opp og her er en eksempel-url: http://www.nrk.no/rogaland/rogaland-i-bilder-2012-1.7962507
Kun 7 artikler har ikke bilde, og 24481 har 14 bilder, dette virker snodig.

- bildetekst har encoding-issues (skal være utf-8)

- related stories er 6 på alle, (SELECT count(*) c,`related_stories`, url FROM page group by `related_stories` order by related_stories desc)
er dette templaten? Stemmer det i alle tilfeller?


- related_stories_box_thematic && related_stories_box_les
samme som over

- kart. ingen har kart. kan neppe stemme.

- regionskontor (SELECT count(*) c,`regional_office`, url FROM page group by `regional_office` order by c desc)
antall 	kontor					url-eksempel
40192	NA						http://www.nrk.no/livsstil/hvordan-bli-den-ultimate-jegeren-1.11286386
1618	NRK Østlandssendingen	http://nrk.no/nyheter/distrikt/ostlandssendingen/1.10282684
1350	NRK Hordaland			http://nrk.no/hordaland/1-0-pa-brann-stadion-1.11031047
1116	NRK Østafjells			http://nrk.no/nyheter/distrikt/ostafjells/buskerud/1.10045518
1034	NRK Rogaland			http://nrk.no/nyheter/distrikt/rogaland/1.1037872
903		NRK Sørlandet			http://nrk.no/nyheter/distrikt/sorlandet/1.10263610
899		NRK Nordland			http://nrk.no/nordland/1.10878022
878		NRK Østfold				http://nrk.no/nyheter/distrikt/ostfold/1.10037961
334		NRK Troms og Finnmark	http://nrk.no/nordnytt/1100-har-sokt-turnusplass-i-nord-1.11063445
333		NRK Sogn og Fjordane	http://nrk.no/sognogfjordane/1-0-til-forde-i-forste-omgang-1.11058527
263		NRK Trøndelag			http://nrk.no/trondelag/300-ansatte-far-ikke-bo-her-1.11076290
234		NRK Møre og Romsdal		http://nrk.no/mr/1.11012760
181		NRK Hedmark og Oppland	http://nrk.no/ho/1.10852333
7		NRK Norge				http://nrk.no/norge/1.11013412
2		NRK Sápmi				http://nrk.no/sapmi/1.1845872

dette hentes ut fra url, så dette vil inneholde en del feil. Likevell ser ikke distribusjonen helt gal ut, 
selv om NA er veldig høy (helt akseptabelt) og Sapmi veldig lav.


- programtilknytning (SELECT count(*) c,`program_related`, url FROM page group by `program_related` order by c desc)
antall	program 	url-eksempel
47113	NA			http://www.nrk.no/livsstil/hvordan-bli-den-ultimate-jegeren-1.11286386
1460	Fotball		http://nrk.no/sport/fotball/10-kampar-for-rasistisk-oppforsel-1.11041641
644		Ytring		http://nrk.no/ytring/1.10434903
96		Fordypning	http://nrk.no/fordypning/1.10773020
29		Valg		http://nrk.no/valg2013/455-milliarder-mer-til-samferdsel-1.11071064
2		Sapmi		http://nrk.no/sapmi/1.1845872

NA er høy. er det ikke mer goodies inni her, mon tro?

- hovedkategori nyheter (SELECT count(*) c,`main_news_category`, url FROM page group by `main_news_category` order by c desc)
antall	kategori			url-eksempel
23674	Helse og livsstil	http://www.nrk.no/livsstil/hvordan-bli-den-ultimate-jegeren-1.11286386
13204	Distrikt			http://nrk.no/nyheter/distrikt/hedmark_og_oppland/1.10037459
4972	NA					http://nrk.no/17mai/17.-mai-i-norges-storste-byer-1.11015040
4263	Sport				http://nrk.no/sport/1.10362597
2590	Verden				http://nrk.no/nyheter/verden/1.10309798
401		Økonomi				http://nrk.no/nyheter/okonomi/1.10039478
204		Kultur og underholdning	http://nrk.no/nyheter/kultur/1.10871583
29		Valg 2013			http://nrk.no/valg2013/455-milliarder-mer-til-samferdsel-1.11071064
7		Norge				http://nrk.no/norge/1.11013412

Helst og livsstil er vanligvis en liten nyhetskategori. her må det være en feil noe sted.

- iframes (SELECT count(*) c,`iframe`, url FROM page group by `iframe` order by c desc)
antall	frams 	url-eksempel
47735	0	http://www.nrk.no/livsstil/hvordan-bli-den-ultimate-jegeren-1.11286386
1603	1	http://nrk.no/ho/1.10970815
5		2	http://nrk.no/nyheter/distrikt/nrk_sogn_og_fjordane/1.11042812
1		3	http://nrk.no/nordnytt/hun-blogger-for-livet-1.11022017

dette ser riktig ut.


