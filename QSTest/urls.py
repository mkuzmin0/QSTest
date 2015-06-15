from django.conf.urls import include, url
from django.contrib import admin
from DBEmulation.views import db_tree_view, index_view, reset, cache_node, cache_tree_view, \
    add_node, edit_node, delete_node, save_changes
import os

site_media = os.path.join(
    os.path.dirname(__file__), 'site_media'
)

urlpatterns = [
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^db_tree/$', db_tree_view),
    url(r'^cache_tree/$', cache_tree_view),
    url(r'^cache_node/$', cache_node),
    url(r'^add/$', add_node),
    url(r'^edit/$', edit_node),
    url(r'^delete/$', delete_node),
    url(r'^save/$', save_changes),
    url(r'^db_reset/$', reset),
    url(r'^$', index_view),
]
