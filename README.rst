Django Static Blog
==================

django-staticblog is a
`markdown <http://daringfireball.net/projects/markdown>`_-based blog
system for `Django <https://www.djangoproject.com/>`_ that compiles to
static html.

Requirements
------------

django-staticblog requires:

-  Python 2.6+
-  Django 1.4+
-  markdown
-  html2text

Installation
------------

``pip install django-staticblog``

or

``python setup.py install``

after checking out the code from
http://github.com/cgrice/django-staticblog

Add ``staticblog`` to your ``INSTALLED_APPS`` setting, and add

::

    url(r'^preview/', include('staticblog.urls'))

to your ``urls.py``

Configuration Options
---------------------

``STATICBLOG_ROOT`` - root directory of your django project

``STATICBLOG_POST_DIRECTORY`` - full path to the directory which holds
your blog posts in markdown format. Defaults to your
``STATICBLOG_ROOT + '/posts'``

``STATICBLOG_COMPILE_DIRECTORY`` - full path to the directory which will
hold compiled post and archive html pages. Defaults to
``MEDIA_ROOT + '/posts'``

``STATICBLOG_STORAGE`` - Defines how ``staticblog`` stores images
defined in blog posts. Defaults to ``DEFAULT_FILE_STORAGE``.

Usage
-----

To start using ``staticblog``, write some posts in your
``STATICBLOG_POST_DIRECTORY``. These posts should be formatted in
`markdown <http://daringfireball.net/projects/markdown>`_. Post
filenames should contain alphanumeric characters and dashes only, and
end with ``.post``. For examples, please see the ``examples`` folder in
this repository.

Each post can also contain metadata used for title tags and post
information. For example:

::

    Title: Look, I'm blogging!
    Summary: A concise summary of a post
    Author: John Doe
    Date: 2009-08-05 11:25:53 GMT

You can include remotely hosted images in your posts - these will
automatically be downloaded and stored in the location defined by
``STATICBLOG_STORAGE``.

To include local files, create a folder with the same name as your post
file, minus the ``.post`` extension. You can then add image files to
this folder, and reference them in your markdown like so:

::

    ![Alt Text](post-name/image.jpg)

Compiling Posts
~~~~~~~~~~~~~~~

To display your posts, you need to compile them. To do this,
``staticblog`` provides a management command named ``update_blog``. By
defult, this command will process all new blog posts, handle their
images, and create a folder in your ``STATICBLOG_COMPILE_DIRECTORY``
with the post name, with an ``index.html`` file containing the blog
post.

``update_blog`` also creates a post listing, which it stores in an
``index.html`` file in your ``STATICBLOG_COMPILE_DIRECTORY``.

``update_blog`` takes two optional arguments:

``--all`` - process all blog posts regardless of whether they already
exist ``--name=POST,POST2`` - process a list of blog posts by post name

Templates
---------

``staticblog`` provides two default templates - ``staticblog/post.html``
and ``staticblog/archive.html``. You can overwrite these in your own
template directory to integrate the posts with your site.

Template Variables
~~~~~~~~~~~~~~~~~~

``staticblog/post.html``
^^^^^^^^^^^^^^^^^^^^^^^^

-  ``post`` : a dict containing:

   -  ``content`` : blog content in html format
   -  ``title``
   -  ``date``
   -  ``author``
   -  ``summary``

``staticblog/archive.html``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  ``posts`` : a list of ``post`` dicts as defined in ``post.html``
   above

Changelog
---------

0.2.4 - 2012-10-16
~~~~~~~~~~~~~~~~

* URL for rendering posts is no longer hardcoded to '/preview'
* Added view to handle github post-receives and render blog




