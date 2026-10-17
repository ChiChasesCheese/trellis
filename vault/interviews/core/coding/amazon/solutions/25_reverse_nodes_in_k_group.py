"""LC 25 Reverse Nodes in k-Group -- reverse each full block of k in place. Time O(n), space O(1)."""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build(values):
    dummy = tail = ListNode()
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out

# --- solution ---
def reverse_k_group(head, k):
    dummy = ListNode(0, head)
    group_prev = dummy                         # node just before the current block
    while True:
        kth = group_prev
        for _ in range(k):                     # find the k-th node of the block, or stop if short
            kth = kth.next
            if not kth:
                return dummy.next
        group_next = kth.next                  # first node after the block
        prev, cur = group_next, group_prev.next
        while cur is not group_next:           # reverse the block; its tail ends up pointing at group_next
            cur.next, prev, cur = prev, cur, cur.next
        block_tail = group_prev.next           # old first node is now the block's tail
        group_prev.next = kth                  # kth is the new block head
        group_prev = block_tail
# --- end ---

if __name__ == "__main__":
    assert to_list(reverse_k_group(build([1, 2, 3, 4, 5]), 2)) == [2, 1, 4, 3, 5]
    assert to_list(reverse_k_group(build([1, 2, 3, 4, 5]), 3)) == [3, 2, 1, 4, 5]   # tail < k stays
    assert to_list(reverse_k_group(build([1, 2, 3]), 1)) == [1, 2, 3]
    assert to_list(reverse_k_group(build([1, 2, 3, 4]), 4)) == [4, 3, 2, 1]
    assert to_list(reverse_k_group(build([1]), 2)) == [1]
    assert to_list(reverse_k_group(build([]), 3)) == []
    print("ok 25_reverse_nodes_in_k_group")
