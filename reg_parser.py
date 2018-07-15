__author__ = 'gru'


from io import StringIO
from Registry import Registry
import pprint

def print_tree_recursive(k, print_branch=False):
    for s in k.subkeys():
        if print_branch:
            print(s)
        else:
            print(s.name())

        if len(s.subkeys()) > 0:
            print_tree_recursive(s, print_branch)


# level order tree traversal
def find_key(nodes, key):

    if len(nodes) == 0:
        return None

    new_nodes = []

    for n in nodes:
        if key == n.name():
            return n
        else:
            new_nodes += n.subkeys()

    return find_key(new_nodes, key)


def get_leafs(node, leafs_to_populate):

    for n in node.subkeys():
        if len(n.subkeys()) == 0:
            leafs_to_populate.append(n)
        else:
            get_leafs(n, leafs_to_populate)

    return


def in_order(node, key, re):
    if node.name() == key:
        re.append(node)

    for sub in node.subkeys():
        in_order(sub, key, re)


def find_key_pre_order(node, key):
    if node.name() == key:
        return node

    match = None
    sks = node.subkeys()
    for s in sks:
        if match is None:
            match = find_key_pre_order(s, key)

    return match


def extract_values(key):
    leafs = []
    get_leafs(key, leafs)

    values = {}
    for l in leafs:
        if len(l.values()) > 0:
            values[l] = l.values()

    return values


# Cuts off, after first string
def convert_binary_data(data):
    data = data[::2]
    data = data[:data.find(b'\x00')]
    return data


def print_results(resultdict):
    for k in resultdict.keys():

        if resultdict[k][0].value_type() != Registry.RegNone:
            print("--------------------------")
            print(str(k))

        for v in resultdict[k]:
            if v.value_type() == Registry.RegNone:
                continue
            elif v.value_type() == Registry.RegBin:
                print("Datatype: " + v.value_type_str())
                print(convert_binary_data(v.value()))
            else:
                print(v.value())




f = open("Vibranium-NTUSER.DAT", "rb")
r = Registry.Registry(f)
root = (r.root())

# OpenSaveMRU
# RecentDocs
# LastVisitedMRU
# Explorer


# Extract ext->program links
node = find_key([root], "FileExts")
resultdict = extract_values(node)
print_results(resultdict)

# Extract recent documents
node = find_key_pre_order(root, "RecentDocs")
print_tree_recursive(node, print_branch=True)
resultdict = extract_values(node)
print_results(resultdict)


# Extract OpenSaveMRU
#node = find_key_pre_order(root, "RecentDocs")
#print_tree_recursive(node, print_branch=True)
#resultdict = extract_values(node)
#print_results(resultdict)