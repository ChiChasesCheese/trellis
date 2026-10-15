"""LC 138 Copy List with Random Pointer -- old->new hash map (O(n) space) or interleaving (O(1) space)."""


class Node:
    def __init__(self, x, next=None, random=None):
        self.val = x
        self.next = next
        self.random = random


def build(pairs):
    """pairs = [(val, random_index_or_None), ...]"""
    nodes = [Node(v) for v, _ in pairs]
    for i, (_, r) in enumerate(pairs):
        if i + 1 < len(nodes):
            nodes[i].next = nodes[i + 1]
        if r is not None:
            nodes[i].random = nodes[r]
    return nodes[0] if nodes else None


def dump(head):
    nodes, cur = [], head
    while cur:
        nodes.append(cur)
        cur = cur.next
    index = {id(n): i for i, n in enumerate(nodes)}
    return [(n.val, index[id(n.random)] if n.random else None) for n in nodes], nodes

# --- solution ---
def copy_random_list(head):
    clone = {None: None}                    # old node -> new node; None maps to None
    cur = head
    while cur:                              # pass 1: create all copies
        clone[cur] = Node(cur.val)
        cur = cur.next
    cur = head
    while cur:                              # pass 2: wire next/random through the map
        clone[cur].next = clone[cur.next]
        clone[cur].random = clone[cur.random]
        cur = cur.next
    return clone[head]


def copy_random_list_o1(head):
    if not head:
        return None
    cur = head
    while cur:                              # A -> A' -> B -> B' ...
        cur.next = Node(cur.val, cur.next)
        cur = cur.next.next
    cur = head
    while cur:                              # A'.random = A.random' (the node right after A.random)
        if cur.random:
            cur.next.random = cur.random.next
        cur = cur.next.next
    new_head = head.next
    cur = head
    while cur:                              # unzip the two lists, restoring the original
        copy = cur.next
        cur.next = copy.next
        copy.next = copy.next.next if copy.next else None
        cur = cur.next
    return new_head
# --- end ---

if __name__ == "__main__":
    spec = [(7, None), (13, 0), (11, 4), (10, 2), (1, 0)]
    for f in (copy_random_list, copy_random_list_o1):
        head = build(spec)
        _, old_nodes = dump(head)
        new = f(head)
        shape, new_nodes = dump(new)
        assert shape == spec
        assert all(n not in old_nodes for n in new_nodes)       # deep copy: no shared nodes
        assert dump(head)[0] == spec                            # original untouched
        assert f(None) is None
    print("ok 138_copy_list_with_random_pointer")
