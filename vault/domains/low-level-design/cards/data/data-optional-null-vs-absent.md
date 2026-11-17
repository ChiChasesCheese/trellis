---
id: data-optional-null-vs-absent
node: data.optional
type: qa
step: 3
---
## Q
报表接口的参数 `k` 缺省是 10。请求体写 `{"k": null}` 和不写 `k`，该当成一回事吗？`body.get("k", 10)` 在这两种请求下各返回什么？

## A
**键不在和值为 null 是两个输入，合同分开定**

- **`.get("k", 10)`**：键不在返回 `10`，键在但是 `null` 返回 `None`；默认值只管“键不在”；
- **常见的三种合同**：`null` 等同缺省（筛选条件类字段）；`null` 是错误（必须是数字的 `k`）；`null` 有独立含义（“清除这个字段”）；
- **要区分就用哨兵**：`_MISSING = object()`，`body.get("k", _MISSING)`，再分三个分支；
- **错误别吞掉**：`int(None)` 会抛 `TypeError`，在适配层一律翻译成 400，不要变成 500；
- **同类问题**：JSON 的 `1.0` 与整数 `1` 在 Python 里是 `float` 与 `int`，`True` 又是 `int`，类型判断要写明。

```python
_MISSING = object()

def parse_k(body: dict) -> int:
    k = body.get("k", _MISSING)
    if k is _MISSING:
        return 10                                    # 没写：用缺省
    if type(k) is not int or not 1 <= k <= 20:
        raise ValueError("invalid_k")                # null、字符串、布尔、越界：都是 400
    return k

print(parse_k({}), parse_k({"k": 5}))
try: parse_k({"k": None})
except ValueError as e: print(e)
```

**知识点：**缺失值的表示（Optional & Null）
