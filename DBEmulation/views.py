from django.http import HttpResponse
from tree.DBTree import DBTree
from tree.CacheTree import CacheTree
from DBEmulation.models import Entry
from django.template import loader
from django.views.decorators.csrf import csrf_exempt


class HttpResponseBadRequest(HttpResponse):
    status_code = 400


def init_db():
    global db_tree, cache_tree
    db_tree = DBTree()
    cache_tree = CacheTree()
    db_tree.build_tree_from_qs(Entry.objects.all())


init_db()


def db_tree_view(request):
    return HttpResponse(db_tree.to_json())


def cache_tree_view(request):
    return HttpResponse(cache_tree.to_json())


def index_view(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}))


@csrf_exempt
def reset(request):
    if request.method == 'POST':
        init_db()

    return HttpResponse()


@csrf_exempt
def cache_node(request):
    if request.method == 'POST':
        db_node_id = request.POST.get('id')
        if db_node_id:
            db_node = db_tree.get_node_by_entry_key(int(db_node_id))
        else:
            return HttpResponseBadRequest('DB node id was not passed.')

        cache_tree.cache_node(db_node.parent, db_node.key, db_node.value)
        print db_node.value
    return HttpResponse()


@csrf_exempt
def add_node(request):
    if request.method == 'POST':
        cache_node_id = request.POST.get('id')
        cache_node_value = request.POST.get('value')
        if not cache_node_id:
            return HttpResponseBadRequest('Cache node id was not passed.')

        if not cache_node_value:
            return HttpResponseBadRequest('Cache node new value was not passed.')

        cache_tree.add_node(int(cache_node_id), cache_node_value)
    return HttpResponse()


@csrf_exempt
def edit_node(request):
    if request.method == 'POST':
        cache_node_id = request.POST.get('id')
        cache_node_value = request.POST.get('value')
        if not cache_node_id:
            return HttpResponseBadRequest('Cache node id was not passed.')

        if not cache_node_value:
            return HttpResponseBadRequest('Cache node new value was not passed.')

        cache_tree.edit_node(int(cache_node_id), cache_node_value)
    return HttpResponse()


@csrf_exempt
def delete_node(request):
    if request.method == 'POST':
        cache_node_id = request.POST.get('id')
        if not cache_node_id:
            return HttpResponseBadRequest('Cache node id was not passed.')

        cache_tree.del_node(int(cache_node_id))
    return HttpResponse()


@csrf_exempt
def save_changes(request):
    if request.method == 'POST':
        cache_tree.save(db_tree)
    return HttpResponse()
