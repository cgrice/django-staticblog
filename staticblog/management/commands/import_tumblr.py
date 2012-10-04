from django.core.management.base import BaseCommand

from staticblog.app_settings import STATICBLOG_POST_DIRECTORY

import time
import json
import urllib2
import html2text

class Command(BaseCommand):
    help = "Import blog posts from tumblr"
    args = "<blog_url>"

    def handle(self, *args, **options):
        if len(args) != 1:
            print 'Incorrect arguments'
            return False
        url = args[0]
        if not 'http://' in url and not 'https://' in url:
            url = 'http://' + url
        url += '/api/read/json?debug=1'
        blog = urllib2.urlopen(url)
        blog = json.loads(blog.read())

        for post in blog['posts']:
            meta = ''
            if post['slug'] != '':
                filename = post['slug'] + '.post'
            else:
                filename = post['id'] + '.post'
            if post['type'] == 'regular':
                markdown = html2text.html2text(post['regular-body'])
                if post['regular-title'] == None:
                    post['regular-title'] = ' '
                meta = "Title: " + post['regular-title'] + "\n"
            elif post['type'] == 'audio':
                markdown = html2text.html2text(post['audio-caption'])
                markdown += "\n" + post['audio-player']
                meta = "Title: " + "\n"
            meta += "Summary: " + "\n"
            meta += "Author: " + "\n"
            meta += "Date: " + post['date-gmt'] + "\n"
            meta += "\n" 

            print "Importing %s" % filename

            with open(STATICBLOG_POST_DIRECTORY + filename, 'w') as f:
                f.write(meta)
                f.write(markdown.encode('UTF-8'))

            time.sleep(1)
                
        
        
