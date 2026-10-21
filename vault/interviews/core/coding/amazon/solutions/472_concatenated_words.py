"""LC 472 Concatenated Words -- shortest-first: a word is concatenated iff the trie of SHORTER words segments it."""
from random import Random

# --- solution ---
def find_all_concatenated_words(words):
    root = {}
    out = []

    def segmentable(w):                              # forward DP, trie walk from every reachable position
        n = len(w)
        reachable = [False] * (n + 1)
        reachable[0] = True
        for i in range(n):
            if not reachable[i]:
                continue
            node = root
            for j in range(i, n):
                node = node.get(w[j])
                if node is None:
                    break
                if "$" in node:
                    reachable[j + 1] = True
            if reachable[n]:
                return True
        return False

    for w in sorted({w for w in words if w}, key=len):   # drop "" and duplicates; shortest first
        if segmentable(w):                                # the trie holds only shorter words: >= 2 pieces
            out.append(w)
        else:
            node = root                                   # a concatenated word adds nothing to the trie, so skip it
            for ch in w:
                node = node.setdefault(ch, {})
            node["$"] = True
    return out
# --- end ---

def _brute(words):
    ws = {w for w in words if w}
    def pieces(w, i, count):
        if i == len(w):
            return count >= 2
        return any(w[i:j] in ws and pieces(w, j, count + 1)
                   for j in range(i + 1, len(w) + 1))
    return sorted(w for w in ws if pieces(w, 0, 0))

if __name__ == "__main__":
    ws = ["cat", "cats", "catsdogcats", "dog", "dogcatsdog", "hippopotamuses", "rat", "ratcatdogcat"]
    assert sorted(find_all_concatenated_words(ws)) == ["catsdogcats", "dogcatsdog", "ratcatdogcat"]
    assert sorted(find_all_concatenated_words(["cat", "dog", "catdog"])) == ["catdog"]
    assert find_all_concatenated_words([""]) == []
    assert find_all_concatenated_words(["a", "a"]) == []                  # a word is not made of ITSELF twice
    assert sorted(find_all_concatenated_words(["a", "aa", "aaa"])) == ["aa", "aaa"]
    rng = Random(29)
    for _ in range(500):
        words = ["".join(rng.choice("ab") for _ in range(rng.randint(0, 6))) for _ in range(rng.randint(0, 9))]
        assert sorted(find_all_concatenated_words(words)) == _brute(words), words
    print("ok 472_concatenated_words")
