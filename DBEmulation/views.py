from django.http import HttpResponse
from tree.DBTree import DBTree
from tree.CacheTree import CacheTree
from DBEmulation.models import Entry
from django.template import loader

db_tree = DBTree()
cache_tree = CacheTree()
qs = Entry.objects.all()
db_tree.build_tree_from_qs(qs)

def db_tree_view(request):
    return HttpResponse(db_tree.to_json())

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}))
