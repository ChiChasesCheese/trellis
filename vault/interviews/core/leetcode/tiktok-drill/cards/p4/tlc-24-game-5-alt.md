---
id: tlc-24-game-5-alt
node: p4.24-game
type: qa
step: 5
---
## Q
**LC 679 24 点游戏**｜另一种解法

如果不想推「每步合并两个数」的递归，直接枚举所有表达式怎么写？这样做对 `4` 张牌可以接受吗？

## A
**思路。** `4` 张牌时表达式总数有限：`4!` 个数字排列，`4^3` 个运算符组合，`5` 种括号形状（`((ab)c)d`、`(ab)(cd)`、`(a(bc))d`、`a((bc)d)`、`a(b(cd))`）。全部算一遍，有一个等于 `24` 就返回 `True`。除数为 `0` 的表达式作废。

```python
from collections.abc import Callable
from fractions import Fraction
from itertools import permutations, product
from operator import add, mul, sub, truediv


def judge_point24_shapes(cards: list[int]) -> bool:
    def calc(op: Callable[[Fraction, Fraction], Fraction], x: Fraction | None, y: Fraction | None) -> Fraction | None:
        if x is None or y is None:
            return None
        try:
            return op(x, y)
        except ZeroDivisionError:          # 除数为 0：这条表达式作废
            return None

    for a, b, c, d in permutations(map(Fraction, cards)):
        for o1, o2, o3 in product((add, sub, mul, truediv), repeat=3):
            results = (
                calc(o3, calc(o2, calc(o1, a, b), c), d),      # ((a b) c) d
                calc(o3, calc(o1, a, b), calc(o2, c, d)),      # (a b) (c d)
                calc(o3, calc(o2, a, calc(o1, b, c)), d),      # (a (b c)) d
                calc(o3, a, calc(o2, calc(o1, b, c), d)),      # a ((b c) d)
                calc(o3, a, calc(o2, b, calc(o1, c, d))),      # a (b (c d))
            )
            if 24 in results:
                return True
    return False
```

运行：`[4,1,8,7]` → `True`，`[1,2,1,2]` → `False`。

**为什么对。** 五种形状覆盖四个操作数的全部二叉括号结构（卡特兰数 `C_3 = 5`）；`permutations` 覆盖操作数顺序，`product` 覆盖三个运算符的选择，因此枚举了所有不使用一元负号、不拼接数字的表达式。

**取舍。** 暴力版总共 `24 * 64 * 5 = 7680` 个表达式，对固定的 `4` 张牌完全可接受，且不依赖「合并两个数」这个观察，难以写错；缺点是只适用于 `4` 张牌，推广到 `n` 张需要生成所有括号结构，非常繁琐。合并法的优点是对 `n` 通用、重复计算更少，面试里先说出暴力的规模，再给合并法。
