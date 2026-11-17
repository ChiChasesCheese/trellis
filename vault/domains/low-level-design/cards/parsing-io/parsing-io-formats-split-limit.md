---
id: parsing-io-formats-split-limit
node: parsing-io.formats
type: qa
step: 3
---
## Q
付款记录是 `付款号, 金额, 备注`，备注是自由文本，可能含逗号，也可能整段缺失。`line.split(",")` 为什么不行？该怎么拆？

## A
**分隔符固定、最后一段自由：限定拆分次数**

- **`split(", ", 2)`**：最多切两刀，得到最多三段；最后一段保留里面所有的逗号；
- **段数检查**：至少两段（付款号和金额）；备注缺失时是两段，要当作空备注；
- **去空白**：每段 `strip()`，付款号和金额不能为空；
- **什么时候不用它**：字段里可能出现分隔符且有引号规则时，就是 CSV，用 `csv` 模块；这里没有引号规则，限定拆分次数正合适；
- **数字另转**：金额拆出来是字符串，转 `int`（分）失败要翻成同一类解析错误（代码里没写这一步）。

```python
def parse_payment(line: str) -> tuple[str, int, str]:
    parts = [p.strip() for p in line.split(", ", 2)]
    if len(parts) < 2 or not parts[0] or not parts[1]:
        raise ValueError("bad_payment")
    note = parts[2] if len(parts) == 3 else ""
    return parts[0], int(parts[1]), note

print(parse_payment("P1, 250, rent, March"))     # ('P1', 250, 'rent, March')
print(parse_payment("P2, 90"))                   # ('P2', 90, '')
print("P1, 250, rent, March".split(","))         # 四段：备注被切碎
```

**知识点：**CSV 与 JSON 的稳健读写（CSV & JSON）
