---
id: tlc-super-washing-machines-2-code
node: b.super-washing-machines
type: qa
step: 2
---
## Q
**LC 517 超级洗衣机**｜写出 Python 实现

`machines`（长度 `1` 到 `10^4`，每项 `0` 到 `10^5`）是一排洗衣机的衣服件数；每步任意多台同时各向相邻台送一件。求让所有台件数相等的最少步数，做不到返回 `-1`。要求 `O(n)`。

## A
**思路。** 不能整除返回 `-1`。扫描时维护前缀余量 `flow`（必须穿过当前机器右侧那条边的件数），答案取 `|flow|` 和每台多余件数 `m - avg` 中的最大值。

```python
def find_min_moves(machines: list[int]) -> int:
    total, n = sum(machines), len(machines)
    if total % n:                          # 总数不能均分，永远做不到
        return -1
    avg = total // n
    ans = flow = 0
    for m in machines:
        surplus = m - avg                  # 这台多（正）或缺（负）几件
        flow += surplus                    # 前缀净余量：必须从它右侧这条边流过去的件数（负数表示向左流）
        # 一条边每步最多过 1 件 → |flow|；一台机器每步最多送出 1 件 → surplus
        ans = max(ans, abs(flow), surplus)
    return ans
```

运行：`[1,0,5]` → `3`，`[0,3,0]` → `2`，`[0,2,0]` → `-1`，`[2,2,0,0]` → `2`，`[3,0,3]` → `1`，`[4]` → `0`。

**复杂度。** 时间 `O(n)`：求和一遍、扫描一遍；空间 `O(1)`。

**写法要点。** `total, n = sum(machines), len(machines)` 元组赋值一行拿到两个量；`if total % n` 直接把非零余数当真值；`max(ans, abs(flow), surplus)` 一次比较三个数；`surplus` 不取绝对值是有意的，注释写清原因，面试官最常追问这一处。
