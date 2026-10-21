"""LC 49 Group Anagrams -- group by a canonical key. Time O(n*k), space O(n*k)."""
from collections import defaultdict

# --- solution ---
def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        count = [0] * 26                       # letter histogram is the canonical form
        for ch in s:
            count[ord(ch) - ord("a")] += 1
        groups[tuple(count)].append(s)         # tuple: hashable, a list is not
    return list(groups.values())
# --- end ---

if __name__ == "__main__":
    out = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    norm = sorted(sorted(g) for g in out)
    assert norm == [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
    assert group_anagrams([""]) == [[""]]
    assert group_anagrams(["a"]) == [["a"]]
    assert sorted(len(g) for g in group_anagrams(["ab", "ba", "ab", "cd"])) == [1, 3]
    print("ok 49_group_anagrams")
