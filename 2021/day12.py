from dataclasses import dataclass, field

START = 0
END = 1
LARGE = 2
SMALL = 3

paths = 0

@dataclass
class Node:
    name: str
    ntype: int
    visited = False
    connections: list = field(default_factory=list)

nodes = {}

def find_path(node, twice, twice_node=None):
    node.visited = True
    if node.ntype == END:
        global paths
        paths += 1
        return
    for connection in node.connections:
        if connection.ntype == START:
            continue
        elif connection.ntype == SMALL and twice and connection.visited:
            continue
        if connection.ntype == SMALL and connection.visited:
            find_path(connection, True, connection)
        else:
            find_path(connection, twice, twice_node)
    if not (node is twice_node and twice):
        node.visited = False

with open('day12.txt', 'r') as f:
    for line in f:
        nodenames = line.strip().split('-')
        for nodename in nodenames:
            if nodename not in nodes:
                if nodename == 'start':
                    tp = START
                elif nodename == 'end':
                    tp = END
                elif nodename.isupper():
                    tp = LARGE
                else:
                    tp = SMALL
                nodes[nodename] = Node(nodename, tp)
        nodes[nodenames[0]].connections.append(nodes[nodenames[1]])
        nodes[nodenames[1]].connections.append(nodes[nodenames[0]])
    find_path(nodes['start'], False)
print(paths)