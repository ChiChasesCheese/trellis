"""LC 206 Reverse Linked List -- three pointers, rewire next in place. Time O(n), space O(1)."""


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
def reverse_list(head):
    prev = None
    cur = head
    while cur:
        nxt = cur.next        # 1. remember the rest before we cut the link
        cur.next = prev       # 2. point backwards
        prev = cur            # 3. advance prev
        cur = nxt             # 4. advance cur
    return prev               # prev is the new head when cur falls off the end


def reverse_list_recursive(head):
    if not head or not head.next:
        return head
    new_head = reverse_list_recursive(head.next)   # reverse the tail first
    head.next.next = head                          # the node after head now points back at head
    head.next = None
    return new_head
# --- end ---

if __name__ == "__main__":
    for f in (reverse_list, reverse_list_recursive):
        assert to_list(f(build([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]
        assert to_list(f(build([1, 2]))) == [2, 1]
        assert to_list(f(build([]))) == []
        assert to_list(f(build([7]))) == [7]
    print("ok 206_reverse_linked_list")
