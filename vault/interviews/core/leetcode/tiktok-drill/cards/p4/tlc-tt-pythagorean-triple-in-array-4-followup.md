---
id: tlc-tt-pythagorean-triple-in-array-4-followup
node: p4.tt-pythagorean-triple-in-array
type: qa
step: 4
---
## Q
**整数数组中的勾股三元组**｜追问

面试官接着问：（1）统计不同值的三元组有多少个；（2）不排序，用哈希能不能做；（3）数值有上界 `M` 但数组很长，怎么更快？

## A
1. **统计不同值的三元组**：这里故意按平方值去重。对 `sorted({x * x for x in nums})` 做同样的双指针，命中后计数，并同时移动 `i += 1; j -= 1` 继续找；`[3,4,5,6,8,10,12,13,5]` → `3`（`3,4,5`、`6,8,10`、`5,12,13`），`[0,0,0]` → `0`（去重后只剩一个平方值）。
2. **哈希写法**：枚举斜边 `k` 和一条直角边 `a`，查另一条的平方 `need = sq[k] - sq[a]` 是否存在于 `Counter` 里。关键是别重复用下标：如果 `need` 恰好等于 `sq[a]` 或 `sq[k]`，要从可用次数里扣掉被占用的那个下标。`O(n^2)` 时间，`O(n)` 额外空间。

```python
from collections import Counter


def has_triple_hash(nums: list[int]) -> bool:
    sq = [x * x for x in nums]
    cnt = Counter(sq)                              # 平方值 -> 出现次数
    for k, c in enumerate(sq):
        for a, s in enumerate(sq):
            if a == k or s > c:
                continue
            need = c - s
            taken = 0                              # 下标 a、k 上的值若恰好等于 need，要从可用次数里扣掉
            if need == s:
                taken += 1
            if need == c:
                taken += 1
            if cnt[need] > taken:
                return True
    return False
```

`[-3,4,-5]` → `True`，`[0,0,0]` → `True`，`[3,3,5]` → `False`。
3. **数值有上界 `M`、数组很长**：从值域出发。用公式 `(m^2 - n^2, 2mn, m^2 + n^2)`（`m > n`，互质，一奇一偶）生成本原三元组，乘上各个倍数，得到斜边不超过 `M` 的全部三元组，数量约 `M log M`；对每个三元组查三个数是否都在数组里（用 `Counter` 保证次数够用）。数组远长于 `M` 时比 `O(n^2)` 快。

**Python 提醒**：`Counter` 读不存在的键返回 `0`，不会插入；`sorted({...})` 里的集合推导式用来去重，排序之后才能做双指针。
