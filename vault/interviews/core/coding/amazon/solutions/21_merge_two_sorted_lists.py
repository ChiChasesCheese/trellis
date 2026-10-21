"""LC 21 Merge Two Sorted Lists -- dummy head + two pointers. Time O(m+n), space O(1)."""


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
def merge_two_lists(a, b):
    dummy = tail = ListNode()              # dummy removes the "is the result empty yet?" special case
    while a and b:
        if a.val <= b.val:                 # <= keeps the merge stable (a's equal items first)
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b                     # splice whatever is left, no copying
    return dummy.next
# --- end ---

if __name__ == "__main__":
    assert to_list(merge_two_lists(build([1, 2, 4]), build([1, 3, 4]))) == [1, 1, 2, 3, 4, 4]
    assert to_list(merge_two_lists(build([]), build([]))) == []
    assert to_list(merge_two_lists(build([]), build([0]))) == [0]
    assert to_list(merge_two_lists(build([5]), build([1, 2, 3]))) == [1, 2, 3, 5]
    print("ok 21_merge_two_sorted_lists")
