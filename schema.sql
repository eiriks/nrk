/*

        Model for nrk scraper
        Forsøker å joine den gamle & haakons

        sammen får vi gå gjennom hele guiden, finne dummy data, og teste opplegget
        -E

*/

DROP TABLE IF EXISTS author_page;
DROP TABLE IF EXISTS author;
DROP TABLE IF EXISTS page;


CREATE TABLE IF NOT EXISTS `author` (
  `autor_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `role` varchar(200) DEFAULT NULL,
  `url` varchar(256) NOT NULL DEFAULT '' COMMENT 'link to page',
  PRIMARY KEY (`autor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='One journo can be author on one text and photographer on a nother, so author needs to de a 1:n, not a n:m.';

CREATE TABLE IF NOT EXISTS `page` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(256) NOT NULL DEFAULT '',
  `title` varchar(256) NOT NULL DEFAULT '',
  `fulltext` text NOT NULL,
  `publication_date` datetime DEFAULT NULL COMMENT 'both date and time',
  `update_date` datetime DEFAULT NULL COMMENT 'both date and time',
  `scrape_date` datetime NOT NULL,
  `share_fb_like` int(11) NOT NULL,
  `share_fb_share` int(11) NOT NULL,
  `share_googleplus` int(11) NOT NULL,
  `share_twitter` int(11) NOT NULL,
  `share_others` int(11) NOT NULL,
  `article_language` varchar(50) DEFAULT NULL,
  `news_bureau` varchar(256) DEFAULT NULL,
  `external_links` int(11) DEFAULT NULL,
  `internal_links` int(11) DEFAULT NULL,
  `images` int(11) DEFAULT NULL,
  `word_count` int(11) DEFAULT NULL,
  `factbox` int(11) DEFAULT NULL COMMENT '0 false 1 true',
  `videos` int(11) DEFAULT NULL,
  `comment_fields` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `factbox` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(256) DEFAULT NULL,
  `num_links` int(11) DEFAULT NULL,
  `num_words` int(11) DEFAULT NULL,
  `factbox_text` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `links` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(256) NOT NULL DEFAULT '' COMMENT 'the page (article) we are examining',
  `link_to` varchar(256) DEFAULT NULL COMMENT 'the link that this row describes',
  `doc_type` varchar(256) DEFAULT NULL COMMENT 'doc, pdf, html, etx',
  `link_subdomain` varchar(256) DEFAULT NULL,
  `link_root_domain` varchar(256) DEFAULT NULL,
  `link_ tld` varchar(50) DEFAULT '' COMMENT 'to get countries se, dk, ..',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




-- CREATE TABLE IF NOT EXISTS author_page (
--        author INTEGER,
--        page INTEGER,
--        FOREIGN KEY(author) REFERENCES author(author_id),
--        FOREIGN KEY(page) REFERENCES page(page_id),
--        PRIMARY KEY(author, page)
-- );
