---
slug: row-with-maximum-ones
---
## Q
**LC 2643 一最多的行**｜Easy

`0/1` 矩阵中找 `1` 最多的行，并列取下标最小，返回 `[行号, 1 的个数]`。

## A
**一句话。** 逐行求和，用严格大于更新，并列时自然保留更早的行。

```python
def row_and_maximum_ones(mat):
    best = [0, -1]
    for i, row in enumerate(mat):
        cnt = sum(row)
        if cnt > best[1]:        # 严格大于：并列保留小下标
            best = [i, cnt]
    return best
```

**复杂度。** 时间 `O(mn)`，空间 `O(1)`。

**易错点。**
- 用 `>=`：并列时会换成更靠后的行。
- 初值 `best = [0, 0]` 配 `>`：全零矩阵也对，但初值 `-1` 更不易出错。

**追问。**
- 一行写法？：`max(range(m), key=lambda i: (sum(mat[i]), -i))`。
- 每行已排好序（`1` 在前）？：每行二分找第一个 `0`，`O(m log n)`。

**同模式。** LC 1672 最富有客户的资产总量、LC 1431 拥有最多糖果的孩子
