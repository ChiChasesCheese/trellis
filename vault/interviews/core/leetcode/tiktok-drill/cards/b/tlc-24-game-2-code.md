---
id: tlc-24-game-2-code
node: b.24-game
type: qa
step: 2
---
## Q
**LC 679 24 点游戏**｜写出 Python 实现

长度为 `4` 的整数数组 `cards`（每个数在 `1` 到 `9`）。用 `+ - * /`（实数除法）和括号，能否让四个数得到 `24`？数字不能拼接，不能一元负号。返回布尔值。

## A
**思路。** `solve(nums)` 对当前的数列表：只剩一个就和 `24` 比较；否则任选两个下标 `i < j`，把 `a = nums[i]`、`b = nums[j]` 做运算得到候选结果集合，把两数去掉、结果加入，递归。`Fraction` 保证除法精确。

```python
from fractions import Fraction
from itertools import combinations


def judge_point24(cards: list[int]) -> bool:
    def solve(nums: list[Fraction]) -> bool:
        if len(nums) == 1:
            return nums[0] == 24
        for i, j in combinations(range(len(nums)), 2):     # 任选两个数合并成一个
            a, b = nums[i], nums[j]
            rest = [x for k, x in enumerate(nums) if k != i and k != j]
            results = {a + b, a * b, a - b, b - a}         # + 和 * 可交换，- 和 / 要试两个方向
            if b:
                results.add(a / b)
            if a:
                results.add(b / a)
            if any(solve([*rest, r]) for r in results):
                return True
        return False
    return solve([Fraction(c) for c in cards])
```

运行：`[4,1,8,7]` → `True`，`[1,2,1,2]` → `False`，`[8,3,8,3]` → `True`，`[3,3,8,8]` → `True`，`[1,1,1,1]` → `False`，`[9,9,9,9]` → `False`。

**复杂度。** 时间 `O(1)`：递归三层，叶子最多 `3888` 个；空间 `O(1)`：递归深度 `3`，每层最多四个数。

**写法要点。** `itertools.combinations(range(len(nums)), 2)` 直接给出所有下标对，不用双重 `for` 加 `i < j`；用**集合**存运算结果，相同结果（如 `a * b`、`b * a`）自动去重；`any(... for r in results)` 是短路的，找到一个解就停；`Fraction` 可哈希、可比较，`== 24` 是精确判断；`if b:` / `if a:` 利用 `Fraction(0)` 为假值，顺手跳过除以零。
