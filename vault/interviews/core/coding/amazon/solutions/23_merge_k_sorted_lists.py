"""LC 23 Merge k Sorted Lists -- min-heap of list heads. Time O(N log k), space O(k)."""
import heapq


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
def merge_k_lists(lists):
    heap = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))    # i breaks ties: ListNode is not comparable
    dummy = tail = ListNode()
    while heap:
        _, i, node = heapq.heappop(heap)
        tail.next = node
        tail = node
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next
# --- end ---

if __name__ == "__main__":
    out = merge_k_lists([build([1, 4, 5]), build([1, 3, 4]), build([2, 6])])
    assert to_list(out) == [1, 1, 2, 3, 4, 4, 5, 6]
    assert merge_k_lists([]) is None
    assert merge_k_lists([None, None]) is None
    assert to_list(merge_k_lists([None, build([2]), build([1])])) == [1, 2]
    assert to_list(merge_k_lists([build([1, 1]), build([1, 1])])) == [1, 1, 1, 1]   # ties -> index tiebreak
    print("ok 23_merge_k_sorted_lists")
