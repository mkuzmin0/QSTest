class TreeNode(object):

    def __init__(self, key=None, value=None, parent=None, marked_as_del=False, marked_as_edited=False, marked_as_new=False):
        self.__key = key
        self.__value = value
        self.__parent = parent
        self.__marked_as_del = marked_as_del
        self.__marked_as_edited = marked_as_edited
        self.__marked_as_new = marked_as_new
        self.__children = []
        self._json = {}

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

    @property
    def marked_as_edited(self):
        return self.__marked_as_edited

    @property
    def marked_as_new(self):
        return self.__marked_as_new

    def get_children(self):
        return self.__children

    def add_child(self, obj):
        self.__children.append(obj)

    def set_parent(self, parent):
        self.__parent = parent

    def mark_as_del(self):
        self.__marked_as_del = True

    def mark_as_edit(self):
        self.__marked_as_edited = True

    def mark_as_new(self):
        self.__marked_as_new = True

    def unmark_as_edit(self):
        self.__marked_as_edited = False

    def unmark_as_new(self):
        self.__marked_as_new = False

    def set_value(self, value):
        self.__value = value

    # This method is used to recursively mark a subtree for the given node as deleted.
    def mark_subtree_as_deleted(self):
        if not self.marked_as_del:
            self.mark_as_del()

        l = len(self.get_children())
        if l > 0:
            for child in self.get_children():
                child.mark_subtree_as_deleted()

    def __unicode__(self):
        return self.__value

    @property
    def json_params(self):
        json_str = '"id": "{id}", "text": "{text}", '.format(id=self.key, text=self.value) + \
            '"state": {"expanded": true}'
        if self.marked_as_del:
            json_str += ', "color": "#F51616"'
            json_str += ', "backColor": "E8E8E8"'
            json_str += ', "selectable": false'
        elif self.marked_as_edited:
            json_str += ', "color": "F7C707"'
        elif self.marked_as_new:
            json_str += ', "color": "07F7A3"'

        return json_str


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
