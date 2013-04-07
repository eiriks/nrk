/*

        Model for nrk scraper

*/


CREATE TABLE IF NOT EXISTS author (
       author_id INTEGER PRIMARY KEY ASC,
       name TEXT NOT NULL,
       email TEXT UNIQUE,
       role TEXT
);

CREATE TABLE IF NOT EXISTS page (
       page_id INTEGER PRIMARY KEY ASC,
       url TEXT UNIQUE,
       title TEXT NOT NULL,
       published DATETIME NOT NULL,
       updated DATETIME,
       external_links INTEGER NOT NULL,
       internal_links INTEGER NOT NULL,
       images INTEGER NOT NULL,
       word_count INTEGER NOT NULL,
       factbox INTEGER,
       news_agency TEXT,
       videos INTEGER NOT NULL,
       comment_fields INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS author_page (
       author INTEGER,
       page INTEGER,
       FOREIGN KEY(author) REFERENCES author(author_id),
       FOREIGN KEY(page) REFERENCES page(page_id),
       PRIMARY KEY(author, page)
);
