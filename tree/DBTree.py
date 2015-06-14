from tree.TreeNode import TreeNode, JSONTreeMixin

import logging
logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.DEBUG)
logger = logging.getLogger()


class DBTree(TreeNode, JSONTreeMixin):

    def __init__(self, root=None):
        TreeNode.__init__(self)
        self.nodes = []
        self.root = root
        self.__dict = []

    def build_tree_from_qs(self, query_set):
        logger.debug('Building tree from the inbound query set data.')
        logger.debug('Initial query_set data: {}'.format(query_set))
        self.root = None
        self.nodes = []
        for qs_entry in query_set:
            self._qs_add_node(qs_entry)

    def add_node(self, key, value, parent_key):
        tmp_node = self._get_node_by_entry_key(key)
        if tmp_node is not None:
            return tmp_node
        else:
            parent_node = self._get_node_by_entry_key(parent_key)

            if parent_node is None:
                logger.error('An attempt to add new node (key={}, value={}) has been failed: parent \
                                    reference is not specified for the given node.'.format(key, value))
                return None

            new_node = TreeNode(key, value, parent_key)
            self.nodes.append(new_node)
            parent_node.add_child(new_node)
            return new_node

    # This method is used to recursively go through the path for each TreeNode item and build a tree
    def add_nodes_subtree(self, node_obj):
        if node_obj is not None:
            logger.debug('Processing "{}" entry.'.format(node_obj.value))
            tree_node = self._get_node_by_entry_key(node_obj.key)
            if tree_node is not None:
                return tree_node
            else:
                parent = node_obj.parent

                if parent is None:
                    logger.error('An attempt to add new node "{}" has been failed: parent \
                                    reference is not specified for the given node.'.format(node_obj.value))
                    return None
                else:
                    parent_node = self._get_node_by_entry_key(node_obj.parent.key)
                    if parent_node is None:
                        logger.debug('Node "{}" parent referecne({}) was not found in the node list.\
                                    Going to insert it.'.format(node_obj.value, parent.value))
                        parent_node = self.add_node(parent)

                    if parent_node is not None:
                        parent_node.add_child(node_obj)
                        self.nodes.append(node_obj)
                        return node_obj

    def edit_node(self, key, value):
        node = self._get_node_by_entry_key(key)
        if node is None:
            logger.error('There is no node for the specified key value: {}'.format(key))
            return

        if node.value == value:
            logger.info('There is no need to update, node "{}" already has value = {}.'.format(node.value, value))
            return

        node.set_value(value)

    def del_node(self, key):
        node = self._get_node_by_entry_key(key)
        logger.debug('Going to delete "{}" node.'.format(node.value))
        if node is None:
            logger.error('There is no node for the specified key value: {}'.format(key))
            return

        if node.marked_as_del:
            logger.debug('Node "{}" is marked as deleted already, will ignore the request.'.format(node.value))
            return

        node.mark_subtree_as_deleted()

    # This method is used to recursively go through the path for each queryset item and build a tree
    def _qs_add_node(self, entry_obj):
        logger.debug('Processing {} entry.'.format(entry_obj))
        tmp_node = self._get_node_by_entry_key(entry_obj.id)
        if tmp_node is not None:
            return tmp_node
        else:
            qs_parent = entry_obj.parent_ref

            if qs_parent is None:
                # root has no parents
                root_node = TreeNode(entry_obj.id, entry_obj.value)
                self.root = root_node
                self.nodes.append(root_node)
                return root_node
            else:
                parent_node = self._qs_add_node(qs_parent)

            if parent_node is not None:
                new_node = TreeNode(entry_obj.id, entry_obj.value)
                new_node.set_parent(parent_node)
                parent_node.add_child(new_node)
                self.nodes.append(new_node)
                return new_node

    def _get_node_by_entry_key(self, key):
        for node in self.nodes:
            if node.key == key:
                return node

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
        self._json = '[{' + self.root.json_params

        self._tree_walk(self.root)
        self._json = self._json.rstrip(',')
        self._json += ']'
        logger.debug(self._json)
        return self._json