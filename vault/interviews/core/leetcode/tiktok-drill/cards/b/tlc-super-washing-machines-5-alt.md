---
id: tlc-super-washing-machines-5-alt
node: b.super-washing-machines
type: qa
step: 5
---
## Q
**LC 517 超级洗衣机**｜另一种解法

换一个角度：站在每台机器上，看它左侧整体和右侧整体各多或缺多少，能不能直接算出这台机器至少要忙几步？写出这种逐台分析的解法，并说明和前缀流量版本的取舍。

## A
**思路。** 对第 `i` 台，`left` 是左侧 `i` 台的总余量，`right` 是右侧 `n - 1 - i` 台的总余量（正数多、负数缺）。
- 两侧都缺：缺的全部要从第 `i` 台送出，每步只能送一件 → `-left - right` 步。
- 两侧都多：第 `i` 台可以同时从两边接收 → `max(left, right)` 步。
- 一多一缺：衣服要穿过第 `i` 台，瓶颈是较大的那一侧 → `max(|left|, |right|)` 步。
答案取所有台的最大值。

```python
def find_min_moves_per_machine(machines: list[int]) -> int:
    total, n = sum(machines), len(machines)
    if total % n:
        return -1
    avg = total // n
    ans = left_sum = 0
    for i, m in enumerate(machines):
        left = left_sum - i * avg                          # 左侧整体的余量：负数表示左侧缺
        right = (total - left_sum - m) - (n - 1 - i) * avg # 右侧整体的余量
        if left < 0 and right < 0:                         # 两侧都缺：全部由 i 送出，一步只能送一件
            ans = max(ans, -left - right)
        elif left > 0 and right > 0:                       # 两侧都多：i 可以同时从两边接收
            ans = max(ans, left, right)
        else:                                              # 一侧多一侧缺：衣服要穿过 i
            ans = max(ans, abs(left), abs(right))
        left_sum += m
    return ans
```

运行：`[1,0,5]` → `3`，`[0,3,0]` → `2`，`[0,2,0]` → `-1`，`[2,2,0,0]` → `2`，`[3,0,3]` → `1`。

**取舍。** 两种写法都是 `O(n)` 时间、`O(1)` 空间，结果相同。逐台分析把「机器能同时两边收、却只能一件件往外送」这层不对称写成三个分支，解释起来更直观，适合先讲清思路；前缀流量版把同样的约束压缩成 `|flow|` 和 `surplus` 两个量，代码更短、更不容易写错，适合最后落笔。很小的输入（几台机器、十来件衣服）还可以用 BFS 搜索状态求出精确步数，作为两种公式的参照。
