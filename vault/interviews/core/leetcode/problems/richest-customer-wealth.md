---
slug: richest-customer-wealth
---
## Q
**LC 1672 最富有客户的资产总量**｜Easy

`accounts[i][j]` 是第 `i` 位客户在第 `j` 家银行的存款。返回单个客户在所有银行的存款总和的最大值。

## A
**一句话。** 每行求和，取最大。

```python
def maximum_wealth(accounts):
    best = 0
    for row in accounts:
        best = max(best, sum(row))   # 一行 = 一位客户
    return best
```

**复杂度。** 时间 `O(mn)`，空间 `O(1)`。

**易错点。**
- 按列求和：行才是客户，列是银行。
- 初值设成负无穷并不必要：存款非负，从 `0` 开始即可。

**追问。**
- 想一行写完？：`max(map(sum, accounts))`。
- 数据放在多个文件里？：逐行流式累加，只保留当前最大值。

**同模式。** LC 1431 拥有最多糖果的孩子、LC 2643 一最多的行、LC 1 两数之和
