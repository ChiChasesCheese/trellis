---
id: tlc-k-th-smallest-in-lexicographical-order-4-followup
node: a.k-th-smallest-in-lexicographical-order
type: qa
step: 4
---
## Q
**LC 440 字典序的第 K 小数字**｜追问

面试官接着问：（1）反过来，给定数字 `x`，它在字典序里排第几？（2）要输出字典序的前 `k` 个数（LC 386）？（3）复杂度 `O(log^2 n)` 是怎么来的？

## A
1. **求排名。** 对 `x` 的每个前缀 `p`（从最高位一直到 `x` 本身），累加同一个父结点下比 `p` 小的所有兄弟的子树大小（用 `count`），再加 `1` 表示 `p` 自己；各层相加就是排名。
2. **前 `k` 个数。** 不需要子树大小，按"字典序的下一个数"迭代即可：

```python
def lexical_order(n: int) -> list[int]:
    res: list[int] = []
    cur = 1
    for _ in range(n):
        res.append(cur)
        if cur * 10 <= n:
            cur *= 10                            # 能往下一层就先往下
        else:
            if cur >= n:
                cur //= 10                       # 已经是最大的了：回到上一层
            cur += 1                             # 右邻兄弟
            while cur % 10 == 0:                 # 进位到 0 说明这一层走完，继续回退
                cur //= 10
    return res
```

3. **复杂度来源。** 外层每个数位层最多向右跳 `9` 次、下钻 `1` 次，共约 `9 · log10(n)` 次循环；每次 `count` 至多遍历 `log10(n)` 层。乘起来 `O(log^2 n)`，`n = 10^9` 时约几百次基本操作。

**Python 提醒**：`sorted(range(1, n + 1), key=str)` 是小数据下最短的参照写法，`key=str` 把整数当字符串比较；注意它按字符逐位比较，所以 `"10" < "2"`。
