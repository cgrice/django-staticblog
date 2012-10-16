from django.conf.urls import patterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('staticblog.views',
    (r'^$', 'archive'),
    (r'^([\-\w]+)$', 'render_post'),
    (r'^git/receive', 'handle_hook'),
)
