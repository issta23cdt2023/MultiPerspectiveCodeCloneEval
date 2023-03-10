import os
import javalang
from javalang.ast import Node


def _name(node):
    return type(node).__name__


def get_token(node):
    token = ''
    if isinstance(node, str):
        token = node
    elif isinstance(node, set):
        token = 'Modifier'
    elif isinstance(node, Node):
        token = node.__class__.__name__
    return token


def dfsSearch1(children):
    if not isinstance(children, (str, Node, list, tuple)):
        return
    if isinstance(children, (str, Node)):
        if str(children) == '':
            return
        # ss = str(children)
        if str(children).startswith('"'):
            return
        if str(children).startswith("'"):
            return
        if str(children).startswith("/*"):
            return
        global num_nodes
        num_nodes += 1
        listt1.append(children)
        return
    for child in children:
        if isinstance(child, (str, Node, list, tuple)):
            dfsSearch1(child)


def _traverse_tree(root):
    global num_nodes
    num_nodes = 1
    queue = [root]
    root_json = {
        "node": _name(root),

        "children": []
    }
    queue_json = [root_json]
    while queue:
        current_node = queue.pop(0)
        current_node_json = queue_json.pop(0)

        global listt
        global listt1
        listt1 = []
        dfsSearch1(current_node.children)
        children = listt1
        for child in children:
            child_json = {
                "node": get_token(child),
                "children": []
            }

            current_node_json['children'].append(child_json)
            if isinstance(child, (Node)):
                queue_json.append(child_json)
                queue.append(child)
    return root_json, num_nodes


numnodes = 0


def dfsDict(root):
    global listtfinal
    listtfinal.append(str(root['node']))
    global numnodes
    numnodes += 1
    if len(root['children']):
        pass
    else:
        return
    for dictt in root['children']:
        dfsDict(dictt)


f = open("sentenceBCBwithid.txt", 'w')
listfile = os.listdir("../dataset/cbcb/funcs/")
# print(listfile)
lisfinalfile = []
ff = open("flistBCB.txt", 'w')
for lis in listfile:
    ff.write("../dataset/cbcb/funcs/" + lis)
    ff.write('\t')
    lisfinalfile.append("../dataset/cbcb/funcs/" + lis)
# print(lisfinalfile)
ff.close()

z = 0
for l in lisfinalfile:
    if not os.path.exists(l):
        continue
    ff = open(l, 'r')
    z += 1
    content = ff.read()
    print(l)
    tree = javalang.parse.parse(content)
    sample, size = _traverse_tree(tree)
    listtfinal = []
    dfsDict(sample)
    for lisf in listtfinal:
        f.write(lisf)
        f.write(" ")
    f.write("\n")
f.close()
