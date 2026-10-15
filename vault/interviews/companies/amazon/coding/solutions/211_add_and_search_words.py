"""LC 211 Design Add and Search Words -- trie; '.' fans out over all children (DFS). add O(L), search O(26^dots * L)."""
from random import Random
import re

# --- solution ---
class WordDictionary:
    def __init__(self):
        self.root = {}

    def add_word(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True

    def search(self, pattern):
        def dfs(node, i):
            if i == len(pattern):
                return "$" in node
            ch = pattern[i]
            if ch == ".":                              # wildcard: try every real child (skip the "$" marker)
                return any(dfs(child, i + 1) for key, child in node.items() if key != "$")
            return ch in node and dfs(node[ch], i + 1)
        return dfs(self.root, 0)
# --- end ---

if __name__ == "__main__":
    d = WordDictionary()
    for w in ["bad", "dad", "mad"]:
        d.add_word(w)
    assert d.search("pad") is False
    assert d.search("bad") is True
    assert d.search(".ad") is True
    assert d.search("b..") is True
    assert d.search("b.") is False and d.search("...") is True and d.search("....") is False
    assert d.search("") is False                       # the empty word was never added
    d.add_word("")
    assert d.search("") is True
    rng = Random(17)
    for _ in range(300):
        d, words = WordDictionary(), set()
        for _ in range(rng.randint(0, 8)):
            w = "".join(rng.choice("abc") for _ in range(rng.randint(0, 4)))
            d.add_word(w); words.add(w)
        for _ in range(15):
            p = "".join(rng.choice("abc.") for _ in range(rng.randint(0, 4)))
            assert d.search(p) == any(re.fullmatch(p, w) for w in words), (p, words)
    print("ok 211_add_and_search_words")
