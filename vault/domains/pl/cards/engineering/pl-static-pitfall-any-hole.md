---
id: pl-static-pitfall-any-hole
node: engineering.static-analysis
type: qa
step: 8
---
## Q
类型检查器（mypy）报告「没有问题」，是否说明类型都对？用一个 `json.loads` 的例子说明它会在哪里漏掉错误。

## A
不能。类型检查器只保证**有类型信息的部分**。一旦值的类型是 `Any`（任意类型），检查器就关闭对它的检查，错误会穿过这个洞。

**例**：函数标注了 `int` 参数，数据却来自 JSON：

```python
import json

def total_cents(price: int, qty: int) -> int:
    return price * qty

order = json.loads('{"price": "250", "qty": 3}')   # json.loads returns Any
print(total_cents(order["price"], order["qty"]))
```

`mypy --strict` 的结果：

```text
Success: no issues found in 1 source file
```

运行输出：

```text
250250250
```

`json.loads` 返回 `Any`，所以 `order["price"]` 也是 `Any`，传给 `int` 参数时检查器不拦。更糟的是运行时也没有报错：字符串 `"250"` 乘以整数 `3` 在 Python 里是合法的重复，得到 `"250250250"`，一个错误的账目悄悄地进入了系统。

**教训**：
- 静态保证的强度等于**最弱的那一环**。凡是进入系统的外部数据（JSON、数据库、环境变量），都是类型洞的入口。
- 在边界处**验证并转换**，而不是仅仅断言类型：用 pydantic、`msgspec` 或 dataclass 加手写校验，把 `Any` 变成确定的类型后再进入内部；Go 里是 `json.Unmarshal` 到有类型的结构体，Rust 里是 serde，Java 里是 Jackson 的有类型绑定，类型就在解码时被强制了。
- 严格模式的一些开关（如 `disallow_any_explicit`、`warn_return_any`）能让 `Any` 更显眼，但不能消除它。
