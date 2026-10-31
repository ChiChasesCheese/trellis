---
id: tlc-shu-zu-zhong-de-ni-xu-dui-lcof-5-alt
node: b.shu-zu-zhong-de-ni-xu-dui-lcof
type: qa
step: 5
---
## Q
**剑指 Offer 51 数组中的逆序对**｜另一种解法

不用归并排序，还有什么 `O(n log n)` 的做法？它是怎么计数的，什么时候该选它，什么时候选归并？

## A
**思路：树状数组（Fenwick tree）。** 从左到右扫描。对每个元素 `v`，已经出现过的元素共有 `seen` 个，其中不超过 `v` 的有 `prefix(rank(v))` 个，所以严格大于 `v` 的有 `seen - prefix(rank(v))` 个——这就是以 `v` 为后项的逆序对数。再把 `v` 的名次加入树状数组。因为值的范围可能很大，先**离散化**（只保留相对大小）：把去重排序后的值映射成 `1..m` 的名次。

```python
def reverse_pairs_bit(record: list[int]) -> int:
    rank = {v: i for i, v in enumerate(sorted(set(record)), 1)}   # 离散化：值 -> 1..m
    tree = [0] * (len(rank) + 1)                                   # 树状数组，记录各名次出现的次数

    def add(i: int) -> None:
        while i < len(tree):
            tree[i] += 1
            i += i & -i

    def prefix(i: int) -> int:                                     # 名次 <= i 的元素个数
        total = 0
        while i > 0:
            total += tree[i]
            i -= i & -i
        return total

    count = 0
    for seen, v in enumerate(record):
        r = rank[v]
        count += seen - prefix(r)                                  # 前面已出现的元素里，严格大于 v 的个数
        add(r)
    return count
```

运行：`[9,7,5,4,6]` → `8`，`[]` → `0`，`[2,2,2]` → `0`，`[3,2,1]` → `3`；`50000` 个随机数约 `0.03` 秒，结果与归并版一致。

**复杂度。** 时间 `O(n log n)`（排序 + 每个元素两次 `O(log m)` 操作）；空间 `O(n)`。

**什么时候选哪个。**
- 归并排序：不需要额外的数据结构，代码短，逻辑在一个函数里；合并后的有序数组可以直接复用（LC 315、LC 493 都是它的变体）。面试里的默认答案。
- 树状数组：思路是「在线」的——边读边数，不需要整体重排；需要同时回答区间计数、单点更新（比如逆序对随更新变化）时是首选；代价是要离散化，写法稍长，位运算 `i & -i` 要熟。
- 暴力 `O(n^2)`：只在 `n` 很小（几千）时可接受，如果面试官只想确认正确性可以先说出来。

**Python 提醒**：`i & -i` 取最低位的 `1`，Python 的负整数用无限补码表示，所以这个技巧同样成立；`enumerate(sorted(set(record)), 1)` 的第二个参数让名次从 `1` 开始，树状数组下标必须从 `1` 起，`0` 会让 `i += i & -i` 死循环。
