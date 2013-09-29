# coding: utf-8

from settings import rdbms_hostname, rdbms_username, rdbms_password

## RDBMS dependent code
def add_to_db(dict):
    insertion = open('insertion.sql', 'r').read()
    print "Warning: add_to_db(dict) is unimplemented"
    print "This action will merely print the statement that it WOULD have executed, if it had done so."
    print "It can't and it won't. (Later though, it will be able to, and will do so.)"

    print insertion.format(url_self_link="url_self_link IS NOT DONE",
                           title=dict['headline'].decode('unicode-escape'),
                           fulltext=dict['body'].decode('unicode-escape'),
                           publication_date=dict['published'].decode('unicode-escape'),
                           update_date=dict['updated'].decode('unicode-escape'),
                           scrape_date="scrape_date IS NOT DONE",
                           share_fb_like="share_fb_like IS NOT DONE",
                           share_fb_share="share_fb_share IS NOT DONE",
                           share_googleplus="share_googleplus IS NOT DONE",
                           share_twitter="share_twitter IS NOT DONE",
                           share_others="share_others IS NOT DONE",
                           article_language=dict['language'].decode('unicode-escape'),
                           lesbahet="lesbahet IS NOT DONE",
                           external_links="external_links IS NOT DONE",
                           internal_links="internal_links IS NOT DONE",
                           word_count="word_count IS NOT DONE",
                           line_count="line_count IS NOT DONE",
                           char_count="char_count IS NOT DONE",
                           factbox="factbox IS NOT DONE",
                           comment_fields="comment_fields IS NOT DONE",
                           comment_number="comment_number IS NOT DONE",
                           interactive_elements="interactive_elements IS NOT DONE",
                           poll="poll IS NOT DONE",
                           game="game IS NOT DONE",
                           video_files="video_files IS NOT DONE",
                           video_files_nrk="video_files_nrk IS NOT DONE",
                           flash_file="flash_file IS NOT DONE",
                           image_collection="image_collection IS NOT DONE",
                           images="images IS NOT DONE",
                           image_captions="image_captions IS NOT DONE",
                           related_stories="related_stories IS NOT DONE",
                           related_stories_box_thematic="related_stories_box_thematic IS NOT DONE",
                           related_stories_box_les="related_stories_box_les IS NOT DONE",
                           map="map IS NOT DONE",
                           regional_office="regional_office IS NOT DONE",
                           program_related="program_related IS NOT DONE",
                           main_news_category="main_news_category IS NOT DONE",
                           iframe="iframe IS NOT DONE" )
                             
                               
    
    return

