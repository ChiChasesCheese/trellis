"""LC 2 Add Two Numbers -- digit-by-digit with carry (digits stored in reverse). Time O(max(m,n)), space O(1) extra."""


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
def add_two_numbers(a, b):
    dummy = tail = ListNode()
    carry = 0
    while a or b or carry:                 # carry keeps the loop alive for the final extra digit
        total = carry
        if a:
            total += a.val
            a = a.next
        if b:
            total += b.val
            b = b.next
        carry, digit = divmod(total, 10)
        tail.next = ListNode(digit)
        tail = tail.next
    return dummy.next
# --- end ---

if __name__ == "__main__":
    assert to_list(add_two_numbers(build([2, 4, 3]), build([5, 6, 4]))) == [7, 0, 8]
    assert to_list(add_two_numbers(build([0]), build([0]))) == [0]
    assert to_list(add_two_numbers(build([9, 9, 9, 9]), build([1]))) == [0, 0, 0, 0, 1]   # final carry
    assert to_list(add_two_numbers(build([5]), build([5]))) == [0, 1]
    print("ok 2_add_two_numbers")
