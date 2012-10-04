from django.core.management.base import BaseCommand
from django.test.client import Client

import sys
import os
from optparse import make_option

from staticblog.app_settings import STATICBLOG_POST_DIRECTORY, STATICBLOG_COMPILE_DIRECTORY

class Command(BaseCommand):
    help = "Compile blog posts from html to markdown, and upload images to S3 Defaults to processing only new blog posts"
    option_list = BaseCommand.option_list + (
        make_option('--all',
            action='store_true',
            dest='all',
            default=False,
            help='Get all blog posts, regardless of date'
        ),
        make_option('--name',
            action='store',
            dest='post_name',
            default=False,
            help='Get named blog post'
        ),
    )

    def handle(self, *args, **options):
        client = Client()
        outdir = STATICBLOG_COMPILE_DIRECTORY
        posts = []
        previews = []
        
        if options['all']:
            print 'Compiling all blog posts'
            posts = self._get_all_posts()
        elif options['post_name']:
            posts = self._get_named_posts(options['post_name'])
        else:
            print 'Compiling new blog posts'
            posts = self._get_all_posts(new = True)

        print '%d posts found' % len(posts)
        print '----------------------------'

        for post in posts:  
            print "Compiling " + post['md_name'] + " to " + post['html_name']
            path = '/preview/' + post['path']
            resp = client.get(path)
            if os.path.exists(outdir + post['path']) == False:
                try:
                    with open(outdir + post['path'], 'r') as f: 
                        pass
                except IOError as e:
                    os.mkdir(outdir + post['path'])

            with open(outdir + post['html_name'], 'w') as f:
                f.write(resp.content) 

        if len(posts) > 0:
            print '----------------------------'

        print 'Updating listings...'
        print '----------------------------'
        path = '/preview/'
        resp = client.get(path)

        with open(STATICBLOG_COMPILE_DIRECTORY + 'index.html', 'w') as f:
            f.write(resp.content) 
        
        print 'Done'


    def _get_all_posts(self, new = False):    
        posts = []
        for item in os.listdir(STATICBLOG_POST_DIRECTORY):
            post = self._create_post(item, new)
            if post:
                posts.append(post)
        return posts

    def _get_named_posts(self, post):
        post_list = post.split(',')
        posts = []
        for item in post_list:
            try:
                with open(STATICBLOG_POST_DIRECTORY + item, 'r') as f: 
                    post = self._create_post(item)
                    if post:
                        posts.append(post)
            except IOError as e:
                print >> sys.stderr, '\033[01;31m' + str(e) + '\033[0m'
        return posts

    def _create_post(self, item, new = False):
        outdir = STATICBLOG_POST_DIRECTORY
        compiled_post = {
            'md_name' : item,
            'html_name' : '',
            'path' : '',
            'html' : '',
        }
        if item.endswith('.post'):
            compiled_post['path'] = item.replace('.post', '')
            compiled_post['html_name'] = compiled_post['path'] + '/index.html'
            if new:
                try:
                    with open(outdir + compiled_post['html_name'], 'r') as f: 
                        return False
                except IOError as e:
                    return compiled_post
            else:
                return compiled_post   
