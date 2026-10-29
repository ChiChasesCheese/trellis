---
id: tlc-rabbits-in-forest-4-followup
node: a.rabbits-in-forest
type: qa
step: 4
---
## Q
**LC 781 森林中的兔子**｜追问

面试官接着问：（1）回答是流式到来的、不能先统计怎么办？（2）要输出一种具体的颜色分配？（3）为什么向上取整不直接用 `math.ceil`？

## A
1. **流式一遍扫描。** 为每个回答值记「当前这组还空着的名额」。来了回答 `x`：有空名额就占一个；没有就新开一组（总数加 `x + 1`，新组还剩 `x` 个空名额）。

```python
from collections import defaultdict
from collections.abc import Iterable


def num_rabbits_stream(answers: Iterable[int]) -> int:
    free: defaultdict[int, int] = defaultdict(int)   # free[x]：回答 x 的最新一组里还空着的名额
    total = 0
    for x in answers:
        if free[x]:
            free[x] -= 1                              # 加入已有的颜色组
        else:
            total += x + 1                            # 新开一个颜色组，共 x + 1 只
            free[x] = x                               # 本只占了一个，还剩 x 个名额
    return total
```

2. **具体分配。** 对每个回答值开 `ceil(count / (x + 1))` 个颜色编号，依次给被问到的兔子分配，一组满了换下一个编号；没被问到的兔子按各组的缺口补齐。
3. **取整写法。** `math.ceil(count / (x + 1))` 先做浮点除法，数值超过 `2^53` 会丢精度；`-(-count // (x + 1))` 或 `(count + x) // (x + 1)` 全程整数，没有这个问题。

**Python 提醒**：`defaultdict(int)` 读取不存在的键时会**插入**默认值 `0`，所以 `if free[x]` 也会创建键；这里无妨，但如果之后要用 `len(free)` 统计不同回答值的个数，要意识到读取就算插入。
