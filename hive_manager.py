__author__ = 'gru'


from Registry import Registry
from subkey_processor import ProcessorFactory


class HiveManager:

    def __init__(self, f):
        self.file = open(f, "rb")
        self.registry = Registry.Registry(f)
        self.root = (self.registry.root())

    def retrieve(self, key_str, is_bare, is_raw):
        node = self.find_key([self.root], key_str)
        data = self.extract_values(node)
        proc = ProcessorFactory.get_processor(key_str, data)

        return proc.process_content(is_bare, is_raw)

    @classmethod
    def extract_values(cls, key):
        leafs = []
        cls.get_leafs(key, leafs)

        values = {}

        # Add values of top node
        if len(key.values()) > 0:
            vls = key.values()
            vls.sort(key=lambda x: x.name(), reverse=False)
            values[key] = vls

        # Add values of subnodes
        for l in leafs:
            if len(l.values()) > 0:
                entries = l.values()
                entries.sort(key=lambda x: x.name(), reverse=False)
                values[l] = entries
                #values[l] = l.values()

        return values


    @classmethod
    def get_leafs(cls, node, leafs_to_populate):

        for n in node.subkeys():
            if len(n.subkeys()) == 0:
                leafs_to_populate.append(n)
            else:
                cls.get_leafs(n, leafs_to_populate)

    @classmethod
    def get_tree_recursive(cls, node, node_list, print_branch=False):
        for sub in node.subkeys():
            if print_branch:
                node_list.append(str(sub))
            else:
                node_list.append(sub.name())

            if len(sub.subkeys()) > 0:
                cls.get_tree_recursive(sub, node_list, print_branch)

    @classmethod
    def get_tree_structure(cls, k, print_branch=False):
        node_list = []
        cls.get_tree_recursive(k, node_list, print_branch)
        node_list_as_str = '\n'.join(node_list)

        return node_list_as_str

    # level order tree traversal
    @classmethod
    def find_key(cls, nodes, key):

        if len(nodes) == 0:
            return None

        new_nodes = []

        for n in nodes:
            if key == n.name():
                return n
            else:
                new_nodes += n.subkeys()

        return cls.find_key(new_nodes, key)

    @classmethod
    def search_key(cls, nodes, key):

        if len(nodes) == 0:
            return None
        new_nodes = []

        for n in nodes:
            if key in n.name():
                return n
            else:
                new_nodes += n.subkeys()

        return cls.search_key(new_nodes, key)

    @classmethod
    def in_order(cls, node, key, re):
        if node.name() == key:
            re.append(node)

        for sub in node.subkeys():
            cls.in_order(sub, key, re)

    @classmethod
    def find_key_pre_order(cls, node, key):
        if node.name() == key:
            return node

        match = None
        sks = node.subkeys()
        for s in sks:
            if match is None:
                match = HiveManager.find_key_pre_order(s, key)

        return match