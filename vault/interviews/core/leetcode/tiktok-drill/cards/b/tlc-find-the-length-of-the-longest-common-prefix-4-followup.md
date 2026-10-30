---
id: tlc-find-the-length-of-the-longest-common-prefix-4-followup
node: b.find-the-length-of-the-longest-common-prefix
type: qa
step: 4
---
## Q
**LC 3043 最长公共前缀的长度**｜追问

面试官接着问：（1）用字典树（trie）怎么写？（2）能不能不建集合，只靠排序？（3）要返回具体是哪一对数和那个前缀？

## A
1. **字典树**：把 `arr1` 每个数的数字串插入字典树；对 `arr2` 的每个数沿树往下走，走不下去时已走的深度就是它的最长公共前缀。

```python
def longest_common_prefix_trie(arr1: list[int], arr2: list[int]) -> int:
    root: dict[str, dict] = {}
    for x in arr1:
        node = root
        for ch in str(x):
            node = node.setdefault(ch, {})   # 没有就建一层
    best = 0
    for y in arr2:
        node, depth = root, 0
        for ch in str(y):
            if ch not in node:
                break
            node = node[ch]
            depth += 1
        best = max(best, depth)
    return best
```

   `([1,10,100], [1000])` → `3`，`([123], [129])` → `2`。复杂度与集合版同阶，常数更大（每个数字一个字典）。
2. **排序**：把两组数都转成字符串并标上来源，合并排序。任意两个来自不同数组的字符串，它们的公共前缀不超过排序后夹在它们之间的任一相邻对的公共前缀，所以最长公共前缀一定出现在相邻、且来自不同数组的一对上。线性扫描相邻对，`O((n + m) log(n + m) · L)`，不需要额外的集合。
3. **返回具体的数**：集合里的值换成字典 `前缀 → 某个产生它的 arr1 的数`，命中时记下 `y` 和前缀，答案对是 `(字典[前缀], y)`。

**Python 提醒**：`dict.setdefault(ch, {})` 每次调用都会先构造一个空字典再决定要不要用，量大时可以用 `collections.defaultdict` 或自定义节点类避免这笔开销；整数 `x //= 10` 对正数是向下取整，对负数方向相反，这里全是正整数所以没问题。
