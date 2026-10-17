"""LC 472 Concatenated Words -- Trie of ALL words + DFS: from index i walk the trie; at every word end, recurse on the rest."""
from random import Random

# --- solution ---
def find_all_concatenated_words(words):
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = True

    def can_split(w, i, dead):                            # can w[i:] be cut into >= 1 dictionary words?
        if i == len(w):
            return True
        if i in dead:
            return False
        node = root
        for j in range(i, len(w)):
            node = node.get(w[j])
            if node is None:
                break
            if "$" in node and (i > 0 or j + 1 < len(w)):   # from 0 the piece must not be the whole word
                if can_split(w, j + 1, dead):
                    return True
        dead.add(i)                                       # memo: failing suffixes are never retried
        return False

    return [w for w in words if w and can_split(w, 0, set())]
# --- end ---

def _brute(words):
    ws = {w for w in words if w}
    def pieces(w, i, count):
        if i == len(w):
            return count >= 2
        return any(w[i:j] in ws and pieces(w, j, count + 1) for j in range(i + 1, len(w) + 1))
    return sorted(w for w in ws if pieces(w, 0, 0))

if __name__ == "__main__":
    ws = ["cat", "cats", "catsdogcats", "dog", "dogcatsdog", "hippopotamuses", "rat", "ratcatdogcat"]
    assert sorted(find_all_concatenated_words(ws)) == ["catsdogcats", "dogcatsdog", "ratcatdogcat"]
    assert find_all_concatenated_words(["a", "b", "ab", "abc"]) == ["ab"]
    rng = Random(472)
    for _ in range(500):
        words = list({"".join(rng.choice("ab") for _ in range(rng.randint(1, 6))) for _ in range(rng.randint(0, 9))})
        assert sorted(find_all_concatenated_words(words)) == _brute(words), words
    print("ok 472_concatenated_words_trie")
