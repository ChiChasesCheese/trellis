---
slug: k-th-smallest-in-lexicographical-order
---
## Q
**LC 440 字典序的第 K 小数字**｜Hard

求 `[1, n]` 中按字典序排列的第 `k` 小的数字，`n` 最大 `10^9`。

## A
**一句话。** 把 `1..n` 看成十叉前缀树，字典序即先序遍历：子树装得下剩余步数就整棵跳过，装不下就钻进第一个孩子。

```python
def find_kth_number(n, k):
    def count(prefix):             # 以 prefix 为根的子树有几个数 <= n
        lo, hi, total = prefix, prefix + 1, 0
        while lo <= n:
            total += min(n + 1, hi) - lo   # 末层被 n 截断
            lo, hi = lo * 10, hi * 10
        return total

    cur, k = 1, k - 1              # 起点 1 已占第一名
    while k:
        size = count(cur)
        if size <= k:              # 不在子树里：跳到右邻兄弟
            k -= size
            cur += 1
        else:                      # 在子树里：钻进第一个孩子
            k -= 1
            cur *= 10
    return cur
```

**复杂度。** 时间 `O(log² n)`，空间 `O(1)`。

**易错点。**
- `count` 里写 `min(n, hi)`：区间是半开的，`n` 自己漏数，`(13, 13)` 得 `10`，应为 `9`。
- 忘了 `k -= 1`：起点 `1` 已占第一名，`(13, 2)` 得 `11`，应为 `10`。

**追问。**
- 反过来求 `x` 的字典序排名？：沿根到 `x` 的路径累加被跳过的左邻兄弟子树大小，再加祖先个数。
- 只要输出字典序前 `k` 个数（LC 386）？：按「下一个数」规则迭代，不用算子树大小，`O(k)`。

**同模式。** LC 386 字典序排数、LC 60 排列序列、LC 668 乘法表中第 k 小的数、LC 378 有序矩阵中第 K 小的元素
