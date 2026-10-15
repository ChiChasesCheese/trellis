"""LC 341 Flatten Nested List Iterator -- lazy iterator with an explicit stack. next O(1) amortized, has_next O(depth)."""

class NestedInteger:                       # LeetCode supplies this interface; here a tiny stand-in
    def __init__(self, value):
        self._v = value

    def isInteger(self):
        return isinstance(self._v, int)

    def getInteger(self):
        return self._v

    def getList(self):
        return self._v


def make(x):
    return NestedInteger([make(i) for i in x] if isinstance(x, list) else x)

# --- solution ---
class NestedIterator:
    def __init__(self, nested_list):
        self.stack = list(reversed(nested_list))      # top of stack = next item to look at

    def has_next(self):
        while self.stack:                             # unwrap lists lazily until an integer is on top
            top = self.stack[-1]
            if top.isInteger():
                return True
            self.stack.pop()
            self.stack.extend(reversed(top.getList()))
        return False

    def next(self):
        if not self.has_next():                       # next() must be safe without a prior has_next()
            raise StopIteration
        return self.stack.pop().getInteger()
# --- end ---

def _drain(it):
    out = []
    while it.has_next():
        out.append(it.next())
    return out

if __name__ == "__main__":
    assert _drain(NestedIterator([make(x) for x in [[1, 1], 2, [1, 1]]])) == [1, 1, 2, 1, 1]
    assert _drain(NestedIterator([make(x) for x in [1, [4, [6]]]])) == [1, 4, 6]
    assert _drain(NestedIterator([make(x) for x in [[], [[]], []]])) == []      # only empty lists
    assert _drain(NestedIterator([])) == []
    it = NestedIterator([make(x) for x in [[[3]]]])
    assert it.next() == 3                                                      # next() without has_next()
    print("ok 341_flatten_nested_list_iterator")
