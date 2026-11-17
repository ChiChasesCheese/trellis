---
id: parsing-io-parse-errors-trailing-input
node: parsing-io.parse-errors
type: qa
step: 4
---
## Q
`JSONDecoder.raw_decode` 能成功解析一个前缀。用它读一行请求，`{"a":1} x` 和截断的 `{"a":` 应该怎么处理，为什么？

## A
**解析完要检查整串吃完，剩下只能是空白**

- **`raw_decode` 只解析前缀**：返回对象和结束位置；`{"a":1} x` 成功返回 `({'a': 1}, 7)`，后面的 ` x` 被悄悄丢掉；
- **所以要自己查**：`text[end:]` 里除了合同允许的空白字符，什么都不能有；
- **截断**：`{"a":` 在对象结束之前就读完了，解析自己会失败；不要把失败降级成「读到多少算多少」；
- **前导空白**：`raw_decode` 不跳过开头的空白；`loads` 会，所以直接用 `loads` 更简单，`raw_decode` 是为了要结束位置才用；
- **和 `loads` 的差别**：`loads` 内部做了同样的检查，报 `Extra data`；自己写解析器时容易漏掉这一步。

```python
import json

DEC = json.JSONDecoder()

def parse_all(text: str):
    obj, end = DEC.raw_decode(text)                     # 只解析一个前缀
    if text[end:].strip(" \t\r\n"): raise ValueError("invalid_json")
    return obj

print(DEC.raw_decode('{"a":1} x'))                      # ({'a': 1}, 7)
for s in ('{"a":1}  ', '{"a":1} x', '{"a":'):
    try: print(parse_all(s))
    except ValueError: print(repr(s), "invalid_json")
```

**知识点：**解析错误（Parse Errors）
