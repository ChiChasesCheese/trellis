---
id: json-custom-encode-decimal-datetime
node: engineering.serialization
type: qa
source: python-docs
---
## Q
`json.dumps()` 默认只认识 dict/list/str/int/float/bool/None 这些内置类型，遇到 `Decimal` 或 `datetime` 对象会直接报错。要让它们能被序列化成 JSON，以及反序列化回来时不丢精度，分别该怎么做？

## A
序列化时给 `json.dumps(obj, default=fn)` 传一个 `default` 函数（或继承 `JSONEncoder` 并重写 `default()` 方法），当遇到 `JSONEncoder` 不认识的类型时，这个函数会被调用一次，返回一个用内置类型表示的等价值（比如把 `Decimal` 转成字符串、把 `datetime` 转成 ISO 格式字符串）。反序列化时，如果不希望 JSON 里的数字被解析成有精度损失的 `float`，可以给 `json.loads(s, parse_float=decimal.Decimal)` 传 `parse_float`，让每个 JSON 浮点数都直接被解析成 `Decimal` 而不是先变成 `float` 再转换。
