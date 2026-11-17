---
id: fluency-style-naming-conventions
node: fluency.style
type: qa
step: 1
---
## Q
评审时有人指出 `def calcPrice(Items, timeout)`、`MAX_retry`、`isValid` 的命名都不对。Python 里函数、类、常量、私有成员各用什么命名？“名字里带单位和含义”指的是什么？

## A
**函数小写下划线，类驼峰，常量全大写**

- **约定（PEP 8）**：变量、函数、方法、模块用 `snake_case`；类用 `CapWords`；常量用 `UPPER_SNAKE_CASE`，写在模块顶层；
- **前导下划线**：`_helper` 表示内部使用，不属于公共接口，`from m import *` 也不会导出；双下划线开头（`__x`）会触发名字改写（name mangling），只在防止子类冲突时用，不是“私有”；`__init__` 这种首尾双下划线留给语言；
- **布尔变量读起来像判断**：`is_valid`、`has_items`、`can_retry`；别叫 `flag`、`status` 却存布尔值；
- **名字带上单位**：`timeout_ms`、`amount_cents`、`age_seconds`；一个叫 `timeout` 的参数，调用方不知道是秒还是毫秒，是 bug 的来源；
- **名字说“是什么”而不是“怎么存”**：`users` 优于 `user_list`，`price_by_sku` 说明键是什么；
- **`_` 表示故意不用**：`for _ in range(3)`、`a, _ = pair`。

```python
MAX_RETRIES = 3                          # 常量

class PaymentService:                    # 类：CapWords
    def __init__(self, timeout_ms: int):
        self._timeout_ms = timeout_ms    # 内部状态：前导下划线、带单位

    def is_expired(self, age_seconds: float) -> bool:    # 判断：is_ 开头
        return age_seconds * 1000 >= self._timeout_ms

print(PaymentService(timeout_ms=30_000).is_expired(age_seconds=29.9))   # False
```

**知识点：**命名与风格规范（Naming, Style & Linters）
