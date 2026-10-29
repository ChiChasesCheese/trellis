---
id: tlc-24-game-4-followup
node: a.24-game
type: qa
step: 4
---
## Q
**LC 679 24 点游戏**｜追问

面试官接着问：（1）要输出一个具体的表达式？（2）牌数改成 `n` 张、目标改成任意 `target`？（3）不用 `Fraction`，用浮点怎么写才安全？

## A
1. **输出表达式**：让每个元素带上它的字符串，列表元素是 `(值, 表达式)`。合并时同时拼字符串，叶子处值等于 `24` 就返回对应字符串：

```python
from fractions import Fraction
from itertools import combinations


def find_expression(cards: list[int], target: int = 24) -> str | None:
    def solve(items: list[tuple[Fraction, str]]) -> str | None:
        if len(items) == 1:
            return items[0][1] if items[0][0] == target else None
        for i, j in combinations(range(len(items)), 2):
            (a, sa), (b, sb) = items[i], items[j]
            rest = [x for k, x in enumerate(items) if k != i and k != j]
            options = [(a + b, f"({sa}+{sb})"), (a * b, f"({sa}*{sb})"),
                       (a - b, f"({sa}-{sb})"), (b - a, f"({sb}-{sa})")]
            if b:
                options.append((a / b, f"({sa}/{sb})"))
            if a:
                options.append((b / a, f"({sb}/{sa})"))
            for value, text in options:
                if (found := solve([*rest, (value, text)])) is not None:
                    return found
        return None
    return solve([(Fraction(c), str(c)) for c in cards])
```
   运行：`[4,1,8,7]` → `(8*(7-(4*1)))`，`[3,3,8,8]` → `(8/(3-(8/3)))`，`[1,2,1,2]` → `None`。
2. **`n` 张牌 / 任意目标**：同一个递归，`target` 作参数；叶子数按 `C(n,2) · 6 · C(n-1,2) · 6 …` 阶乘级增长，`n` 到 `6` 以上要加记忆化：把 `tuple(sorted(nums))` 作为缓存键，相同的多重集合只算一次。
3. **浮点版**：叶子比较 `abs(x - 24) < 1e-6`，除法前判断 `abs(b) > 1e-6`。能工作，但阈值是经验值；在这里 `Fraction` 更稳，且 `4` 张牌时速度差别可以忽略。

**Python 提醒**：`Fraction` 之间做运算得到的还是 `Fraction`，但 `Fraction + float` 会悄悄变成 `float` 并丢掉精确性；不要把 `24.0` 这样的浮点数混进来，比较目标用整数 `24`。
