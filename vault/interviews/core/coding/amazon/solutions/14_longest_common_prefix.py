"""LC 14 Longest Common Prefix -- vertical scan (O(total chars)), and the trie version for many queries."""
from random import Random

# --- solution ---
def longest_common_prefix(strs):
    if not strs:
        return ""
    first = strs[0]
    for i, ch in enumerate(first):               # vertical scan: column i of every word
        for s in strs[1:]:
            if i == len(s) or s[i] != ch:
                return first[:i]
    return first


class PrefixTrie:                                # the same answer from a trie; worth it when words are added over time
    def __init__(self):
        self.root = {}                           # node = dict char -> child node; "$" marks the end of a word
        self.size = 0

    def add(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True
        self.size += 1

    def common_prefix(self):
        node, out = self.root, []
        while len(node) == 1 and "$" not in node:   # exactly one way to continue and no word ends here
            ch = next(iter(node))
            out.append(ch)
            node = node[ch]
        return "".join(out)
# --- end ---

def _brute(strs):
    best = ""
    for k in range(1, min(map(len, strs), default=0) + 1):
        if len({s[:k] for s in strs}) == 1:
            best = strs[0][:k]
    return best

if __name__ == "__main__":
    assert longest_common_prefix(["flower", "flow", "flight"]) == "fl"
    assert longest_common_prefix(["dog", "racecar", "car"]) == ""
    assert longest_common_prefix(["a"]) == "a"
    assert longest_common_prefix(["", "b"]) == ""
    assert longest_common_prefix(["ab", "ab"]) == "ab"
    assert longest_common_prefix(["ab", "abc"]) == "ab"
    rng = Random(12)
    for _ in range(500):
        strs = ["".join(rng.choice("ab") for _ in range(rng.randint(0, 5))) for _ in range(rng.randint(1, 5))]
        want = _brute(strs)
        assert longest_common_prefix(strs) == want, strs
        t = PrefixTrie()
        for s in strs:
            t.add(s)
        assert t.common_prefix() == want, strs
    print("ok 14_longest_common_prefix")
