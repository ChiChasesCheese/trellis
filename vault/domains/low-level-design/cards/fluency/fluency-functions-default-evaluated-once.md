---
id: fluency-functions-default-evaluated-once
node: fluency.functions
type: qa
step: 3
---
## Q
`def log(msg, at=datetime.now())` 的两次调用，为什么拿到的时间一模一样？默认值什么时候求值，需要“每次调用取当前值”或“区分没传和传了 None”时怎么写？

## A
**默认值在 def 时求一次，需要动态值用 None**

- **机制**：默认表达式在函数定义时执行一次，结果保存下来；`datetime.now()`、`uuid.uuid4()`、`[]`、`{}` 全都是定义那一刻的值；
- **后果**：服务启动时的时间戳成了所有日志的时间；同一个“随机 id”出现在每次调用里；
- **惯用写法**：默认 `None`，函数体里取值：`at = clock() if at is None else at`；
- **时钟当参数传入**：`clock=datetime.now` 这样默认值是函数本身（不调用），测试里换成固定时钟；
- **`None` 本身有含义时**（“把名字清空”和“不改名字”不同），用哨兵对象 `_MISSING = object()`，用 `is` 判断；
- **别写 `at or datetime.now()`**：`0`、空串等有效值也会被当成“没传”；用 `is None`。

```python
import time
from datetime import datetime

def log_bad(msg, at=datetime.now()):          # 只在 def 时调用一次
    return at

a = log_bad("x"); time.sleep(0.01); b = log_bad("y")
print(a == b)                                 # True：时间冻住了

def log(msg, *, at=None, clock=datetime.now):
    return clock() if at is None else at      # 每次调用才取值

print(log("x", at=datetime(2026, 1, 1)))      # 2026-01-01 00:00:00

_MISSING = object()
def update(name=_MISSING): return "unchanged" if name is _MISSING else name
print(update(), update(None))                 # unchanged None
```

**知识点：**函数签名与参数（Function Signatures）
