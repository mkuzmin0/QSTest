from django.conf.urls import include, url
from django.contrib import admin
from DBEmulation.views import db_tree_view, index
import os

site_media = os.path.join(
	os.path.dirname(__file__), 'site_media'
)

urlpatterns = [
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': site_media}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^db_tree/$', db_tree_view),
    url(r'^$', index),
]
