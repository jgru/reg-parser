__author__ = 'gru'


from io import StringIO
from Registry import Registry


def print_tree_recursive(k):
    for s in k.subkeys():
        print(s.name())
        if len(s.subkeys()) > 0:
            print_tree_recursive(s)


# level order tree traversal
def find_key(nodes, key, i):

    if len(nodes) == 0:
        return None

    new_nodes = []

    for n in nodes:
        if key == n.name():
            return n
        else:
            new_nodes += n.subkeys()

    return find_key(new_nodes, key, i)


def in_order(node, key, re):
    if node.name() == key:
        re.append(node)

    for sub in node.subkeys():
        in_order(sub, key, re)


def pre_order(node, key):
    if node.name() == key:
        return node

    match = None
    sks = node.subkeys()
    for s in sks:
        if match is None:
            match = pre_order(s, key)

    return match


def extract_values(key):
    return

f = open("Vibranium-NTUSER.DAT", "rb")
r = Registry.Registry(f)
root = (r.root())

fqkn = pre_order(root, "Winmm")
