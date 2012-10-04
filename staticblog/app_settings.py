from django.conf import settings
import os

STATICBLOG_ROOT = os.path.abspath(os.path.dirname(__name__))

STATICBLOG_POST_DIRECTORY = getattr(
    settings, 
    'STATICBLOG_POST_DIRECTORY', 
    STATICBLOG_ROOT + '/posts/'
)

STATICBLOG_COMPILE_DIRECTORY = getattr(
    settings, 
    'STATICBLOG_COMPILE_DIRECTORY', 
    settings.MEDIA_ROOT + 'posts/'
)

STATICBLOG_STORAGE = getattr(
    settings, 
    'STATICBLOG_STORAGE', 
    'django.core.files.storage.FileSystemStorage'
)
