---
id: parsing-io-formats-json-strict
node: parsing-io.formats
type: qa
step: 2
---
## Q
接口规定请求体是一个只含整数、布尔、字符串的扁平 JSON 对象。直接 `json.loads` 之后，哪些不合规的输入会被它放过？要自己写解析器，还是用库？

## A
**用库管词法，子集规则用钩子和后置检查补上**

- **放过的输入**：重复键（后一个覆盖前一个）、`NaN`、`Infinity`、小数、嵌套、任意大的整数；这些都是 Python 的 `json` 接受的；
- **钩子**：`object_pairs_hook` 拿到键值对列表，在此检查重复，键已经是解码之后的（`"a/b"` 与 `"a\/b"` 是同一个键）；`parse_float` 和 `parse_constant` 可以直接拒绝小数和 `NaN`；
- **代码没做的**：整数是否在 64 位内、值是否只有三种类型，要在解析完后再递归检查一遍，注意 `True` 是 `int` 的实例，用 `type(v) is`；
- **换库的得失**：词法（转义、数字语法、截断）库已经做对，比手写省事、也更不容易出洞；子集规则库不管，要自己加；
- **错误统一**：库抛出的 `JSONDecodeError` 和你的钩子抛出的错误，在边界处都翻成同一个错误码。

```python
import json
def no_dupes(pairs):
    d = dict(pairs)
    if len(d) != len(pairs): raise ValueError("duplicate key")
    return d
def reject(token: str): raise ValueError(f"not allowed: {token}")
def strict(text: str):
    return json.loads(text, object_pairs_hook=no_dupes, parse_float=reject, parse_constant=reject)
print(json.loads('{"a":1,"a":2}'), strict('{"a":1,"b":true}'))
for s in ('{"a":1,"a":2}', '{"a/b":1,"a\\/b":2}', '{"a":NaN}', '{"a":1.5}'):
    try: strict(s)
    except ValueError as e: print(s, "->", e)
```

**知识点：**CSV 与 JSON 的稳健读写（CSV & JSON）
