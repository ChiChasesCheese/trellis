---
id: api-returns-result-object
node: api.returns
type: qa
step: 3
---
## Q
限流器的 `check(key)` 返回三元组 `(allowed, remaining, reset_after_ms)`。调用方什么时候会把后两项弄反？返回多个值时，元组、字典、命名元组、数据类各适合什么场合？

## A
**多于两个值，就给它们名字**

- **位置不带含义**：`(True, 0, 1500)` 里哪个是剩余次数、哪个是等待毫秒，只能去翻文档；两个都是 `int`，弄反了类型检查器也看不出；
- **`NamedTuple`**：既能 `a, r, t = check(k)` 解包，又能 `res.remaining` 取名；已有调用方不会被改坏，适合从元组演进过来；
- **`dataclass(frozen=True)`**：要加方法、加默认值、以后继续加字段时用；不能解包，反而逼调用方按名字取，加字段不会破坏旧调用；
- **普通 `dict`**：键拼错只在运行时才发现，多用于直接序列化成 JSON 的出口；
- **两个值的元组**（如 `(ok, value)`）是惯用写法，三个以上就换成有名字的类型。

```python
from typing import NamedTuple

class Verdict(NamedTuple):
    allowed: bool
    remaining: int
    reset_after_ms: int

def check(used: int, limit: int = 3) -> Verdict:
    left = max(limit - used, 0)
    return Verdict(left > 0, left, 0 if left else 1500)

v = check(3)
print(v.reset_after_ms, v)                   # 1500
allowed, remaining, reset = check(1)         # 仍然可以解包
```

**知识点：**返回值设计（Return Values）
