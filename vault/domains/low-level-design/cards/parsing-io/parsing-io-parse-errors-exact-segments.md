---
id: parsing-io-parse-errors-exact-segments
node: parsing-io.parse-errors
type: qa
step: 1
---
## Q
汇率记录的格式是 `USD:EUR:1.25`，多条记录用逗号连接。怎样拆分才能让缺段、多冒号、首尾多余的逗号、整串为空都被当作错误？

## A
**拆完先数段数，空段也是错**

- **先拆再数**：`rec.split(":")` 后要求 `len == 3`；缺段（`USD:EUR`）和多冒号（`USD:EUR:1:2`）都在这一步出局；
- **空段同样非法**：`USD::1` 拆出三段，其中一段是空串；要求每段非空；
- **多条记录**：`"A,B,".split(",")` 的结果最后多一个空串；它是一条空记录，所以首尾逗号被拒绝，不要用 `if x` 悄悄过滤掉；
- **空输入**：`"".split(",")` 得到 `['']`，一条空记录，不是零条记录；是否允许「零条」要写在合同里，代码再单独判；
- **不要靠 `try: a, b, c = ...`**：解包失败的异常信息是库的，分不清是缺段还是多段。

```python
def parse_record(rec: str) -> tuple[str, str, str]:
    parts = rec.split(":")
    if len(parts) != 3 or not all(parts):
        raise ValueError("bad_record")
    return tuple(parts)

for s in ("USD:EUR:1.25", "USD:EUR", "USD:EUR:1:2", "USD::1", ""):
    try: print(parse_record(s))
    except ValueError as e: print(repr(s), e)
print("USD:EUR:1,".split(","))    # ['USD:EUR:1', '']：尾逗号带来一条空记录
```

**知识点：**解析错误（Parse Errors）
