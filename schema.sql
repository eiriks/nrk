/*

        Model for nrk scraper
        Forsøker å joine den gamle & haakons

        sammen får vi gå gjennom hele guiden, finne dummy data, og teste opplegget
        -E

*/

USE nrk; /* hos meg heter dataabsen jeg bruker nrk -Haakon */

DROP TABLE IF EXISTS author_page;
DROP TABLE IF EXISTS author;
DROP TABLE IF EXISTS page;
DROP TABLE IF EXISTS links;
DROP TABLE IF EXISTS factbox;

CREATE TABLE IF NOT EXISTS `author` (
  `autor_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(256) NOT NULL COMMENT 'link to page',
  `name` varchar(200) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `role` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`autor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='One journo can be author on one text and photographer on a nother, so author needs to de a 1:n, not a n:m.';

CREATE TABLE IF NOT EXISTS `page` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(256) NOT NULL DEFAULT '' COMMENT 'inputt url',
  `url_self_link` varchar(256) DEFAULT NULL COMMENT 'ta med "kopier lenkeadresse"',
  `title` varchar(256) NOT NULL DEFAULT '',
  `full_text` text NOT NULL,
  `publication_date` datetime DEFAULT NULL COMMENT 'both date and time',
  `update_date` datetime DEFAULT NULL COMMENT 'both date and time',
  `scrape_date` datetime NOT NULL,
  `share_fb_like` int(1) NOT NULL,
  `share_fb_share` int(1) NOT NULL,
  `share_googleplus` int(1) NOT NULL,
  `share_twitter` int(1) NOT NULL,
  `share_others` int(1) NOT NULL,
  `article_language` varchar(50) DEFAULT NULL COMMENT 'maalform',
  `lesbahet` float DEFAULT NULL,
  `news_bureau` varchar(256) DEFAULT NULL,
  `external_links` int(11) DEFAULT NULL,
  `internal_links` int(11) DEFAULT NULL,
  `word_count` int(11) DEFAULT NULL,
  `line_count` int(11) DEFAULT NULL,
  `char_count` int(11) DEFAULT NULL,
  `factbox` int(11) DEFAULT NULL COMMENT 'antall',
  `comment_fields` int(11) DEFAULT NULL COMMENT 'antall kommentarfelt',
  `comment_number` int(11) DEFAULT NULL COMMENT 'antall kommentarer',
  `interactive_elements` int(11) DEFAULT NULL COMMENT 'antall',
  `poll` int(11) DEFAULT NULL COMMENT 'antall',
  `game` int(11) DEFAULT NULL COMMENT 'antall',
  `video_files` int(11) DEFAULT NULL COMMENT 'sum alle videofiler',
  `video_files_nrk` int(11) DEFAULT NULL COMMENT 'antall NRKinterne videoer',
  `flash_file` int(11) DEFAULT NULL COMMENT 'antall',
  `image_collection` int(11) DEFAULT NULL COMMENT 'antall karuseller',
  `images` int(11) DEFAULT NULL COMMENT 'antall bilder',
  `image_captions` varchar(1024) DEFAULT NULL COMMENT 'konkatinert ved flere bilder',
  `related_stories` int(11) DEFAULT NULL COMMENT 'antall',
  `related_stories_box_thematic` int(11) DEFAULT NULL COMMENT 'antall stories',
  `related_stories_box_les` int(11) DEFAULT NULL COMMENT 'abtall stories',
  `map` int(11) DEFAULT NULL COMMENT 'antall',
  `regional_office` varchar(256) DEFAULT NULL COMMENT 'i URL: hordaland, østafjells, osv',
  `program_related` varchar(256) DEFAULT NULL COMMENT 'i URL: program teksten tilhores. f.eks. migrapolis eller forbrukerinspektorene',
  `main_news_category` varchar(256) DEFAULT NULL COMMENT 'i URL: finnes i globalmenyen',
  `iframe` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS  `factbox` (
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
  `link_tld` varchar(50) DEFAULT '' COMMENT 'to get countries se, dk, ..',
  `internal` int(1) DEFAULT NULL COMMENT 'nrk.no, yr.no, nrkabeta.no, p3.no, ...',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




-- CREATE TABLE IF NOT EXISTS author_page (
--        author INTEGER,
--        page INTEGER,
--        FOREIGN KEY(author) REFERENCES author(author_id),
--        FOREIGN KEY(page) REFERENCES page(page_id),
--        PRIMARY KEY(author, page)
-- );
