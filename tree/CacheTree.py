from tree.TreeNode import TreeNode, JSONTreeMixin
from random import randrange

import logging
logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.DEBUG)
logger = logging.getLogger()


class CacheTree(TreeNode, JSONTreeMixin):

    def __init__(self, root=None):
        TreeNode.__init__(self)
        self.nodes = []
        self.root = root
        self.nodes_edit = []
        self.nodes_delete = []
        self.nodes_add = []

    def cache_node(self, parent_key, key, value):
        if self._get_node_by_key(key) is not None:
            logger.debug('Such element is already in the cache nodes list.')
            return

        parent_node = self._get_node_by_key(parent_key)
        cached_node = TreeNode(key, value)

        if parent_node is not None:
            logger.debug('Parent node "{}" was found.'.format(parent_node.value))
            cached_node.set_parent(parent_node)
            parent_node.add_child(cached_node)
        else:
            logger.debug('Cache node "{}" is not linked yet.'.format(cached_node.value))

        self.nodes.append(cached_node)
        self._link_by_parent(cached_node)

    def _link_by_parent(self, parent_node):
        if len(self.nodes) < 2:
            return

        for n in self.nodes:
            # TODO: change to if n.parent == parent_node.key
            if n.parent is not None:
                # Assume this is the root otherwise
                if n.parent.key == parent_node.key:
                    parent_node.set_child(n)

    def add_node(self, parent_key, value):
        parent_node = self._get_node_by_key(parent_key)
        if parent_node is None:
            logger.debug('Parent node (key={}) was not found in the cache nodes list.'.format(parent_key))
            return

        if parent_node.marked_as_del:
            logger.debug('Parent node (key={}) is marked as deleted, will ignore the request.'.format(parent_key))
            return

        new_node = TreeNode(randrange(1000000), value, parent_node)
        parent_node.add_child(new_node)
        self.nodes.append(new_node)
        self.nodes_add.append(new_node)

    """def add_node(self, parent_key, value):
        parent_node = self._get_node_by_key(parent_key)
        if parent_node is None:
            logger.debug('Parent node (key={}) was not found in the cache nodes list.'.format(parent_key))
            return

        if parent_node.marked_as_del:
            logger.debug('Parent node (key={}) is marked as deleted, will ignore the request.'.format(parent_key))
            return

        new_node = TreeNode(randrange(1000000), value, parent_key)
        parent_node.add_child(new_node)
        self.nodes.append(new_node)
        self.nodes_add.append(new_node)"""

    def edit_node(self, key, value):
        node = self._get_node_by_key(key)
        if node is None:
            logger.error('There is no node for the specified key value: {}'.format(key))
            return

        if node.marked_as_del:
            logger.debug('Node "{}" is marked as deleted, will ignore the request.'.format(node.value))
            return

        self.nodes_edit.append(node)
        node.set_value(value)

    def del_node(self, key):
        node = self._get_node_by_key(key)
        if node is None:
            logger.error('There is no node for the specified key value: {}'.format(key))
            return

        if node.marked_as_del:
            logger.debug('Node "{}" is marked as deleted, will ignore the request.'.format(node.value))
            return

        self.nodes_delete.append(node)
        node.mark_subtree_as_deleted()

    def _get_node_by_key(self, key):
        for n in self.nodes:
            if n.key == key:
                return n

    def save(self, db_tree):
        for n in self.nodes_add:
            db_tree.add_node(n.key, n.value, n.parent.key)

        self.nodes_add = []

        for n in self.nodes_edit:
            db_tree.edit_node(n.key, n.value)

        self.nodes_edit = []

        for n in self.nodes_delete:
            db_tree.del_node(n.key)

        self.nodes_delete = []

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
