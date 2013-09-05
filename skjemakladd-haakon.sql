/*
        Model for NRK-scraper
	Oppdatert 5/9 2013 av Haakon
	Dette er en kladd enn så lenge, ikke kjør denne!
*/

/* Kommentert ut for å unngå galskap og vondskap.
DROP TABLE IF EXISTS author_page;  
DROP TABLE IF EXISTS author;
DROP TABLE IF EXISTS page;
*/

CREATE TABLE IF NOT EXISTS author (
       author_id INTEGER PRIMARY KEY ASC,
       name TEXT NOT NULL,
       email TEXT UNIQUE,
       role TEXT
);

CREATE TABLE IF NOT EXISTS page (
--       page_id INTEGER PRIMARY KEY ASC, -- Mente å huske
-- 	 DATETIME er dato + tidspunkt
       url TEXT UNIQUE,	 
       title TEXT NOT NULL,
       fulltext LONGTEXT NOT NULL,
       /* 
       	For å gjøre det lettere å søke gjennom databasen er dette gjort slik akkurat nå.
        Det burde gjøres bedre, og så kunne vi heller lagt ved eksempelspørringer, men akkurat nå er det en slik en.
       */
	Akkurat nå er ting bare lagt ut slik 
       -- <todo class="absolutely_disgusting" >
       publication_date date NOT NULL,
       publication_time time NOT NULL,
       update_date date NOT NULL,
       update_time time NOT NULL,
       scrape_date date NOT NULL,
       scrape_date time NOT NULL,
       -- </todo>
       share_fb_like INTEGER NOT NULL,
       share_fb_share INTEGER NOT NULL,
       share_twitter INTEGER NOT NULL,
       share_googleplus INTEGER NOT NULL,
       share_others INTEGER NOT NULL,
       article_language TEXT NOT NULL,
       news_bureau INTEGER NOT NULL -- Jeg antar at vi skal gjøre oppslag her?
);

CREATE TABLE IF NOT EXISTS factbox (
       parent_article_url,
       num_links INTEGER,
       num_words INTEGER,
       factbox_text TEXT,
       FOREIGN KEY(parent_article_url) REFERENCES page(url),
       PRIMARY KEY (parent_article_url)
);

CREATE TABLE IF NOT EXISTS authorships (
       author INTEGER,
       page INTEGER,
       FOREIGN KEY(author) REFERENCES author(author_id),
       FOREIGN KEY(page) REFERENCES page(page_id),
       PRIMARY KEY(author, page)
);
