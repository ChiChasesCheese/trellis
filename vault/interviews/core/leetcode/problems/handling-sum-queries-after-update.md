---
slug: handling-sum-queries-after-update
---
## Q
**LC 2569 更新数组后处理求和查询**｜Hard

`0/1` 数组 `nums1` 和数组 `nums2`。操作 1 把 `nums1[l..r]` 取反；操作 2 令所有 `nums2[i] += nums1[i]·p`；操作 3 询问 `sum(nums2)`。返回所有操作 3 的答案。

## A
**一句话。** 操作 2 只让 `nums2` 总和增加 `p × (nums1 中 1 的个数)`，所以只需维护 1 的个数；区间取反用懒标记线段树，翻转后 1 的个数变成「长度 − 原个数」。

```python
def handle_query(nums1, nums2, queries):
    n = len(nums1)
    cnt = [0] * (4 * n)        # 区间里 1 的个数
    flip = [False] * (4 * n)   # 懒标记：子结点待翻转

    def build(o, l, r):
        if l == r:
            cnt[o] = nums1[l]
            return
        m = (l + r) // 2
        build(2 * o, l, m)
        build(2 * o + 1, m + 1, r)
        cnt[o] = cnt[2 * o] + cnt[2 * o + 1]

    def apply(o, l, r):        # 整段翻转
        cnt[o] = (r - l + 1) - cnt[o]
        flip[o] = not flip[o]

    def update(o, l, r, L, R):
        if L <= l and r <= R:
            apply(o, l, r)
            return
        m = (l + r) // 2
        if flip[o]:            # 先把懒标记推给孩子
            apply(2 * o, l, m)
            apply(2 * o + 1, m + 1, r)
            flip[o] = False
        if L <= m:
            update(2 * o, l, m, L, R)
        if R > m:
            update(2 * o + 1, m + 1, r, L, R)
        cnt[o] = cnt[2 * o] + cnt[2 * o + 1]

    build(1, 0, n - 1)
    total, ans = sum(nums2), []
    for op, a, b in queries:
        if op == 1:
            update(1, 0, n - 1, a, b)
        elif op == 2:
            total += a * cnt[1]    # 只要全局 1 的个数
        else:
            ans.append(total)
    return ans
```

**复杂度。** 时间 `O(n + q log n)`，空间 `O(n)`。

**易错点。**
- 真的去更新 `nums2`：每次 `O(n)`，总和只依赖 1 的个数。
- 懒标记用赋值 `flip[o] = True`：翻两次等于没翻，要取反。

**追问。**
- 不用线段树？：把 `nums1` 看成一个大整数，区间取反是异或一个掩码，`bit_count()` 得 1 的个数，Python 里很快。
- 换成区间赋值为 1？：懒标记改成「整段置 1」，`cnt = 长度`，下推时覆盖孩子的翻转标记。

**同模式。** LC 307 区域和检索 - 数组可修改、LC 699 掉落的方块
