from django.http import HttpResponse
from tree.DBTree import DBTree
from tree.CacheTree import CacheTree
from DBEmulation.models import Entry
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

def init_db():
    global db_tree, cache_tree
    db_tree = DBTree()
    cache_tree = CacheTree()
    db_tree.build_tree_from_qs(Entry.objects.all())

init_db()

def db_tree_view(request):
    return HttpResponse(db_tree.to_json())

def cache_tree_view(request):
    return HttpResponse()

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}))

@csrf_exempt
def reset(request):
    if request.method == 'POST':
        init_db()
    return HttpResponse()

