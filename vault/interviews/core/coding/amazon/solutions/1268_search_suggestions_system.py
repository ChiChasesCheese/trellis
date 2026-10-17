"""LC 1268 Search Suggestions System -- trie where every node keeps its 3 smallest words; one walk per keystroke."""
import bisect
from random import Random

# --- solution ---
def suggested_products(products, search_word):
    root = {}
    for word in sorted(products):                      # sorted insertion => each node's list is already sorted
        node = root
        for ch in word:
            node = node.setdefault(ch, {})
            top = node.setdefault("#", [])             # "#" holds up to 3 best words through this node
            if len(top) < 3:
                top.append(word)
    out, node = [], root
    for ch in search_word:
        node = node.get(ch) if node is not None else None
        out.append(node["#"][:] if node is not None else [])   # once the prefix falls off the trie, all later answers are []
    return out


def suggested_products_bisect(products, search_word):          # no trie: sort once, binary-search each prefix
    products = sorted(products)
    out, prefix = [], ""
    for ch in search_word:
        prefix += ch
        i = bisect.bisect_left(products, prefix)
        out.append([p for p in products[i:i + 3] if p.startswith(prefix)])
    return out
# --- end ---

def _brute(products, word):
    return [sorted(p for p in products if p.startswith(word[:k]))[:3] for k in range(1, len(word) + 1)]

if __name__ == "__main__":
    prods = ["mobile", "mouse", "moneypot", "monitor", "mousepad"]
    want = [["mobile", "moneypot", "monitor"], ["mobile", "moneypot", "monitor"],
            ["mouse", "mousepad"], ["mouse", "mousepad"], ["mouse", "mousepad"]]
    assert suggested_products(prods, "mouse") == want
    assert suggested_products(["havana"], "havana") == [["havana"]] * 6
    assert suggested_products(["havana"], "tatiana") == [[]] * 7
    assert suggested_products([], "a") == [[]]
    rng = Random(33)
    for _ in range(500):
        prods = ["".join(rng.choice("abc") for _ in range(rng.randint(1, 5))) for _ in range(rng.randint(0, 8))]
        q = "".join(rng.choice("abc") for _ in range(rng.randint(1, 6)))
        w = _brute(prods, q)
        assert suggested_products(prods, q) == w, (prods, q)
        assert suggested_products_bisect(prods, q) == w, (prods, q)
    print("ok 1268_search_suggestions_system")
