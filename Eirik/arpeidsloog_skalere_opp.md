 # Arbeidslogg NRK skalere opp:

# legge til et status felt i sqlite-filen
 sqlite3 nrk2013_2.db
 .tables
 ALTER TABLE links ADD COLUMN status TEXT;

# noen endringer:
python run.py -v INFO


# 
SELECT * FROM links WHERE status is NOT NULL;
SELECT count(*) FROM links WHERE status is NOT NULL;
SELECT count(*) as c, * FROM links WHERE status is NOT NULL group by status;
SELECT * FROM links WHERE link = "http://nrk.no/rogaland/kvelertak-pa-rolling-stone-liste-1.11416030";

# force progress by letting the query for the sqlite3 only target urlz where 
# status = NULL.

...
SELECT * FROM links WHERE status is NULL ORDER BY date DESC LIMIT 1,10;


# fixed problem with urls found from different pages (page,link in db)
# these needs to be updated regardless of from what page they where found.

# fixed code
# reset mysql & sqlite3 
UPDATE links SET status = NULL;

# nytt forsøk -> ok, but:
To check if .db & mysql is in sync, select distinct link from .db
...
SELECT * FROM links WHERE status = "scraped" group by link;
SELECT link, count(*) FROM links WHERE status = "scraped" group by link;

nei... 
### 

SELECT count(distinct link) as c FROM links WHERE status = "scraped";
vs
SELECT count(distinct url) as c FROM page;

# Notater med Helle
- antall bilder... skal også telle bilder fra faktaboks

wordtelling: alfa tror vi teller omtrent riktig. 
- hvordan teller vi antall ord?
- ord for mye {1, 7, 0, }
- word_count, line_count, char_count <- hvordan funker dette?? 

# same amount as in mysql
SELECT count(distinct link) FROM links WHERE status = "scraped"; 
# list the updated urlz
SELECT * FROM links WHERE status is NOT NULL;
# show the cats of updated 
SELECT count(*) as c, * FROM links WHERE status is NOT NULL group by status;


# mySQL Get all stories with NO author
# SELECT t1.url FROM page t1 LEFT JOIN author t2 ON t2.url = t1.url WHERE t2.url IS NULL;


### Todo torsdag:
- feil i autor-tabellen, folk mangler (ender opp som NULL; NULL; NULL;)
	-Fikset.
- antall bilder, skal også telle fra faktaboks
- antall lenker, skal også telle fra faktaboks
- antall ord, skal også telle fra faktaboks
- Hvorfor får jeg redundante URLer i mysql? 
	(tror dette er fikset med en commit().)










