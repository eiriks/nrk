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

DATASETT: N=alt


* fulltekst (hele saken, med unntak av delelemener (tittel, forfatter, etc) som lagres i andre felt.)

* Publiseringsdato (date)

* Klokkeslett (datetime)

* Oppdateringstidspunkt (datetime)

* Interaktive element (antall, int)

*  tekstlengde: Antall ord (all tekst - overskrift, ingress, bildetekster m.m.)

* lix Lesbarhetsindex-tall 
Se https://github.com/eiriks/samstemmer/blob/master/fylkesperspektiv/management/commands/compute_lix.py

* Nyhetsbyrå

 ```python
{
	0 : NA
	1 : NTB
	2 : ANB
	3 : Reuters
	4 : AP
	5 : AFP
	6 : NRK
	7 : Andre byråer
	8 : Flere byråer	
}
 ```
* Målform: nn || nb || annen_språkkode? 
bruk kode her: https://github.com/saffsd/langid.py funker overraskende bra.


* bildetekst (konkatinert ved flere bilder, formodentlig)


* Kommentarfelt
 ```python
{
	na || antall
}
 ```

* Spørreundersøkelse
 ```python
{
	na || antall
}
 ```


* Spillelement
 ```python
{
	na || antall
}
 ```

* Egentesting (poll)
 ```python
{
	na || antall
}
 ```

* Videofil
 ```python
{
	0.	NA
	1.	Flashfil
	2.	Ikke flashfil
	3.	Flere flashfiler
}
 ```

* Antall videofiler totalt (inkludere vimeo, youtube, osv)

* Antall videofiler fra NRK (egenproduksjon)


* Bildekarusell
 ```python
{
	0.	NA
	1.	Bildekarusell
	2.	Ikke bildekarusell
	3.	Flere bildekaruseller
}
 ```


*	Galleriboks aka. Relaterte saker
 ```python
{
	0.	NA
	1.	Galleriboks
	2.	Ikke galleriboks
	3.	Flere galleribokser
}
 ```

*	Flashfil 
 ```python
{
	0. 	NA
	1.	Flashfil
	2.	Ikke flashfil
	3.	Flere flashfiler
}
 ```

*	Andre interaktive element
 ```python
{
	0. 	NA
	1.	Annet interaktivt element
	2.	Ikke annet interaktivt element
	3.	Flere andre interaktive element
}
 ```


*	Lenkepraksis
 ```python
{
	0.	NA
	1.	Interne lenker
	2.	Eksterne lenker
	3.	Både interne og eksterne lenker
}
 ```

* interne lenker (antall)

* eksterne lenker (antall)

Skulle vi også ha lagret nettverket av hvem som lenker hvem?
Eller lagre root domenene som lenkes? Eller lenkens geografiske tilhørighet? 


* Publiseringssted (disse henter vi ut i fra URL'n)

 ```python
{
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
}
 ```
*	Programtilknytning
Dette henter vi ut i fra URL'n. Er det flere vi burde se etter?
 ```python
{
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
	18. Valg
	19. BarneTV aka nrksuper
}
 ```

* NRKs hovedkategorier nyheter
Hentes ut i fra URL
 ```python
{
	0.	NA
	1.	Forsiden
	2.	Norge
	3.	Verden
	4.	Økonomi
	5.	Sport
	6.	Kultur og underholdning
	7.	Helse og livsstil (puls)
	8.	Teknologi og vitenskap (katta)
	9.	Vær (yr.no)
	10. ut.no
}
 ```

* NRKs nyhetskategorier
Hentes fra URL
 ```python
{
	0.	NA
	1.	Siste nytt
	2.	Norge
	3.	Verden
	4.	Økonomi
	5.	Nobels fredspris
	6.	Klima
	7.	Distrikt
	8.	Valg 09 / Valg2012?
	9.	Kultur
	10.	Sport
}
 ```


* Les/Les også
Dette er en kontekstboks i den gamle designmalen (finnes dette i den nye?)
 ```python
{
	0.	NA
	1.	Les/Les også
	2.	Ikke Les/Les også
}
 ```

* Faktaboks
 ```python
{
	0.	NA
	1.	Ja
	2.	Nei
}
 ```

* antall faktabokser (finnes det eksempler der det er flere?)

* antall ord i faktaboks(er)

* Byline
OBS: En tekst kan ha flere forfattere
  - Navn
  - tittel
  - epost


* Bilder (antall)


* Deling facebook "like" (ja/nei)

* Deling facebook "share" (ja/nei)

* Deling twitter (ja/nei)

* Deling g+ (ja/nei)

* Deling annet (hvordan skal dette operasjonalliseres)


* Kart (antall)
  - antall
  - lat/long

### Skal vi lagre all html noe sted, slik at vi ikke trenger å pinge nrk enda en gang hvis vi finner ut at vi vill hente ut flere eller andre ting, eller hente ut på andre måter?







# Gammelt rusk:
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