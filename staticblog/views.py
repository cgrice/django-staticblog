# Django imports
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.files.storage import get_storage_class
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt


def render_response(req, *args, **kwargs):
    """Shortcut to wrap request in RequestContext"""
    kwargs['context_instance'] = RequestContext(req)
    return render_to_response(*args, **kwargs)

# stdlib
import os
import sys
import urllib2
import hashlib

# 3rd party
import markdown
from markdown.inlinepatterns import ImagePattern, IMAGE_LINK_RE

# app
from staticblog.app_settings import STATICBLOG_COMPILE_DIRECTORY, \
                                    STATICBLOG_POST_DIRECTORY, \
                                    STATICBLOG_STORAGE

class S3ImagePattern(ImagePattern):
    """ Wrapper class to handle image matches in markdown document """

    def handleMatch(self, match):
        node = ImagePattern.handleMatch(self, match)
        # check 'src' to ensure it is local
        src = node.attrib.get('src')
        storage_class = get_storage_class(STATICBLOG_STORAGE)
        storage = storage_class()
    
        # otherwise we need to do some downloading!
        if 'http://' in src or 'https://' in src:
            img_data = urllib2.urlopen(src).read()
            md5 = hashlib.md5()
            md5.update(img_data)
            name = md5.hexdigest() + '/' + os.path.basename(src)
        else:
            with open(STATICBLOG_POST_DIRECTORY + src, 'r') as fhandle:
                img_data = fhandle.read()
            name = src
        
        print >> sys.stderr, 'Uploading ' + src
        try:
            storage.save(name, ContentFile(img_data))
            node.attrib['src'] = storage.url(name)
            print >> sys.stderr, 'Uploaded ' + src + ' to ' + storage.url(name)
        except Exception as e:
            print >> sys.stderr, str(e)
            print >> sys.stderr, '\033[01;31mUpload of %s failed\033[0m' % src
        return node




def render_post(request, post_name):
    """ Render a blog post based on a .post template

    The used template is rendered as html in the folder defined
    by STATICBLOG_COMPILE_DIRECTORY
    """

    content = ""
    mdown = markdown.Markdown(extensions = ['meta',])
    mdown.inlinePatterns['image_link'] = S3ImagePattern(IMAGE_LINK_RE, mdown)
    try:
        post_filename = STATICBLOG_POST_DIRECTORY + post_name + '.post'
        with open(post_filename, 'r') as fhandle:
            content = fhandle.read()
            html = mdown.convert(content.decode('UTF-8'))  
    except IOError as e:
        print str(e)
        with open(STATICBLOG_POST_DIRECTORY + post_name + '.preview', 'r') as f:
            content = f.read()
            html = mdown.convert(content)

    post = {
        'content' : html ,
    }

    try:
        post['date'] = mdown.Meta['date'][0]
        post['title'] = mdown.Meta['title'][0]
        post['author'] = mdown.Meta['author'][0]
        post['summary'] = mdown.Meta['summary'][0]
    except:
        pass

    meta = {}
    if 'title' in post: 
        meta['title'] = post['title']

    return render_response(
        request, 
        'staticblog/post.html', 
        {'post' : post, 'meta' : meta}
    )

def archive(request):
    mdown = markdown.Markdown(extensions = ['meta',])
    posts = []
    import string
    for item in os.listdir(STATICBLOG_COMPILE_DIRECTORY):       
        if item.endswith('.post'):
            continue
        try:
            with open(STATICBLOG_POST_DIRECTORY + item + '.post') as fhandle:
                content = fhandle.read()
                mdown.convert(content.decode('UTF-8'))  
                post = {
                    'name' : item,
                }
                if 'title' in mdown.Meta and len(mdown.Meta['title'][0]) > 0:
                    post['title'] = mdown.Meta['title'][0]
                else:
                    post['title'] = string.capwords(item.replace('-', ' '))
                if 'date' in mdown.Meta:
                    post['date'] = mdown.Meta['date'][0]

                posts.append(post)
        except:
            pass

    from operator import itemgetter
    posts = sorted(posts, key=itemgetter('date'))     
    posts.reverse()
    return render_response(
        request, 
        'staticblog/archive.html', 
        {'posts' : posts}
    )

@csrf_exempt
def handle_hook(request):
    from django.http import HttpResponse
    from django.core.management import call_command
    result = call_command('update_blog', verbosity = 0)
    return HttpResponse(result)
            
