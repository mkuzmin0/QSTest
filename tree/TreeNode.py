class TreeNode(object):

    def __init__(self, key=None, value=None, parent=None, marked_as_del=False):
        self.__key = key
        self.__value = value
        self.__parent = parent
        self.__marked_as_del = marked_as_del
        self.__children = []
        self._json = {}
    """def __init__(self, key=None, value=None, parent_key=None, marked_as_del=False):
        self.__key = key
        self.__value = value
        self.__parent = parent_key
        self.__marked_as_del = marked_as_del
        self.__children = []"""

    @property
    def key(self):
        return self.__key

    @property
    def value(self):
        return self.__value

    @property
    def parent(self):
        return self.__parent

    @property
    def marked_as_del(self):
        return self.__marked_as_del

    def get_children(self):
        return self.__children

    def add_child(self, obj):
        self.__children.append(obj)

    def set_parent(self, parent):
        self.__parent = parent

    def mark_as_del(self):
        self.__marked_as_del = True

    def set_value(self, value):
        self.__value = value

    def append_dict_for_child(self, child):
        self._json['nodes']

    def add_node_dict(self):
        self._json['id'] = self.key
        self._json['text'] = self.value
        self._json['nodes'] = []

    # This method is used to recursively mark a subtree for the given node as deleted.
    def mark_subtree_as_deleted(self):
        self.mark_as_del()
        l = len(self.get_children())
        if l > 0:
            for child in self.get_children():
                child.mark_subtree_as_deleted()

    def __unicode__(self):
        return self.__value

    @property
    def json_params(self):
        return '"id": "{id}", "text": "{text}", '.format(id=self.key, text=self.value) + \
            '"state": {"expanded": true}'


class JSONTreeMixin(object):
    def _tree_walk(self, node):
        if node:
            children = node.get_children()
            if children:
                self._json += ', "nodes": ['
                for c in node.get_children():
                    self._json += '{' + c.json_params
                    self._tree_walk(c)

                self._json = self._json.rstrip(',')
                self._json += ']'
            self._json += '},'
