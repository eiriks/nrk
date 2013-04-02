nrk
===

Kode til automatisert innholdsanalyse av nrk.no


## Grunnleggende idé

Basert på en liste med URLer henter vi ut info om hver tekst. Vi
sparer på elementene i kodeboken i en database. Overskfrit, ingress,
brødtekst osv, alt lagres som i en rad i en stor tabell. Ved siste
korsvei holdt vi alt i en tabell (ingen relasjoner), mens det nok er
hensiktsmessig å legge til noen relasjoner her og der.

Hva vi henter ut er basert på kodeboken (som er designet for å besvare
et sett forskningsspørsmål). Det er ok å legge til flere variabler der
vi ser en gevinst og liten kostnad.



## Kodebok

AUTOMATISERT INNHOLDSANALYSE

DATASETT: N= XXXXX

###1.	Publiseringsdato (14 dager)
dette var den konstruerte to-ukersperioden

0.	Mandag 19 januar
1.	Tirsdag 27 januar
2.	Onsdag 11 februar
3.	Torsdag 12 mars
4.	Fredag 24 april
5.	Lørdag 16 mai
6.	Søndag 21 juni
7.	Mandag 13 juli
8.	Tirsdag 18 august
9.	Onsdag 16 september
10.	Torsdag 15 oktober
11.	Fredag 13 november
12.	Lørdag 5 desember
13.	Søndag 20 desember


### 1.	Publiseringsdato (hele 2009)

### 2.	Klokkeslett

### 3.	Oppdateringstidspunkt

### 4.	Interaktive element (antall)

### 5.	Kommentarfelt
0.	NA
1.	Kommentarfelt
2.	Ikke kommentarfelt
3.	antall kommentarfelt

### 6.	Spørreundersøkelse
0.	NA
1.	Spørreundersøkelse
2.	Ikke spørreundersøkelse
3.	Flere spørreundersøkelser

### 7.	Spillelement
0.	NA
1.	Spillelement
2.	Ikke spillelement
3.	Flere spillelement

### 8.	Egentesting
0.	NA
1.	Egentest
2.	Ikke egentest
3.	Flere egentester

### 9.	Videofil
0.	NA
1.	Flashfil
2.	Ikke flashfil
3.	Flere flashfiler
Er videoen fra nrk? (egenproduksjon)

### 10.	Bildekarusell
0.	NA
1.	Bildekarusell
2.	Ikke bildekarusell
3.	Flere bildekaruseller



### 11.	Galleriboks aka. Relaterte saker
0.	NA
1.	Galleriboks
2.	Ikke galleriboks
3.	Flere galleribokser

### 12.	Flashfil

	0. 	NA
	1.	Flashfil
	2.	Ikke flashfil
	3.	Flere flashfiler

### 13.	Andre interaktive element

	0. 	NA
	1.	Annet interaktivt element
	2.	Ikke annet interaktivt element
	3.	Flere andre interaktive element

###14.	Ordtelling
all tekst (overskrift, ingress, bildetekster m.m.)
lix # se https://github.com/eiriks/samstemmer/blob/master/fylkesperspektiv/management/commands/compute_lix.py


###15.	Lenker (antall)
antall interne
antall eksterne

###16.	Lenkepraksis
0.	NA
1.	Interne lenker
2.	Eksterne lenker
3.	Både interne og eksterne lenker

###17.	Publiseringssted
0.	NA
1.	NRK Riks
2.	NRK Hedmark og Oppland
3.	NRK Hordaland
4.	NRK Møre og Romsdal
5.	NRK Nordland
6.	NRK Rogaland
7.	NRK Sogn og Fjordane
8.	NRK Sørlandet
9.	NRK Troms og Finnmark
10.	NRK Trøndelag
11.	NRK Østafjells
12.	NRK Østfold
13.	NRK Østlandssendingen
14.	NRK Samí Radio

###18.	Programtilknytning
0.	NA
1.	Puls
2.	Forbrukerinspektørene FBI
3.	Juntafil
4.	Norgesglasset
5.	Migrapolis
6.	Radiodokumentaren
7.	Schrödingers katt
8.	Studio Sokrates
9.	P2 Akademiet
10.	Newton
11.	Kurer
12.	Kunstreisen
13.	Nitimen
14.	P3.no (flere programmer)
15.	 Spiller.no
16.	Vær (yr.no/nyhende)
17.	 Lydverket

###19.	NRKs hovedkategorier nyheter
0.	NA
1.	Forsiden
2.	Norge
3.	Verden
4.	Økonomi
5.	Sport
6.	Kultur og underholdning
7.	Helse og livsstil (puls)
8.	Teknologi og vitenskap (katta)
9.	 Vær (yr)

###20.	NRKs nyhetskategorier
0.	NA
1.	Siste nytt
2.	Norge
3.	Verden
4.	Økonomi
5.	Nobels fredspris
6.	Klima
7.	Distrikt
8.	Valg 09
9.	Kultur
10.	Sport

###21.	Nyhetsbyrå
0 = NA
1 = NTB
2 =  ANB
3 = Reuters
4 = AP
5 = AFP
6 = NRK
7 = Andre byråer
 8 = Flere byråer

###22.	Les/Les også
0.	NA
1.	Les/Les også
2.	Ikke Les/Les også


###23 Faktaboks
antall ord

###24 Byline
Navn
tittel
epost


###25 Bilder
antall

###26 Kart
antall
lat/long

###Deling
facebook (like)
facebook dele
twitter
g+
