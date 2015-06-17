from tree.TreeNode import TreeNode, JSONTreeMixin
from random import randrange

import logging
logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.DEBUG)
logger = logging.getLogger()


class CacheTree(TreeNode, JSONTreeMixin):

    def __init__(self, root=None):
        TreeNode.__init__(self)
        self.nodes = []
        self.roots = []
        self.root = root
        self.nodes_edit = []
        self.nodes_delete = []
        self.nodes_add = []

    def cache_node(self, parent_key, key, value):
        logger.debug('Caching node: key={}, value={}, parent_key={}.'.format(key, value, parent_key))
        if self.get_node_by_key(key) is not None:
            logger.debug('Such element is already in the cache nodes list.')
            return

        cached_node = TreeNode(key, value)
        parent_node = None

        if parent_key:
            parent_node = self.get_node_by_key(parent_key)
            cached_node.set_parent(parent_key)

        if parent_node:
            logger.debug('Parent node "{}" was found.'.format(parent_node.value))
            """if not parent_node.marked_as_del:
                parent_node.add_child(cached_node)
            else:
                logger.debug('Parent node "{}" is marked to be deleted, will ignore the request.'.format(parent_node.value))
                return"""
            parent_node.add_child(cached_node)
        else:
            logger.debug('Parent node was not found.')
            self.roots.append(cached_node)

        self.nodes.append(cached_node)
        self._link_by_parent(cached_node)

    def _link_by_parent(self, parent_node):
        roots_to_remove = []
        logger.debug('Link process called for node: key={}, value={}, parent={}'.format(parent_node.key, parent_node.value, parent_node.parent))
        if len(self.nodes) < 2:
            return

        for r in self.roots:
            logger.debug('Looping through the root list, "{}" node is processed.'.format(r.value))
            if r.parent is None:
                logger.debug('Parent is not specified.')
                # According to the initial conditions there should be the only one root with no parent specified.
                self.root = r
                # self.roots.remove(r)
            else:
                logger.debug('Parent ref: {}.'.format(r.parent))
                if r.parent == parent_node.key:
                    # parent_node.add_child(r)
                    roots_to_remove.append(r)
                    # self.roots.remove(r)

        for rem in roots_to_remove:
            self.roots.remove(rem)

        for n in self.nodes:
            if n.parent is not None and n.parent == parent_node.key:
                parent_node.add_child(n)

        self._validate_tree()

    def _validate_tree(self):
        for n in self.nodes:
            if n.marked_as_del:
                n.mark_subtree_as_deleted()

    def add_node(self, parent_key, value):
        logger.debug('Add node: parent_key={}, value={}.'.format(parent_key, value))
        parent_node = self.get_node_by_key(parent_key)
        if parent_node is None:
            logger.debug('Parent node (key={}) was not found in the cache nodes list.'.format(parent_key))
            return

        if parent_node.marked_as_del:
            logger.debug('Parent node (key={}) is marked as deleted, will ignore the request.'.format(parent_key))
            return

        # It's not good, but may be accepted as a temporary test solution
        new_node = TreeNode(randrange(1000000), value, parent_key)
        parent_node.add_child(new_node)
        self.nodes.append(new_node)
        new_node.mark_as_new()
        self.nodes_add.append(new_node)

    def edit_node(self, key, value):
        node = self.get_node_by_key(key)
        if node is None:
            logger.error('There is no node for the specified key value: {}'.format(key))
            return

        if node.marked_as_del:
            logger.debug('Node "{}" is marked as deleted, will ignore the request.'.format(node.value))
            return

        node.mark_as_edit()
        self.nodes_edit.append(node)
        node.set_value(value)

    def del_node(self, key):
        node = self.get_node_by_key(key)
        if node is None:
            logger.error('There is no node for the specified key value: {}'.format(key))
            return

        if node.marked_as_del:
            logger.debug('Node "{}" is marked as deleted, will ignore the request.'.format(node.value))
            return

        self.nodes_delete.append(node)
        node.mark_subtree_as_deleted()

    def get_node_by_key(self, key):
        for n in self.nodes:
            if n.key == key:
                return n

    def save(self, db_tree):
        for n in self.nodes_delete:
            db_tree.del_node(n.key)

        self.nodes_delete = []

        self._validate_tree()

        for n in self.nodes_add:
            # Fixing the problem of inserting childs for their deleted parents
            res = db_tree.add_node(n.key, n.value, n.parent)
            if res == 0:
                n.unmark_as_new()
            elif res == 3:
                parent_node = self.get_node_by_key(n.parent)
                parent_node.mark_subtree_as_deleted()

        self.nodes_add = []

        for n in self.nodes_edit:
            # Fixing the problem of editing childs for their deleted parents
            res = db_tree.edit_node(n.key, n.value)
            if res == 0:
                n.unmark_as_edit()
            elif res == 3:
                parent_node = self.get_node_by_key(n.parent)
                parent_node.mark_subtree_as_deleted()

        self.nodes_edit = []

        self._validate_tree()

    def show(self):
        self.show_container = []
        self._show_tree(self.root)

    def _show_tree(self, cur_node):
        if cur_node == self.root:
            self.show_container.append(self.root.value)
        else:
            self.show_container.append('--')
            self.show_container.append(cur_node.value)
            print ''.join(self.show_container)
            self.show_container.pop()
            self.show_container.pop()

        if cur_node and cur_node.get_children():
            self.show_container.append('   |')
            print ''.join(self.show_container)

        for c in cur_node.get_children():
            self._show_tree(c)

        if cur_node.get_children() and self.show_container:
            self.show_container.pop()

    def to_json(self):
        self._json = '['
        for r in self.roots:
            self._json += '{' + r.json_params
            self._tree_walk(r)

        self._json = self._json.rstrip(',')
        self._json += ']'

        logger.debug(self._json)
        return self._json
