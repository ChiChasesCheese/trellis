---
id: errors-boundary-no-silent-coercion
node: errors.boundary-validation
type: qa
step: 3
---
## Q
校验一个“数量”参数时，先 `int(x)` 转换再比范围，会把哪些本该拒绝的输入放进来？

## A
**转换会把错误输入变成合法值**

- **截断**：`int(3.9)` 是 `3`，`int(True)` 是 `1`，调用方传错了类型，得到的却是成功；
- **字符串太宽松**：`int("1_0")` 是 `10`，`int(" 5 ")` 是 `5`，`int("+5")` 是 `5`，`int("１２")`（全角）是 `12`；
- **`isdigit()` 认全角数字**：`"１２".isdigit()` 为 `True`，要加 `.isascii()`；正则里 `\d` 同样匹配 Unicode 数字，用 `[0-9]`；
- **`$` 放过结尾换行**：`re.match(r"^[0-9]+$", "12\n")` 能匹配，用 `re.fullmatch`；
- **取舍**：宽容看着友好，但调用方的 bug 被藏起来，两个调用方对同一输入还可能各有理解；默认严格，需要宽容就把解析规则明写出来。

```python
import re

print(int(3.9), int("1_0"), int(" 5 "), int("+5"), int("１２"))

def strict_int(s: str) -> int:
    if not re.fullmatch(r"[0-9]+", s):      # 只收 ASCII 数字
        raise ValueError(s)
    return int(s)

print(strict_int("12"))
```

**知识点：**边界校验（Validate at the Boundary）
