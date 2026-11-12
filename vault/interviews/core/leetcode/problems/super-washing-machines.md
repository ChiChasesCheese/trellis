---
slug: super-washing-machines
---
## Q
**LC 517 超级洗衣机**｜Hard

`n` 台洗衣机排成一排，每步可任选若干台，各自同时送一件衣服给相邻一台。求让每台件数相等的最少步数，做不到返回 `-1`。

## A
**一句话。** 总数不能整除就 `-1`，否则答案是所有「边的净流量绝对值」和「单机多余件数」的最大值。

```python
def find_min_moves(machines):
    total, n = sum(machines), len(machines)
    if total % n:
        return -1
    avg = total // n
    ans = flow = 0
    for m in machines:
        surplus = m - avg          # 这台多（正）或缺（负）
        flow += surplus            # 必须流过右侧这条边的件数
        # 一条边每步过 1 件；一台每步送出 1 件
        ans = max(ans, abs(flow), surplus)
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 只看 `|flow|`：`[0,3,0]` 得 `1`，应为 `2`，中间那台要送出 `2` 件而每步只能送 `1` 件。
- 用 `|surplus|` 代替 `surplus`：`[3,0,3]` 得 `2`，应为 `1`，缺的一台能被两边同时补。

**追问。**
- 为什么是取最大值而不是求和？：各处的搬运可以并行，瓶颈只有最慢的那条边或那台机器。
- 排成一棵树怎么做？：LC 979，后序遍历，每条边流量是子树余量。

**同模式。** LC 979 在二叉树中分配硬币、LC 462 最小操作次数使数组元素相等 II
