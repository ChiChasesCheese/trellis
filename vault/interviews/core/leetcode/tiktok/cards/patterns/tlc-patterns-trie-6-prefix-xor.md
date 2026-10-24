---
id: tlc-patterns-trie-6-prefix-xor
node: patterns.trie
type: qa
step: 6
---
## Q
**字典树（Trie）｜前缀的其他用法：公共前缀、数字前缀集合、二进制字典树求最大异或**

求最长公共前缀（LC 14、LC 3043）不一定要建字典树，什么时候一个 `set` 就够？比特字典树怎样求最大异或对？

## A
**LC 14 最长公共前缀**：以第一个串为初值，逐个与其他串比较，不是前缀就缩短。

```python
def longest_common_prefix(strs: list[str]) -> str:
    prefix = strs[0]
    for s in strs[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]           # 缩短到 s 也以它开头
    return prefix
print(repr(longest_common_prefix(["flower", "flow", "flight"])), repr(longest_common_prefix(["dog", "racecar", "car"])))   # 'fl' ''
```

**LC 3043**：两个整数数组，找 `arr1` 的数与 `arr2` 的数的最长公共前缀（十进制位数）。把 `arr1` 中每个数的所有前缀放进一个 `set`（反复 `x //= 10`），再对 `arr2` 的每个数从长到短找第一个在 `set` 里的前缀。

```python
def longest_common_prefix_len(arr1: list[int], arr2: list[int]) -> int:
    prefixes: set[int] = set()
    for x in arr1:
        while x:
            prefixes.add(x)
            x //= 10
    best = 0
    for y in arr2:
        while y and y not in prefixes:
            y //= 10                       # 砍掉末位，直到成为 arr1 的某个前缀
        if y:
            best = max(best, len(str(y)))
    return best
print(longest_common_prefix_len([1, 10, 100], [1000]), longest_common_prefix_len([1, 2, 3], [4, 4, 4]))   # 3 0
```

`set` 版时间 `O((n + m) · 位数)`，与字典树同阶，写法更短；当需要"枚举所有以它为前缀的串"时才需要字典树。

**最大异或对（LC 421）**：把每个数的 31 位二进制从高位到低位插入字典树，每个节点只有 0、1 两个孩子；查询 `x` 时每一位尽量走**与 `x` 当前位相反**的分支，这一位异或为 1，贪心得到最大值。`[3,10,5,25,2,8]` → `28`（`5 xor 25`）。
