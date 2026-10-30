---
id: tlc-two-sum-2-code
node: p2.two-sum
type: qa
step: 2
---
## Q
**LC 1 两数之和**｜写出 Python 实现

整数数组 `nums`（长度 `2` 到 `10^4`，元素和 `target` 都在 ±10^9 内），返回和为 `target` 的两个不同位置的下标，只存在一个有效答案。要求优于 `O(n^2)`。

## A
**思路。** 一遍扫描。字典 `seen` 记录「值 → 下标」；扫到 `x` 时先查 `target - x` 是否已在 `seen` 里，在就返回两个下标，不在再把 `x` 存进去。

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}                  # 值 -> 下标
    for i, x in enumerate(nums):
        if (j := seen.get(target - x)) is not None:   # 先查：只会匹配到前面的元素
            return [j, i]
        seen[x] = i                            # 后存：自己不会和自己配对
    return []
```

运行：`([2,7,11,15], 9)` → `[0, 1]`，`([3,2,4], 6)` → `[1, 2]`，`([3,3], 6)` → `[0, 1]`，`([1,2], 10)` → `[]`。

**复杂度。** 时间 `O(n)`：每个元素一次字典查询加一次插入，均摊 `O(1)`；空间 `O(n)`：字典最多存 `n` 个元素。

**写法要点。** `enumerate` 同时给下标和值；`seen.get(key)` 查不到返回 `None`，不抛 `KeyError`；海象运算符 `:=` 把「查」和「判断」合成一步，但必须写 `is not None`，因为下标 `0` 也是假值。重复值（如 `[3,3]`）后一个覆盖前一个没关系：第二个 `3` 到来时，第一个 `3` 已经在表里被查到了。
