---
id: errors-boundary-type-before-range
node: errors.boundary-validation
type: qa
step: 4
---
## Q
校验写成 `if limit < 1 or limit > 50: raise ...`，传入 `None` 或 `"5"` 会怎样？多项检查应该按什么顺序排？

## A
**先查类型，再比范围**

- **`None < 1` 抛 `TypeError`**：不是你定义的校验错误，到了上层变成 500，而不是 400；`"5" < 1` 同样；
- **`s.strip()` 在非 `str` 上抛 `AttributeError`**：所以 `isinstance(s, str)` 要在 `strip()` 之前；
- **顺序**：先看有没有，再看类型，再看取值范围，最后才看与其他字段、与已有状态的关系；
- **为什么顺序重要**：后面的检查默认前面的已经成立，类型没确认就比大小，错误就从校验层漏到了解释器；
- **短路求值**：`type(x) is int and 1 <= x <= 50` 里，类型不对时右边根本不会执行，所以类型检查必须写在左边。

```python
class BadInput(ValueError): ...

def check_limit(x):
    if not (type(x) is int and 1 <= x <= 50):
        raise BadInput("limit")
    return x

def check_name(s):
    if not isinstance(s, str) or not s.strip():
        raise BadInput("name")
    return s

for bad in (None, "5", 0, 51, True):
    try: check_limit(bad)
    except BadInput: print("rejected", repr(bad))
```

**知识点：**边界校验（Validate at the Boundary）
