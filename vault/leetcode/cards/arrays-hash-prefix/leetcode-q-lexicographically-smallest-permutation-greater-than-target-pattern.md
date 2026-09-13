---
id: leetcode-q-lexicographically-smallest-permutation-greater-than-target-pattern
node: arrays-hash-prefix.enumeration
type: qa
anki: 1788391211098
tags: [lc::3720, leetcode, pattern, recall]
---
## Q
求「用给定字符集组成的、字典序大于 target 的最小排列」，如何贪心构造？

## A
从右往左遍历 target 的每个位置 i：先把 target[i] 这个字符“归还”给可用字符计数器 cnt（相当于假设前 i 位与 target 相同，第 i 位待定），若归还后出现负数说明字符不够用，跳过继续往左；否则在 cnt 中找比 target[i] 大的最小字符 bigger（sorted(cnt) 中第一个 count>0 且大于 c 的），若找不到就继续往左找更高位放大；找到则令该位为 bigger，剩余字符升序排列拼在后面（因为后面已经比 target 严格大，可以任意取最小排列），返回 target[:i] + bigger + 剩余升序字符串；若所有位置都试过仍无解，返回空串。

**Evidence**

```
def lexGreaterPermutation(self, s, target):
    cnt = Counter(s)
    cnt.subtract(target)
    for i in range(len(target) - 1, -1, -1):
        c = target[i]
        cnt[c] += 1
        if any(v < 0 for v in cnt.values()):
            continue
        bigger = next((ch for ch in sorted(cnt) if cnt[ch] > 0 and ch > c), None)
        if not bigger:
            continue
        cnt[bigger] -= 1
        return target[:i] + bigger + ''.join(sorted(cnt.elements()))
    return ""
```

[原文 ↗](obsidian://open?vault=lc&file=questions%2F3720%20-%20Lexicographically%20Smallest%20Permutation%20Greater%20Than%20Target)
