---
id: craft-sentinels-4-inf-is-honest-unlimited
node: craft.idioms.sentinels
type: qa
step: 4
---
## Q
**哨兵 · 「无上限」和「永远不会通过」用什么数表示**｜写法

限流器的队列配额默认写成 `UNLIMITED = 1 << 30`；另一处，单次开销超过桶容量时，`retry_after` 应该返回多少秒？用一个很大的有限数、`None` 和 `math.inf` 各自的后果是什么？

## A
**要点。** 魔法数（magic number）会撒谎：`1 << 30` 约十亿，「无上限」其实有上限，且调用方可以把它当真实数字用。`math.inf` 和所有浮点数都能比较，`x < inf` 对任何有限数都成立，所以「无限」不用特殊判断；「永远不会通过」返回 `inf`，调用方不会拿一个很大的有限数去 `sleep`，白等一个不会到来的时刻。

```python
import json, math

UNLIMITED = 1 << 30
print(UNLIMITED, 2_000_000_000 > UNLIMITED)       # 「无上限」其实有上限

def retry_after(cost: int, capacity: int) -> float:
    if cost > capacity:
        return math.inf                           # 永远不会通过
    return 0.5

for cost in (1, 99):
    r = retry_after(cost, 10)
    print(cost, r, "可重试" if math.isfinite(r) else "别重试了")
print(math.inf > 10**100, math.inf == math.inf, 5 < math.inf)
print(json.dumps({"retry_after": math.inf}))
try:
    json.dumps({"retry_after": math.inf}, allow_nan=False)
except ValueError as e:
    print("ValueError:", e)
```

实际输出（Python 3.14；报错文字在 3.11 里略有不同）：

```
1073741824 True
1 0.5 可重试
99 inf 别重试了
True True True
{"retry_after": Infinity}
ValueError: Out of range float values are not JSON compliant: inf
```

**代价。** `inf` 是 `float`，表示整数配额时类型变成 `int | float`；`json.dumps` 默认输出的 `Infinity` 不是标准 JSON，别的语言的解析器会拒绝，所以出 API 之前要转成 `null` 或专门的字段（例如 `"retryable": false`）。整数配额用 `None` 表示无上限也可以，但每个比较处都要先判断 `None`。

**信号。** 需要「没有上界」「永不」时，选一个能参与比较的值（`inf`）或一个明确的 `None`，而不是一个看起来很大的整数。
